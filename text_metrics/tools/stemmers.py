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
import text_metrics.resource_pool


class DelafStemmer(object):

    """Docstring for DelafStemmer. """

    def __init__(self):
        """@todo: to be defined1. """
        pass

    def get_lemma(self, word, pos=None):

        if pos == "ADJ":
            pos = "A"
 
        word = word.lower()

        delaf_word = text_metrics.resource_pool.rp.db_helper().get_delaf_word(word, pos)

        if delaf_word is None:
            delaf_word = text_metrics.resource_pool.rp.db_helper().get_delaf_word(word)

        return delaf_word.lemma if delaf_word is not None else None
