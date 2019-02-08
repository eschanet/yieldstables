import collections

names = collections.OrderedDict()
names["ttbar"] = "t#bar{t}"
names["ttbar_allhad"] = "t#bar{t} allhad"
names["singletop"] = "Single top"
names["wjets"] = "W+jets"
names["wjets_Sherpa221"] = "W+jets"
names["zjets"] = "Z+jets"
names["zjets_Sherpa221"] = "Z+jets"
names["diboson"] = "Diboson"
names["diboson_Sherpa221"] = "Diboson"
names["ttv"] = "t#bar{t}+V"
names["tth"] = "t#bar{t}+h"
names["dijets"] = "Dijets"
names["multiboson"] = "Multiboson"
names["ttX"] = "t#bar{t}+X"
names["vh"] = "V+h"

names["C1N2_Wh_hbb_300p0_150p0"] = "(300,150)"
names["C1N2_Wh_hbb_550p0_300p0"] = "(550,300)"
names["C1N2_Wh_hbb_800p0_0p0_fs"] = "(800,0)"
names["C1N2_Wh_hbb_900p0_0p0_fs"] = "(900,0)"

def get_process_name(name):
    try:
        return names[name]
    except:
        return name
