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
from text_metrics.tools.tag.api import Tagger
from nltk.tag.util import str2tuple
from text_metrics.conf import config
import codecs
import subprocess
import tempfile


class OpenNLPTagger(Tagger):
    """A general interface for running the OpenNLP tagger."""

    def __init__(self, bin_conf, model_conf):
        """Form an OpenNLPTagger.

        :bin_conf: the name of the variable in text_metrics.conf.config that contains
            the path to the OpenNLP executable.
        :model_conf: the name of the variable in text_metrics.conf.config that contains
            the path to the model to be used by the tagger.
        """
        self._bin_conf = bin_conf
        self._model_conf = model_conf
        self._encoding = 'utf-8'

    def tag_sents(self, sentences):
        # Create a temporary input file.
        fdesc, _input_file_path = tempfile.mkstemp(text=True)
        os.close(fdesc)

        # Write the sentences to the temporary input file.
        with codecs.open(_input_file_path, mode='w', encoding=self._encoding)\
                as _input_file:
            _input = '\n'.join((' '.join(x) for x in sentences))
            _input_file.write(_input)

        with codecs.open(_input_file_path, mode='r', encoding=self._encoding)\
                as _input_file:
            # Run the tagger and get the output
            p = subprocess.Popen(self._cmd, stdin=_input_file,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

            result = p.communicate()

        return_value = self._process_output(result[0].decode(self._encoding))
        os.remove(_input_file_path)

        return return_value

    @property
    def _cmd(self):
        return [config[self._bin_conf], 'POSTagger', config[self._model_conf]]

    def _process_output(self, out):
        # Ignore the first line, containing:
        #       "Loading POS Tagger model ... done (x.xxxs)"
        # , the last three lines, containing:
        #       "Average: x sents/x
        #        Total: x sents
        #        Runtime: xs"
        # and empty lines

        lines = [line for line in out.split('\n') if line.strip()][1:-3]

        def as_tuples(line):
            return [str2tuple(token, sep='_') for token in line.split(' ')]

        return [as_tuples(line) for line in lines]
