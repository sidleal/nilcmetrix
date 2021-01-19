from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config

import math

def load_psicolinguistico():
    with open(config['PSICOLINGUISTICO'], 'r', encoding="utf-8") as fp:
        lines = fp.read().splitlines()[1:]
    lines = [i.split(',') for i in lines]
    dic = {}
    for i in lines:
        dic[i[0]] = dict()
        dic[i[0]]['concretude'] = float(i[3])
        dic[i[0]]['familiaridade'] = float(i[4])
        dic[i[0]]['imageabilidade'] = float(i[5])
        dic[i[0]]['idade_aquisicao'] = float(i[6])
    return dic
