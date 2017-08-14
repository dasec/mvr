"""Copyright 2017..."""

import argparse
import csv
from collections import defaultdict
import metrics

# parse arguments
parser = argparse.ArgumentParser(description='Calculate Relative Morph Non-Match Rate (RMNMR) of scores given in CSVs')
parser.add_argument('threshold', type=float, nargs=1,
                    help='threshold of the biometric system')
parser.add_argument('morphs', type=str, nargs=1,
                    help='path of the CSV containing the similarity-scores for morphed sample comparisons in format:'
                         '<morph-id>; <subject-id>; <sample-id>; <score>')
parser.add_argument('genuines', type=str, nargs=1,
                    help='path of the CSV containing the similarity-scores of genuine comparisons in format:'
                         '<subject-id1>; <sample-id1>; <subject-id2>; <sample-id2>; <score>')
parser.add_argument('-m', '--metric', dest='metric', default='minmax', type=str, choices=['minmax', 'prodavg'],
                    help='metric to compute MMPMR (default: compute MinMax-MMPMR)')
args = parser.parse_args()
morphPath = args.morphs[0]
genuinePath = args.genuines[0]
t = args.threshold[0]

# read morph comparison scores from csv in file structure (<morph-id>; <subject-id>; <sample-id>; <score>)
morphScores = defaultdict(lambda: defaultdict(dict))
with open(morphPath, newline='') as csvfile:
    print('reading data: ' + morphPath)
    line = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in line:
        if row:
            morphScores[row[0].lstrip()][row[1].lstrip()][row[2].lstrip()] = float(row[3])

# read genuine comparison scores from csv in file structure:
# (<subject-id1>; <sample-id1>; <subject-id2>; <sample-id2>; <score>)
genuineScores = []
with open(genuinePath, newline='') as genuinefile:
    print('reading data: ' + genuinePath)
    line = csv.reader(genuinefile, delimiter=';', quotechar='|')
    for row in line:
        if (row[0].lstrip() == row[2].lstrip()) & (row[1].lstrip() != row[3].lstrip()):
            genuineScores.append(float(row[4]))
        else:
            print('Do not compare the same sample or different subjects in genuine comparisons')

# compute MMPMR
if args.metric == 'minmax':
    print('Computing MinMax-MMPMR:, theshold: ' + str(t))
    mmpmr = metrics.calc_minmax(morphScores, t)
elif args.metric == 'prodavg':
    print('Computing ProdAvg-MMPMR:, theshold: ' + str(t))
    mmpmr = metrics.calc_prodavg(morphScores, t)
else:
    mmpmr = 0

# compute TMR (= 1-FNMR)
print('Computing TMR:, theshold: ' + str(t))
tmr = metrics.calc_tmr(genuineScores, t)

# compute RNMNR
rnmnr = tmr - mmpmr
print('RNMNR: ' + str(rnmnr))
