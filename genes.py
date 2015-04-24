#!/usr/bin/env python

import random
from names import quantile2text

mean_mutations = 3

#### Pick a histology

histology = quantile2text(random.uniform(0, 1), "histology.csv", 1, 0, ",")

#### Pick from genes with known distribution for given histology.

gene_freq = {}
gene_freq['Adenocarcinoma'] = {'EGFR': 0.10, 'ALK': 0.10, 'ERBB2': 0.04,
                               'BRAF': 0.04, 'KRAS': 0.20, 'PIK3CA': 0.04,
                               'AKT1': 0.0, 'MAP2K1': 0.04, 'MET': 0.04}
gene_freq['Squamous'] = {'EGFR': 0.04, 'ALK': 0.04, 'ERBB2': 0.0,
                         'BRAF': 0.0, 'KRAS': 0.04, 'PIK3CA': 0.04,
                         'AKT1': 0.04, 'MAP2K1': 0.0, 'MET': 0.04}

genes_for_this_hist = []

if histology != 'Large-cell':
    for gene, frequency in gene_freq[histology].iteritems():
        if random.uniform(0,1) < frequency:
            genes_for_this_hist.append(gene)

#### Pick the rest of the genes

gene_set = set(['ABL1', 'ERBB4', 'GNAQ', 'MTOR', 'RET', 'AKT1', 'EZH2', 'GNAS', 'NF1', 'ROS1', 'ALK', 'FANCA', 'HNF1A', 'NF2', 'SMAD4', 'APC', 'FANCC', 'HRAS', 'NOTCH1', 'SMARCB1', 'ATM', 'FANCD2', 'IDH1', 'NPM1', 'SMO', 'BRAF', 'FANCE', 'IDH2', 'NRAS', 'SRC', 'BRCA1', 'FANCF', 'JAK2', 'NTRK1', 'STK11', 'BRCA2', 'FANCG', 'JAK3', 'PALB2', 'TERT', 'BRIP1', 'FANCL', 'KDR', 'PDGFRA', 'TP53', 'CDH1', 'FBXW7', 'KIT', 'PDGFRB', 'TSC1', 'CDKN2A', 'FGFR1', 'KRAS', 'PIK3CA', 'TSC2', 'CSF1R', 'FGFR2', 'MET', 'PMS2', 'VHL', 'CTNNB1', 'FGFR3', 'MLH1', 'PTCH1', 'DDR2', 'FLT3', 'MPL', 'PTEN', 'EGFR', 'FOXL2', 'MSH2', 'PTPN11', 'ERBB2', 'GNA11', 'MSH6', 'RB1'])

if histology != 'Large-cell':
     for gene, frequency in gene_freq[histology].iteritems():
         if frequency > 0.0:
             gene_set.discard(gene)

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
how_many_more = mean_mutations - len(genes_for_this_hist)
if how_many_more > 0:
    genes_for_this_hist = genes_for_this_hist + \
        sample_about_how_many(gene_set, how_many_more)




print genes_for_this_hist
