from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import pickle


def concreteness():
    with open(config['CONCRETENESS'], 'rb') as fp:
        return pickle.load(fp)
