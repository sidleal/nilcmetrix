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
from sys import argv
import text_metrics
import logging
import os
import re
from itertools import chain
import nltk
from nltk.data import load
import multiprocessing
import codecs


text_metrics.config.from_object('config')
logger = logging.getLogger(__name__)

senter = load('tokenizers/punkt/portuguese.pickle')
word_tokenize = nltk.word_tokenize


def process_file(args):
    in_file, i, nfiles, out_file = args

    logger.info('Will process file %s (%d/%d)', in_file, i + 1, nfiles)

    t = text_metrics.Text(filepath=in_file, encoding='iso-8859-1')

    deleted = 0
    try:
        while not t.paragraphs[0][-1] in ('.', ':', '?', '!'):
            del t.paragraphs[0]
            deleted += 1
    except IndexError:
        logger.fatal('Ignored file %s', in_file)
        return

    logger.info('Deleted %d lines', deleted)

    sentences = chain.from_iterable(
        [senter.tokenize(p) for p in t.paragraphs])

    tokens = [[word.lower() for word in word_tokenize(sent)]
              for sent in sentences]

    joined_sentences = '\n'.join([' '.join(sentence)
                                  for sentence in tokens])
    out_file.write(joined_sentences)


def main(in_dir, out_file):
    logger.info('Listing files...')

    in_files = []
    for dirpath, dirnames, filenames in os.walk(in_dir):
        if dirpath != in_dir:
            for filename in filenames:
                in_files.append(os.path.join(dirpath, filename))

    logger.info('Found %d files in %s.', len(in_files), in_dir)

    out = open(out_file, mode='w')
    working_list = [(in_file, i, len(in_files), out)
                    for i, in_file in enumerate(in_files)]

    list(map(process_file, working_list))

    out.close()
    logger.info('Done processing directory %s.', in_dir)


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.FATAL)

    if len(argv) != 3:
        print('Usage: python', argv[0], '<in_dir>', '<out_file>')
    else:
        main(argv[1], argv[2])
