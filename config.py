import collections

# Some selections used later in the config
SRSelection  = "nJet30>=2 && nJet30<=3 && nBJet30_MV2c10==2 && mbb>100. && mbb<140. && met>240."
OneLepSelection = "&&  nLep_base==1&&nLep_signal==1 && ( (AnalysisType==1 && lep1Pt>7.) || (AnalysisType==2 && lep1Pt>6.))"
mct_bins = ["&& mct2>180. && mct2<=230.", "&& mct2>230. && mct2<=280.", "&& mct2>=280."]

#Directory to my trees
_treefilename = "/project/etp5/SUSYEWKWH/1Lbb/trees/v2-0/allTrees_v2_0_2_bkg_1Lbb_skim.root"
_sigfilename = "/project/etp5/SUSYEWKWH/1Lbb/trees/v2-0/allTrees_v2_0_signal_1Lbb_skim.root"

#Selections I want to have in my yields table. Order will be the same in the table!
selections = collections.OrderedDict()
selections["SRLM_bin1"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. && met>240." + mct_bins[0]
selections["SRLM_bin2"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. && met>240." + mct_bins[1]
selections["SRLM_bin3"] = SRSelection + OneLepSelection + "&& mt>=100. && mt<160. " + mct_bins[2]
selections["SRMM_bin1"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[0]
selections["SRMM_bin2"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[1]
selections["SRMM_bin3"] = SRSelection + OneLepSelection + "&& mt>=160. && mt<240. && met>240." + mct_bins[2]
selections["SRHM_bin1"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && mlb1>120.0" + mct_bins[0]
selections["SRHM_bin2"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && mlb1>120.0" + mct_bins[1]
selections["SRHM_bin3"] = SRSelection + OneLepSelection + "&& mt>=240. && met>240. && mlb1>120.0" + mct_bins[2]

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
        ["ttbar", "background", [(_treefilename, "ttbar_NoSys")]],
        ["wjets", "background", [(_treefilename, "wjets_NoSys")]],
        ["singletop", "background", [(_treefilename, "singletop_NoSys")]],
        ["diboson", "background", [(_treefilename, "diboson_NoSys")]],
        ["multiboson", "background", [(_treefilename, "multiboson_NoSys")]],
        ["ttv", "background", [(_treefilename, "ttv_NoSys")]],
        ["tth", "background", [(_treefilename, "tth_NoSys")]],
        ["zjets", "background", [(_treefilename, "zjets_NoSys")]],
        ["vh", "background", [(_treefilename, "vh_NoSys")]],
        ["Signal (800,0)", "signal", [(_sigfilename, "C1N2_Wh_hbb_800p0_0p0_NoSys")]],
        ["Signal (800,150)", "signal", [(_sigfilename, "C1N2_Wh_hbb_800p0_150p0_NoSys")]],
        ["Signal (700,250)", "signal", [(_sigfilename, "C1N2_Wh_hbb_700p0_250p0_NoSys")]],
        ["Signal (500,200)", "signal", [(_sigfilename, "C1N2_Wh_hbb_500p0_200p0_NoSys")]],
        ["Signal (350,150)", "signal", [(_sigfilename, "C1N2_Wh_hbb_350p0_150p0_NoSys")]],
    ],
    "selections" : selections,
    "lumifactor" : 139000,
    "weights" : "genWeight*eventWeight*pileupWeight*leptonWeight*bTagWeight*jvtWeight",
    "output_path" : "./",
    "output_name" : "yields",
}
