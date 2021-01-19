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
import idd3
import logging
from text_metrics import base
from text_metrics.resource_pool import rp as default_rp


LOGGER = logging.getLogger(__name__)


class IdeaDensity(base.Metric):
    name = 'Idea Density'
    column_name = 'idea_density'

    def value_for_text(self, t, rp=default_rp):
        engine = rp.idd3_engine()
        graphs = rp.dep_trees(t)
        sents = rp.tagged_words_in_sents(t)

        id_values = []
        for index in range(len(graphs)):
            relations = []
            for relation in graphs[index].nodes.values():
                relations.append(idd3.Relation(**relation))

            # print('Propositions:')
            try:
                engine.analyze(relations)
                # for i, prop in enumerate(engine.props):
                #     print(str(i + 1) + ' ' + str(prop))
            except Exception as e:
                LOGGER.error('{0} in engine.analyze: {1}'.format(
                    e.__class__.__name__, e))

            n_props = len(engine.props) if hasattr(engine, 'props') else 0

            # print(len(sents[index]), n_props / len(sents[index]) )
            id_values.append(n_props / len(sents[index]) if sents[index] else 0)

        return sum(id_values) / len(id_values) if id_values else 0


class ContentDensity(base.Metric):
    """
        ## Densidade de Conteúdo

        A densidade de conteúdo de um texto é calculada como o número de
        palavras de __classe aberta__ (também denominadas __palavras de
        conteúdo__) dividido pelo número de palavras de __classe fechada__
        (ou __palavras funcionais__).

        ### Exemplo:

        *Maria foi ao mercado. No mercado, comprou ovos e pão.*

        No exemplo, há 7 palavras de conteúdo (Maria, foi, mercado, mercado,
        comprou, ovos, pão), e 3 palavras funcionais (ao, no, e), o que
        resulta num valor de 7/3 = 2,33.
    """

    name = 'Content density'
    column_name = 'content_density'

    def value_for_text(self, t, rp=default_rp):
        tagged_words = rp.tagged_words(t)
        tagset = rp.pos_tagger().tagset

        content_words = [word for word in tagged_words
                         if tagset.is_content_word(word)]

        function_words = [word for word in tagged_words
                          if tagset.is_function_word(word)]

        content_density = len(content_words) / len(function_words) \
            if function_words else 0

        return content_density


class SemanticDensity(base.Category):
    name = 'Semantic Density'
    table_name = 'semantic_density'

    def __init__(self):
        super(SemanticDensity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
