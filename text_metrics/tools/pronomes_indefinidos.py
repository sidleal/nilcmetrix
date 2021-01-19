from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import codecs


def pronomes_indefinidos():
    with codecs.open(config['PRONOMES_INDEFINIDOS'], encoding='utf-8') as fp:
        return [line.strip() for line in fp.readlines()]
