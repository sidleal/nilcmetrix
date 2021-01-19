"""Helper classes for using Statistical Language Models."""

# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014-2015  Andre Luiz Verucci da Cunha
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

import re
import kenlm
import unicodedata
from sys import maxunicode, version_info


class KenLmLanguageModel(object):
    """A class for interfacing with the KenLM toolkit."""

    def __init__(self, model_path):
        # All unicode characters categorized as punctuation.
        if version_info.major == 2:
            self._punct_table = dict.fromkeys(
                (i for i in range(maxunicode)
                 if unicodedata.category(unichr(i)).startswith('P')\
                         and unichr(i) not in self.EXCEPTIONS),
                " ")
        elif version_info.major == 3:
            self._punct_table = dict.fromkeys(
                (i for i in range(maxunicode)
                 if unicodedata.category(chr(i)).startswith('P')\
                         and chr(i) not in self.EXCEPTIONS),
                " ")
        else:
            raise(Exception, "Python version is not supported")

        self.model = kenlm.LanguageModel(model_path)

    def score(self, sent):
        """Return the score assigned by the model to a sentence."""

        return self.model.score(sent)

    def clean(self, raw_sent):
        """Clean a sentence, so that it can be run
        through the model."""

        sent = self._apply_subs(raw_sent)
        sent = self._remove_punct(sent)
        sent = self._remove_multiple_spaces(sent)

        return sent.strip()

    # Auxiliary routines and data for text cleaning.

    SUBS = [[r'``', '"'],  # Fix quotation marks
            [r'\d+([,\.]\d*)?', '<NUM>'],  # Remove numbers
            [r'\(.*?\)', ' '],  # Remove parenthetical clauses
            [r'[^\u0000-\u00FF]', ' ']  # Remove invalid chars
           ]

    # Unicode considers these characters as punctuation, but we don't
    #   want to remove them.
    EXCEPTIONS = ('%')

    MULTISPACES = re.compile(r'[ \t]+')

    def _apply_subs(self, string):
        """Apply substitutions on a string."""

        for left, right in self.SUBS:
            string = re.sub(left, right, string)
        return string

    def _remove_punct(self, string):
        """Remove punctuation marks."""

        return string.translate(self._punct_table)

    def _remove_multiple_spaces(self, string):
        """Remove multiple spaces from a string."""

        return self.MULTISPACES.sub(' ', string)
