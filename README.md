# mvr
**Morphing Vulnerability Reporting** <br>
This repository provides the implementation of the metrics proposed in [1]

## Mated Morph Presentation Match Rate (MMPMR)
Calculate Mated Morph Presentation Match Rate (MMPMR). 

usage: mmpmr_python.py [-h] [-m {minmax,prodavg}] threshold path <br>
the following arguments are required: threshold, path

* **threshold**: threshold of the biometric system
* **path**: path to a csv containing the similarity scores of the morph attacks. The CSV-file needs to be of the format: <br> \<morph-id\>; \<subject-id\>; \<sample-id\>; \<score\>
* **-m** {*minmax*,*prodavg*}: Metric to calculate. MinMax-MMPMR (default) or ProdAvg-MMPMR



## Relative Morph Non Match Rate (RMNMR)
Calculate Relative Morph Non-Match Rate (RMNMR).

usage: mnmr_python.py [-h] [-m {minmax,prodavg}] threshold morphs genuines <br>
the following arguments are required: threshold, morphs, genuines

* **threshold**: threshold of the biometric system
* **morphs**: path to a CSV-file containing the similarity scores of the morph attacks. The CSV-file needs to be of the format: <br> \<morph-id\>; \<subject-id\>; \<sample-id\>; \<score\>
* **genuines**: path to a CSV-file containing the similarity scores of the genuine comparisons. The CSV-file needs to be of the format: <br>
\<subject-id1\>; \<sample-id1\>; \<subject-id2\>; \<sample-id2\>; \<score\>

<br>
<br>
[1] U. Scherhag, A. Nautsch, C. Rathgeb, et. al.: Biometric Systems under Morphing Attacks: Assessment of Morphing Techniques and Vulnerability Reporting (2017)
