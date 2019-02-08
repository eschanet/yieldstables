#!/usr/bin/env python

import ROOT
from yieldsTable import yieldsTable

import logging
from commonHelpers.logger import logger
logger = logger.getChild("yieldsTable")

import pprint
import argparse
import traceback

parser = argparse.ArgumentParser(description="Print yieldstables using a configfile.")
parser.add_argument('configfile', help='python based configfile', nargs="?")
parser.add_argument('--debug', action='store_true', help='print debug messages')

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

pprint.pprint(table)


########################################################
#
# okay, ugly stuff starts here
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
main = ''

columns = "l"
for SR in config["selections"]: columns = columns + "c"

column_names = "Process"
for SR in config["selections"]: column_names = column_names + " & \MyHead{1.0cm}{%s}" % SR.replace("_"," ")

main = main + r'''%%
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
    if "#" in me.get_process_name(point):
        point_name = "$\\mathrm{%s}$"%me.get_process_name(point)
    else:
        point_name = me.get_process_name(point)
    main = main + "{} & ".format(point_name.replace("#","\\")) + " & ".join(weighted_list) + r'''\\
'''
    if point is "Total SM":
        main = main + r'''\midrule
'''

if args.raw:
    main = main + r'''\midrule
'''
    for point,d in results.iteritems():
        if point is "Total SM":
            continue
        point = point.replace("_","\_")
        unweighted_list = []
        for SR,cutstring in cutsDict.iteritems():
            unweighted_list.append(float(d[SR]["raw"]))
        unweighted_list = [r'{:.0f}'.format(n) for n in unweighted_list]
        if "#" in me.get_process_name(point):
            point_name = "$\\mathrm{%s}$"%me.get_process_name(point)
        else:
            point_name = me.get_process_name(point)
        main = main + "Unweighted {} & ".format(point_name.replace("#","\\")) + " & ".join(unweighted_list) + r'''\\
'''

main = main + r'''\bottomrule
\end{tabular}
'''

content = header + main + footer
with open(texfile, 'w') as f:
    f.write(content)
