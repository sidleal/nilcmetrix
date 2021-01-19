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

from text_metrics.tools.tag.api import Tagger, TagSet
from text_metrics.tools.tag.opennlp import OpenNLPTagger
from text_metrics.tools.tag.macmorpho import OpenNLPMacMorphoTagger, MacMorphoTagSet
from text_metrics.tools.tag.universal import OpenNLPUniversalTagger, UniversalTagSet
from text_metrics.tools.tag.nlpnet_tagger import NLPNetTagger
