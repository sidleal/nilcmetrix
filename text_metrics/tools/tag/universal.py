# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, print_function, division
from text_metrics.tools.tag.api import TagSet
from text_metrics.tools.tag.opennlp import OpenNLPTagger


class OpenNLPUniversalTagger(OpenNLPTagger):
    """Represents an OpenNLP tagger trained on the Universal Dependencies
        corpus."""

    def __init__(self):
        super(OpenNLPUniversalTagger, self).__init__('OPENNLP_UNIVERSAL_BIN',
                                                     'OPENNLP_UNIVERSAL_MODEL')
        self.tagset = UniversalTagSet()


class UniversalTagSet(TagSet):
    """The tagset from the Universal Dependencies project.
    """
    article_tags = ['DET']
    verb_tags = ['VERB']
    auxiliary_verb_tags = ['AUX']
    noun_tags = ['NOUN',
                 'PNOUN']
    adjective_tags = ['ADJ']
    adverb_tags = ['ADV']
    pronoun_tags = ['PRON']
    numeral_tags = ['NUM']
    conjunction_tags = ['CONJ', 'SCONJ']
    preposition_tags = ['ADP',
                        'ADPPRON']
    interjection_tags = ['INTJ']

    content_word_tags = verb_tags\
        + noun_tags\
        + adjective_tags\
        + adverb_tags

    function_word_tags = article_tags\
        + preposition_tags\
        + pronoun_tags\
        + conjunction_tags\
        + interjection_tags

    functions_as_noun_tags = ['NOUN', 'PROPN']
    functions_as_adjective_tags = ['ADJ']

    punctuation_tags = ['PUNCT']

    particle_tags = ['PART']
    symbol_tags = ['SYM']
    unknown_tags = ['X']

    fine_to_coarse = {'ADPPRON': 'ADP',
                      'AUX': 'VERB',
                      'PNOUN': 'NOUN'}

    # Operators.
    # TODO: add operators, if future use is intended.
