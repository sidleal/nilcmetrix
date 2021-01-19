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
import logging
import text_metrics
from text_metrics.utils import CorpusIterator
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import TfidfModel, lsimodel


text_metrics.config.from_object('config')
logger = logging.getLogger(__name__)

dir_list = ['/home/andre/Develop/corpora/LacioWeb/proc/exatas',
            '/home/andre/Develop/corpora/LacioWeb/proc/humanas',
            '/home/andre/Develop/corpora/LacioWeb/proc/generalidades',
            '/home/andre/Develop/corpora/LacioWeb/proc/sociais',
            '/home/andre/Develop/corpora/LacioWeb/proc/agrarias',
            '/home/andre/Develop/corpora/LacioWeb/proc/religiao_pensamento',
            '/home/andre/Develop/corpora/LacioWeb/proc/saude',
            '/home/andre/Develop/corpora/FapespV2/proc',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1994',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1995',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1996',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1997',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1998',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A1999',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2000',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2001',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2002',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2003',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2005',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/A2004',
            '/home/andre/Develop/corpora/plnbr_100mil/proc/New',
            '/home/andre/Develop/corpora/wikipedia/ptwiki-proc',
            ]


def build_dictionary():
    corpus = CorpusIterator(dir_list=dir_list)

    dictionary = Dictionary(corpus)

    dictionary.save_as_text(
        '/home/andre/Develop/corpora/lsamodel_wordids.txt.bz2')

    dictionary.filter_extremes(no_below=10, no_above=0.1, keep_n=500000)

    dictionary.save_as_text(
        '/home/andre/Develop/corpora/lsamodel_wordids_filtered.txt.bz2')


def build_corpus(dictionary_path):
    dictionary = Dictionary.load_from_text(dictionary_path)
    corpus = CorpusIterator(dir_list=dir_list, bow=True, dictionary=dictionary)
    MmCorpus.serialize(
        '/home/andre/Develop/corpora/lsamodel_bow.mm',
        corpus, progress_cnt=10000)


def apply_tfidf(dictionary_path, mm_corpus_path):
    dictionary = Dictionary.load_from_text(dictionary_path)
    mm = MmCorpus(mm_corpus_path)
    tfidf = TfidfModel(mm, id2word=dictionary, normalize=True)
    MmCorpus.serialize('/home/andre/Develop/corpora/lsamodel_tfidf.mm',
                       tfidf[mm], progress_cnt=10000)


def build_model(dictionary_path, mm_corpus_path):
    dictionary = Dictionary.load_from_text(dictionary_path)
    # Use the if-idf corpus here, not the original one.
    mm = MmCorpus(mm_corpus_path)
    lsi = lsimodel.LsiModel(corpus=mm, id2word=dictionary, num_topics=400)
    lsi.save('/home/andre/Develop/corpora/lsamodel_lsi.model')


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    if argv[1] == 'build_dictionary':
        build_dictionary()
    elif argv[1] == 'build_corpus':
        build_corpus(argv[2])
    elif argv[1] == 'apply_tfidf':
        apply_tfidf(argv[2], argv[3])
    elif argv[1] == 'build_model':
        build_model(argv[2], argv[3])
    elif argv[1] == 'all':
        build_dictionary()
        build_corpus(
            '/home/andre/Develop/corpora/new/lsamodel_wordids_filtered.txt.bz2')
        apply_tfidf(
            '/home/andre/Develop/corpora/new/lsamodel_wordids_filtered.txt.bz2',
            '/home/andre/Develop/corpora/new/lsamodel_bow.mm')
        build_model(
            '/home/andre/Develop/corpora/new/lsamodel_wordids_filtered.txt.bz2',
            '/home/andre/Develop/corpora/new/lsamodel_tfidf.mm')

