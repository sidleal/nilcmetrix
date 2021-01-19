from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import codecs


def simple_words():
    with codecs.open(config['SIMPLE_WORDS'], encoding='utf-8') as fp:
        return [line.split(',')[0].strip() for line in fp.readlines()]


def discourse_markers():
    with codecs.open(config['DISCOURSE_MARKERS'], encoding='utf-8') as fp:
        return [line.strip() for line in fp.readlines()]


def ambiguous_discourse_markers():
    with codecs.open(config['AMBIGUOUS_DISCOURSE_MARKERS'], encoding='utf-8') as fp:
        return[line.strip() for line in fp.readlines()]
