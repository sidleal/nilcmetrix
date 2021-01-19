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


class DependencyParser(object):

    """Basic interface for a parser in the system. """

    def parse_tagged(self, sent):
        """Parse a sentence.

        :sent: the sentence to parse.
        :returns: an nltk.parse.dependencygraph.DependencyGraph object,
            representing the parse tree for the sentence.
        """
        return self.parse_tagged_sents([sent])[0]

    def parse_tagged_sents(self, tagged_sents):
        """Parse a list of strings.

        :tagged_sents: a list of tagged sentences to parse.
        :returns: a list of nltk.parse.dependencygraph.DependencyGraph objects,
            one for each sentence in sents.
        """
        raise NotImplementedError()
