__author__ = "Ulrich Scherhag"
__copyright__ = "Copyright (C) 2017 Hochschule Darmstadt"
__license__ = "License Agreement provided by Hochschule Darmstadt" \
              "(https://github.com/dasec/mvr/blob/master/mvr-license-170816.pdf)"
__version__ = "1.0"

import argparse
import csv
from collections import defaultdict
import metrics

# parse arguments

parser = argparse.ArgumentParser(description='Calculate Relative Morph Non-Match Rate (RMNMR) of scores given in CSVs')
parser.add_argument('threshold', type=float,
                    help='threshold of the biometric system')
parser.add_argument('morphs', type=str,
                    help='path of the CSV containing the similarity-scores for morphed sample comparisons in format:'
                         '<morph-id>; <subject-id>; <sample-id>; <score>')
parser.add_argument('bona_fide', type=str,
                    help='path of the CSV containing the similarity-scores of bona fide comparisons in format:'
                         '<subject-id1>; <sample-id1>; <subject-id2>; <sample-id2>; <score>')
parser.add_argument('-m', '--metric', dest='metric', default='minmax', type=str, choices=['minmax', 'prodavg'],
                    help='metric to compute MMPMR (default: compute MinMax-MMPMR)')
args = parser.parse_args()

# read morph comparison scores from csv in file structure (<morph-id>; <subject-id>; <sample-id>; <score>)
morphScores = defaultdict(lambda: defaultdict(dict))
with open(args.morphs, newline='') as csvfile:
    print('reading data: ' + args.morphs)
    line = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in line:
        if row:
            morphScores[row[0].lstrip()][row[1].lstrip()][row[2].lstrip()] = float(row[3])

# read bona fide comparison scores from csv in file structure:
# (<subject-id1>; <sample-id1>; <subject-id2>; <sample-id2>; <score>)
bona_fide_scores = []
with open(args.bona_fide, newline='') as bona_fide_file:
    print('reading data: ' + args.bona_fide)
    line = csv.reader(bona_fide_file, delimiter=';', quotechar='|')
    for row in line:
        if (row[0].lstrip() == row[2].lstrip()) & (row[1].lstrip() != row[3].lstrip()):
            bona_fide_scores.append(float(row[4]))
        else:
            print('Do not compare the same sample or different subjects in bona fide comparisons')

# compute MMPMR
if args.metric == 'minmax':
    print('Computing MinMax-MMPMR:, theshold: ' + str(args.threshold))
    mmpmr = metrics.calc_minmax(morphScores, args.threshold)
elif args.metric == 'prodavg':
    print('Computing ProdAvg-MMPMR:, theshold: ' + str(args.threshold))
    mmpmr = metrics.calc_prodavg(morphScores, args.threshold)
else:
    mmpmr = 0

# compute TMR (= 1-FNMR)
print('Computing TMR:, theshold: ' + str(args.threshold))
tmr = metrics.calc_tmr(bona_fide_scores, args.threshold)

# compute RNMNR
rnmnr = tmr - mmpmr
print('RNMNR: ' + str(rnmnr))
