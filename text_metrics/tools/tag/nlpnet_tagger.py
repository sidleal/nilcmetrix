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
import nlpnet
from text_metrics.tools.tag.api import Tagger
from text_metrics.tools.tag.macmorpho import MacMorphoTagSet
from text_metrics.conf import config


class NLPNetTagger(Tagger):

    """Docstring for NLPNetTagger. """

    def __init__(self, data_dir=None):
        self.tagset = MacMorphoTagSet()
        self._data_dir = data_dir
        self._tagger = None

    def load_tagger(self):
        if not self._data_dir:
            self._data_dir = config['NLPNET_DATA_DIR']

        nlpnet.set_data_dir(self._data_dir)
        self._tagger = nlpnet.POSTagger()

    def tag(self, tokens):
        if not self._tagger:
            self.load_tagger()
        return list(zip(tokens, self._tagger.tag_tokens(tokens)))
