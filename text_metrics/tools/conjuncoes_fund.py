from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import codecs


def conjuncoes_fund1():
    with codecs.open(config['CONJUNCOES_FUND1'], encoding='utf-8') as fp:
        return fp.read().splitlines()


def conjuncoes_fund2():
    with codecs.open(config['CONJUNCOES_FUND2'], encoding='utf-8') as fp:
        return fp.read().splitlines()
