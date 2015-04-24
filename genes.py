#!/usr/bin/env python

import random
from names import quantile2text

histology = quantile2text(random.uniform(0, 1), "histology.csv", 1, 0, ",")

gene_list = ['ABL1', 'ERBB4', 'GNAQ', 'MTOR', 'RET', 'AKT1', 'EZH2', 'GNAS', 'NF1', 'ROS1', 'ALK', 'FANCA', 'HNF1A', 'NF2', 'SMAD4', 'APC', 'FANCC', 'HRAS', 'NOTCH1', 'SMARCB1', 'ATM', 'FANCD2', 'IDH1', 'NPM1', 'SMO', 'BRAF', 'FANCE', 'IDH2', 'NRAS', 'SRC', 'BRCA1', 'FANCF', 'JAK2', 'NTRK1', 'STK11', 'BRCA2', 'FANCG', 'JAK3', 'PALB2', 'TERT', 'BRIP1', 'FANCL', 'KDR', 'PDGFRA', 'TP53', 'CDH1', 'FBXW7', 'KIT', 'PDGFRB', 'TSC1', 'CDKN2A', 'FGFR1', 'KRAS', 'PIK3CA', 'TSC2', 'CSF1R', 'FGFR2', 'MET', 'PMS2', 'VHL', 'CTNNB1', 'FGFR3', 'MLH1', 'PTCH1', 'DDR2', 'FLT3', 'MPL', 'PTEN', 'EGFR', 'FOXL2', 'MSH2', 'PTPN11', 'ERBB2', 'GNA11', 'MSH6', 'RB1']

def binomialvariate(n,p):
    X = 0
    for i in range(n):
        if random.uniform(0,1) < p:
            X = X + 1
    return X

def sample_about_how_many(list, how_many):
    n = float(how_many)
    return random.sample(list, binomialvariate(len(list), n/len(list)))

print histology
print sample_about_how_many(gene_list, 3)
