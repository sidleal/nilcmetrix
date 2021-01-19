"""Routines for cleaning text corpora, in preparation for SLM training."""

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

from __future__ import print_function

import re
import codecs
import unicodedata
from sys import argv, maxunicode
from os.path import basename, splitext, dirname, join

SUBS = [[r'``', '"'],  # Fix quotation marks
        [r'\d+([,\.]\d*)?', '<NUM>'],  # Remove numbers
        [r'\(.*?\)', ' '],  # Remove parenthetical clauses
        [r'[^\u0000-\u00FF]', ' ']  # Remove invalid chars
       ]

for j in range(len(SUBS)):
    SUBS[j][0] = re.compile(SUBS[j][0])

# All unicode characters categorized as punctuation.
EXCEPTIONS = ('%')
PUNCT_TABLE = dict.fromkeys((i for i in range(maxunicode)
                             if unicodedata.category(chr(i)).startswith('P')\
                                     and chr(i) not in EXCEPTIONS),
                            " ")

MULTISPACES = re.compile(r'[ \t]+')


def apply_subs(subs, string):
    """Apply substitutions on a string."""

    for left, right in subs:
        string = left.sub(right, string)
    return string


def remove_punct(string):
    """Remove punctuation marks."""

    return string.translate(PUNCT_TABLE)


def remove_multiple_spaces(string):
    """Remove multiple spaces from a string."""

    return MULTISPACES.sub(' ', string)


def count_lines(filename):
    """Count lines in file."""

    with open(filename) as in_f:
        count = 0
        for _ in in_f:
            count += 1
        return count


if __name__ == '__main__':
    for path in argv[1:]:
        print("Processing file", path)
        total_lines = count_lines(path)

        outdir = dirname(path)
        base = basename(path)
        name, ext = splitext(base)
        outfilepath = join(outdir, name + '_clean' + ext)

        with codecs.open(path, mode='r', encoding='utf-8') as infile,\
                codecs.open(outfilepath, mode='w', encoding='utf-8') as outfile:
            for lcount, line in enumerate(infile):
                print('{0}/{1}'.format(lcount, total_lines), end="\r")
                line = apply_subs(SUBS, line)
                line = remove_punct(line)
                line = remove_multiple_spaces(line)
                outfile.write(line.strip())
                outfile.write('\n')
            print('')
