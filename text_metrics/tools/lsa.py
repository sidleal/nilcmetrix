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

import pickle

import numpy as np
from gensim.matutils import cossim
from scipy import spatial


class LsaSpace(object):
    """Represents an LSA space, that can be used to compute similarities
    between text fragments (texts, paragraphs, sentences, and so on).
    """

    def __init__(self, model_path):
        """Load an LSA space from a file.

        :dict_path: path to the dictionary file.
        :model_path: path to the model file.
        """
        f = open(model_path, 'rb')
        self._lsa_model = pickle.load(f)
        f.close()

    def word2vec(self, word):
        if word.lower() in self._lsa_model:
            return self._lsa_model[word.lower()]
        else:
            return np.full(self.num_topics, 0.001)

    def doc2vec(self, tokens):
        word_vec = []
        for word in tokens:
            if len(word) > 2:
                vec = self.word2vec(word)
                word_vec.append(vec)
        if len(word_vec) < 1:
            return []
        doc_vec = np.average(word_vec, axis=0)
        ids = list(range(0, self.num_topics))
        zdoc_vec = list(zip(ids, doc_vec))
        return zdoc_vec

    def get_vector(self, doc):
        return self.doc2vec(doc)

    @property
    def num_topics(self):
        """Return the number of topics in the model."""
        return 300

    def compute_similarity(self, doc1, doc2):
        """Compute the cosine similarity between two documents.

        :doc1: a list of strings, representing the first document.
        :doc2: a list of strings, representing the second document.
        :returns: a number between -1 and 1, representing the similarity
        between the two documents.
        """
        return cossim(self.get_vector(doc1), self.get_vector(doc2))


if __name__ == '__main__':
    from text_metrics.conf import config

    space = LsaSpace(config['LSA_MODEL_PATH'])

    print(space.compute_similarity('o livro está sobre a mesa do menino'.split(' '),
                                   'o livro está sobre a cadeira'.split(' ')))

    print(space.compute_similarity('o livro está sobre a mesa'.split(' '),
                                   'o livro está sobre a árvore'.split(' ')))

    print(space.compute_similarity('o livro está sobre a mesa'.split(' '),
                                   'maria foi ao mercado'.split(' ')))
