__author__ = "Ulrich Scherhag"
__copyright__ = "Copyright (C) 2017 Hochschule Darmstadt"
__license__ = "License Agreement provided by Hochschule Darmstadt" \
              "(https://github.com/dasec/mvr/blob/master/mvr-license-170816.pdf)"
__version__ = "1.0"

import operator
from functools import reduce
from statistics import mean


def calc_minmax(mdata, threshold):
    """
    compute MinMax-MMPMR
    :param mdata: dictionary of dictionaries of dictionaries: <morph-id>; <subject-id>; <sample-id>; <score>
    :param threshold: threshold of the biometric system
    :return: MinMax-MMPMR
    """
    for morph in mdata:
        for subj in mdata[morph]:
            mdata[morph][subj] = max(mdata[morph][subj].values())
    '''
        data[morph] = (min(data[morph].values()) > threshold)
    return list(data.values()).count(True) / len(data)
    '''
    return mean(min(i.values()) > threshold for i in mdata.values())


def calc_prodavg(mdata, threshold):
    """
    compute ProdAvg-MMPMR
    :param mdata: dictionary of dictionaries of dictionaries: <morph-id>; <subject-id>; <sample-id>; <score>
    :param threshold: threshold of the biometric system
    :return: ProdAvg-MMPMR
    """
    for morph in mdata:
        for subj in mdata[morph]:
            mdata[morph][subj] = mean(sample > threshold for sample in mdata[morph][subj].values())
        mdata[morph] = reduce(operator.mul, mdata[morph].values(), 1)
    return mean(mdata.values())


def calc_tmr(data, threshold):
    """
    compute True Match Rate (TMR) (=1-FNMR)
    :param data: list of bona fide similarity-scores
    :param threshold: threshold of the biometric system
    :return: TMR
    """
    return mean(sample > threshold for sample in data)
