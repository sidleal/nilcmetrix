from __future__ import unicode_literals, print_function, division
from text_metrics.conf import config
import codecs

def _read_liwc_dictionary(filename):
    """
    Read a LIWC dictionary, returning the list of patterns.

    This takes care of fixing the `*` wildcards, which should be interpreted as
    a /[A-Za-z]*/ regular expression.

    :param filename: LIWC dictionary file name.
    :return: List of regexes to match.
    """
    with codecs.open(filename, encoding='utf-8') as fp:
        return [line.replace("*", r"[A-Za-z]*").strip() for line in fp]

def positive_words():
    return _read_liwc_dictionary(config['LIWC_POS'])

def negative_words():
    return _read_liwc_dictionary(config['LIWC_NEG'])
