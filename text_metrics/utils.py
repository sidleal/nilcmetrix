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
import os
from os.path import dirname, abspath
from sys import modules
from nltk.tree import Tree
import logging
import codecs
from itertools import chain

logger = logging.getLogger(__name__)
base_path = abspath(dirname(modules[__name__].__file__))

def adjacent_pairs(l):
    """Yield all pairs of adjecent elements in the list.

    :l: a list.
    :returns: an iterator over the adjacent pairs of elements.

    """
    for i in range(len(l) - 1):
        yield l[i], l[i + 1]


def all_pairs(l):
    """Yield all pairs of elements in the list.

    :l: a list.
    :returns: an iterator over the pairs of elements.

    """
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            yield l[i], l[j]


class CorpusIterator(object):

    """An iterator that returns one document at a time. """

    def __init__(self, dir_list, encoding='utf-8', chain=True,
                 bow=False, dictionary=None):
        self._dir_list = dir_list
        self._build_file_list()
        self._encoding = encoding
        self._current = 0
        self._chain = chain

        if bow:
            self._bow = True
            self._chain = True
            self._dictionary = dictionary
        else:
            self._bow = False

    def _build_file_list(self):
        self._file_list = []
        for dir_name in self._dir_list:
            for file_name in os.listdir(dir_name):
                self._file_list.append(os.path.join(dir_name, file_name))

        self._nfiles = len(self._file_list)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current < len(self._file_list):
            logger.info('Loaded file %d/%d: %s', self._current + 1,
                        self._nfiles, self._file_list[self._current])

            with codecs.open(self._file_list[self._current],
                             encoding=self._encoding, mode='r') as infile:
                content_lines = [line.strip().split(' ')
                                 for line in infile.readlines()]
                content = list(chain.from_iterable(content_lines))\
                    if self._chain else content_lines

                content = self._dictionary.doc2bow(content)\
                    if self._bow else content

            self._current += 1

            return content
        else:
            raise StopIteration


def ilen(it):
    """Calculate the number of elements in an iterable."""
    if isinstance(it, list) or isinstance(it, tuple):
        return len(it)

    count = 0
    for i in it:
        count = count + 1
    return count


def is_valid_id(string):
    """Check whether a string is a valid id.

    :string: The string to be checked
    :returns: True if the string represents a valid id; false otherwise.
    """
    import re

    return re.match("^[_A-Za-z][_a-zA-Z0-9]*$", string) is not None


def reverse_tree(tree):
    """Reverses (in place) a syntax tree.

    :tree: The tree to be reversed.
    :returns: None (the tree is reversed in place.)
    """
    if isinstance(tree, Tree):
        tree.reverse()
        for child in tree:
            reverse_tree(child)


def find_subtrees(tree, *labels):
    """Return a list of the subtrees of a tree that contain the given label.

    :tree: a tree.
    :labels: a list of node label (e.g., NP, VP, etc.).
    :returns: a list of trees.
    """
    subtrees = []
    for label in labels:
        for subtree in tree.subtrees():
            if subtree.label() == label:
                subtrees.append(subtree)
    return subtrees


# The following functions are used for counting the occurrences of operators
#   and connectives in a text.


def matches(candidate, operator, ignore_pos=False):
    """Check if candidate matches operator.

    :candidate: a token.
    :operator: an operator.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: True if candidate matches operator; False otherwise.
    """
    if ignore_pos:
        return [w for w, _ in candidate] == [w for w, _ in operator]
    else:
        for token, oper in zip(candidate, operator):
            if type(oper[1]) is str:
                if token != oper:
                    return False
            elif type(oper[1]) is tuple:
                if token[0] != oper[0] or token[1] not in oper[1]:
                    return False
        return True


def count_occurrences(tagged_sent, operator, ignore_pos=False):
    """Count the number of occurrences of an operator in a tagged sentence.

    :tagged_sent: a tagged sentence.
    :operator: an operator.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: The number of times the operator occurs in the sentence.
    """
    # 'tagged_sent' is like
    # [('O', 'ART'), ('gato', 'N'), ('sumiu', 'V'), ('.', 'PU')]
    # 'operator' is like
    # [('e', 'KC')]

    occurrences = 0
    for i, token in enumerate(tagged_sent):
        if token[0].lower() == operator[0][0]:
            candidate = [(w.lower(), t)
                         for w, t in tagged_sent[i:(i + len(operator))]]
            # print('can  ', candidate)
            if matches(candidate, operator, ignore_pos):
                occurrences += 1

    return occurrences


def count_occurrences_for_all(tagged_sent, operators, ignore_pos=False):
    """Count the total number of occurrences of a list of operators in a
    sentence.

    :tagged_sent: a tagged sentence.
    :operators: a list of operators.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: The sum of the occurrences of each operator in the sentence.
    """
    return sum([count_occurrences(tagged_sent, operator, ignore_pos)
                for operator in operators])
