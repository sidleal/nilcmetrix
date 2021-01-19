from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import pickle
import math

def palavras_dificeis():
    with open(config['PALAVRAS_DIFICEIS'], 'rb') as fp:
        return pickle.load(fp)


def calc_log(words, dic):
        sum = 0
        count = 0
        for w in words:
            try:
                sum += math.log(dic[w] + 1)
                count += 1
            except:
                pass
        if count > 0:
            return sum / count
        else:
            return 0
