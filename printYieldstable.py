#!/usr/bin/env python

import ROOT
from yieldsTable import yieldsTable

import logging
from commonHelpers.logger import logger
from commonHelpers import process_names

logger = logger.getChild("yieldsTable")

import machete

import os
import pprint
import argparse
import traceback

parser = argparse.ArgumentParser(description="Print yieldstables using a configfile.")
parser.add_argument('configfile', help='python based configfile', nargs="?")
parser.add_argument('--debug', action='store_true', help='print debug messages')
parser.add_argument('--no-raw', action='store_true', help='do not print raw yields')
args = parser.parse_args()

if args.debug:
    logging.getLogger("yieldsTable").setLevel(logging.DEBUG)

if not args.configfile:
    raise Exception("Need to specify a config file")

if args.configfile:
    try:
        exec(open(args.configfile).read())
    except:
        print("can't read configfile {}".format(args.configfile))
        traceback.print_exc()

yieldsTable = yieldsTable(**config)
table = yieldsTable.createYieldstable()

logger.info("Got table")

########################################################
#
# okay, ugly TeX stuff starts here
#
########################################################

header = r'''\documentclass{standalone}
\usepackage{longtable}
\usepackage{booktabs}
\newcommand\MyHead[2]{%
  \multicolumn{1}{l}{\parbox{#1}{\centering #2}}
}
\begin{document}
'''
footer = r'''
\end{document}
'''
table_header = ''
table_footer = ''
total_sm = ''
main = ''

columns = "l"
for SR in config["selections"]: columns = columns + "c"

column_names = "Process"
for SR in config["selections"]: column_names = column_names + " & \MyHead{1.0cm}{%s}" % SR.replace("_"," ")

table_header = table_header + r'''%%
\begin{tabular}{%s}
\toprule
%s \\
\midrule
%%
''' % (columns,column_names)

for process,d in table.iteritems():

    process = process.replace("_","\_")
    weighted_list = []
    error_list = []

    for SR,cutstring in config["selections"].iteritems():
        weighted_list.append(float(d[SR]["weighted"]))
        error_list.append(float(d[SR]["error"]))

    weighted_list = [r'${:.2f} \pm {:0.2f}$'.format(n,e) for n,e in zip(weighted_list,error_list)]

    if "#" in process_names.get_process_name(process):
        process_name = "$\\mathrm{%s}$"%process_names.get_process_name(process)
    else:
        process_name = process_names.get_process_name(process)

    if "Total SM" in process:
        total_sm = "{} & ".format(process_name.replace("#","\\")) + " & ".join(weighted_list) + r'''\\
\midrule
'''
    else:
        main = main + "{} & ".format(process_name.replace("#","\\")) + " & ".join(weighted_list) + r'''\\
'''

if not args.no_raw:
    main = main + r'''\midrule
'''
    for process,d in table.iteritems():
        if process is "Total SM":
            continue
        process = process.replace("_","\_")
        unweighted_list = []
        for SR,cutstring in config["selections"].iteritems():
            unweighted_list.append(float(d[SR]["raw"]))
        unweighted_list = [r'{:.0f}'.format(n) for n in unweighted_list]
        if "#" in process_names.get_process_name(process):
            process_name = "$\\mathrm{%s}$"%process_names.get_process_name(process)
        else:
            process_name = process_names.get_process_name(process)
        main = main + "Unweighted {} & ".format(process_name.replace("#","\\")) + " & ".join(unweighted_list) + r'''\\
'''

table_footer = table_footer + r'''\bottomrule
\end{tabular}
'''

content = header + table_header + total_sm + main + table_footer + footer

if not os.path.exists(config["output_path"]):
    os.makedirs(config["output_path"])
with open(config["output_path"]+config["output_name"]+".tex", 'w') as f:
    f.write(content)
