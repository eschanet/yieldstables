import ROOT

import collections
import re
import os
import math
from commonHelpers.logger import logger
import re
import glob
import json
from pprint import pprint

logger = logger.getChild("yieldsTable")

class yieldsTable:
    def __init__(self,
                 selections=None,
                 processes=None,
                 weights=None,
                 lumifactor=None):

        logger.info("Initializing yieldsTable")

        self.selections = selections
        self.processes = processes
        self.weights = weights
        self.lumifactor = lumifactor
        self.bkg_processes = [processname for processname,type,trees in self.processes if type == "background"]

    def createYieldstable(self):
        """
        create the yieldsTable
        table is returned as json
        """

        logger.info("Creating yieldstable")

        nested_dict = lambda: collections.defaultdict(nested_dict)

        open_trees = {} # index "filename_treename"
        open_files = {}

        yields_dict = nested_dict()

        for process,type,processtrees in self.processes:

            logger.info("Projecting {}".format(process))

            raw = 0
            weighted = 0
            error = 0

            for selection,cuts in self.selections.iteritems():
                yields_dict[process][selection]["raw"] = 0
                yields_dict[process][selection]["weighted"] = 0.0
                yields_dict[process][selection]["error"] = 0.0

                for filename, treename in processtrees:
                    index = "{}_{}".format(filename, treename)
                    if index in open_trees:
                        tree = open_trees[index]
                    else:
                        if filename in open_files:
                            rootfile = open_files[filename]
                        else:
                            rootfile = ROOT.TFile(filename)
                            open_files[filename] = rootfile
                        tree = rootfile.Get(treename)
                        open_trees[index] = tree

                    logger.debug("Projecting {} in file {} with selection {}".format(treename,filename,selection))

                    h = ROOT.TH1F("h","",1,0.5,1.5)
                    h.Sumw2()
                    yields_dict[process][selection]["raw"] += tree.Project("h","1","({})*({})*({})".format(self.lumifactor,self.weights,cuts))
                    yields_dict[process][selection]["weighted"] += h.Integral()
                    yields_dict[process][selection]["error"] += h.GetBinError(1)**2
                    del h
                yields_dict[process][selection]["error"] = math.sqrt(yields_dict[process][selection]["error"])

        for selection in self.selections:
            logger.debug("Summing up SM -- selection {}".format(selection))
            bkg_total_unweighted = 0
            bkg_total_weighted = 0
            bkg_total_error = 0
            for process in self.bkg_processes:
                logger.debug("Summing up SM -- process {}".format(process))
                bkg_total_unweighted += yields_dict[process][selection]["raw"]
                bkg_total_weighted += yields_dict[process][selection]["weighted"]
                bkg_total_error += yields_dict[process][selection]["error"]**2
            bkg_total_error = math.sqrt(bkg_total_error)
            yields_dict["Total SM"][selection] = {"raw":bkg_total_unweighted, "weighted":bkg_total_weighted, "error":bkg_total_error}

        return yields_dict
