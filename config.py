import collections

# Need this for computing mlb1 using existing information from tree
ROOT.gInterpreter.Declare('''
Double_t getMlb1(Double_t jet1MV2c10, Double_t lj1_eta, Double_t lj2_eta, Double_t lj1_phi, Double_t lj2_phi, Double_t jet1Pt, Double_t jet2Pt, Double_t lep1Pt)
{
    if(jet1MV2c10>=0.64) {
        return sqrt(2*lep1Pt*jet1Pt*(cosh(lj1_eta)-cos(lj1_phi)));
    }
    return sqrt(2*lep1Pt*jet2Pt*(cosh(lj2_eta)-cos(lj2_phi)));
}
''')

# Some selections used later in the config
SRSelection  = "nJet30>=2 && nJet30<=3 && nBJet30_MV2c10==2 && mbb>100. && mbb<140. && met>240."
OneLepSelection = "&&  nLep_base==1&&nLep_signal==1 && ( (AnalysisType==1 && lep1Pt>7.) || (AnalysisType==2 && lep1Pt>6.))"
mct_bins = ["&& mct2>180. && mct2<=220.", "&& mct2>220. && mct2<=280.", "&& mct2>=280."]

#Directory to my trees
_treefilename = "/project/etp4/eschanet/ntuples/common/full_run_2/v1-20/allTrees_v1_20_1_combined_bkg_skimmed.root"

#Selections I want to have in my yields table. Order will be the same in the table!
selections = collections.OrderedDict()
selections["SRLM_bin1"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. && met>240." + mct_bins[0]
selections["SRLM_bin2"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. && met>240." + mct_bins[1]
selections["SRLM_bin3"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. " + mct_bins[2]
selections["SRMM_bin1"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[0]
selections["SRMM_bin2"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[1]
selections["SRMM_bin3"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[2]
selections["SRHM_bin1"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && getMlb1(jet1MV2c10,lep1Eta-jet1Eta,lep1Eta-jet2Eta,lep1Phi-jet1Phi,lep1Phi-jet2Phi,jet1Pt,jet2Pt,lep1Pt)>120.0" + mct_bins[0]
selections["SRHM_bin2"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && getMlb1(jet1MV2c10,lep1Eta-jet1Eta,lep1Eta-jet2Eta,lep1Phi-jet1Phi,lep1Phi-jet2Phi,jet1Pt,jet2Pt,lep1Pt)>120.0" + mct_bins[1]
selections["SRHM_bin3"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && getMlb1(jet1MV2c10,lep1Eta-jet1Eta,lep1Eta-jet2Eta,lep1Phi-jet1Phi,lep1Phi-jet2Phi,jet1Pt,jet2Pt,lep1Pt)>120.0" + mct_bins[2]


################################################################################################
#
#       Actual configuration
#
#  1. A. Processes are defined by their name (first element).
#     B. Second element indicates whether this is a background or signal process.
#     C. Third element is a list of tuples (filename, treename), in case you have multiple trees for a given process
#
#  2. Lumifactor is given in fb.
#
################################################################################################
config = {
    "processes" : [
        ("ttbar", "background", [(_treefilename, "ttbar_NoSys")]),
        ("wjets", "background", [(_treefilename, "wjets_NoSys")]),
        ("singletop", "background", [(_treefilename, "singletop_NoSys")]),
        ("diboson", "background", [(_treefilename, "diboson_NoSys")]),
        ("multiboson", "background", [(_treefilename, "multiboson_NoSys")]),
        ("ttv", "background", [(_treefilename, "ttv_NoSys")]),
        ("tth", "background", [(_treefilename, "tth_NoSys")]),
        ("zjets", "background", [(_treefilename, "zjets_NoSys")]),
        ("vh", "background", [(_treefilename, "vh_NoSys")]),
    ],
    "selections" : selections,
    "lumifactor" : 140500,
    "weights" : "genWeight*eventWeight*pileupWeight*leptonWeight*bTagWeight*jvtWeight",
    "output_path" : "/project/etp5/eschanet/studies/1Lbb_Wh_Run2_reopt_full_new_vars/yieldstables/test_module/",
    "output_name" : "yields",
}
