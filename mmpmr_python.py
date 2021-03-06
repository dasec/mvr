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

parser = argparse.ArgumentParser(description='Calculate Mated Morph Presentation Match Rate (MMPMR) of scores given '
                                             'in CSV')
parser.add_argument('threshold', type=float,
                    help='threshold of the biometric system')
parser.add_argument('path', type=str,
                    help='path of the CSV containing the similarity-scores in format:'
                         '<morph-id>; <subject-id>; <sample-id>; <score>')
parser.add_argument('-m', '--metric', dest='metric', default='minmax', type=str, choices=['minmax', 'prodavg'],
                    help='metric to compute MMPMR (default: compute MinMax-MMPMR)')
args = parser.parse_args()

# read data from csv in file structure (<morph-id>; <subject-id>; <sample-id>; <score>)
data = defaultdict(lambda: defaultdict(dict))
with open(args.path, newline='') as csvfile:
    print('reading data: ' + args.path)
    line = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in line:
        if row:
            data[row[0].lstrip()][row[1].lstrip()][row[2].lstrip()] = float(row[3])

# calculate metric
if args.metric == 'minmax':
    print('Computing MinMax-MMPMR:, theshold: ' + str(args.threshold))
    print(metrics.calc_minmax(data, args.threshold))
elif args.metric == 'prodavg':
    print('Computing ProdAvg-MMPMR:, theshold: ' + str(args.threshold))
    print(metrics.calc_prodavg(data, args.threshold))
