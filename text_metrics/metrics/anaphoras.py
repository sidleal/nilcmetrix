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
import re
from text_metrics import base
from text_metrics.resource_pool import rp as default_rp


class AnaphoricReferencesBase(base.Metric):
    """Docstring for AnaphoricReferencesBase. """

    referents = {r'^elas$': 'fp',
                 r'^nelas$': 'fp',
                 r'^delas$': 'fp',
                 r'^.*-nas$': 'fp',
                 r'^.*-las$': 'fp',
                 r'^.*-as$': 'fp',
                 r'^eles$': 'mp',
                 r'^neles$': 'mp',
                 r'^deles$': 'mp',
                 r'^.*-nos$': 'mp',
                 r'^.*-los$': 'mp',
                 r'^.*-os$': 'mp',
                 r'^ela$': 'fs',
                 r'^nela$': 'fs',
                 r'^dela$': 'fs',
                 r'^.*-na$': 'fs',
                 r'^.*-la$': 'fs',
                 r'^.*-a$': 'fs',
                 r'^ele$': 'ms',
                 r'^nele$': 'ms',
                 r'^dele$': 'ms',
                 r'^.*-no$': 'ms',
                 r'^.*-lo$': 'ms',
                 r'^.*-o$': 'ms',
                 r'^lhes$': 'ap',
                 r'^lhe$': 'as',
                 }

    def __init__(self, nsentences=1):
        """Form an AnaphoricReferencesBase object.

        :nsentences: the number of sentences to look back for anaphoric
            references.
        """

        super(AnaphoricReferencesBase, self).__init__()

        self.nsentences = nsentences

        self.compiled_referents = {}
        for regex, category in self.referents.items():
            self.compiled_referents[regex] = re.compile(regex)

    def find_candidates(self, sentences, indices, category, rp):
        """Find nouns of a certain gender/number in a list of sentences.

        :sentences: the tagged sentences.
        :indices: the indices of the sentences to be searched.
        :category: the category of nouns to look for (ms, mp, fs, fp, as, ap).
        :rp: the resource pool to use.
        :returns: a list of nouns matching the category.
        """

        candidates = []
        for i in indices:
            if (i, category) not in self.computed_categories:
                sentence = sentences[i]
                curr_candidates = []

                for token in sentence:
                    if rp.pos_tagger().tagset.is_noun(token):
                        attrs = rp.db_helper().get_delaf_noun(token[0].lower())
                        if not attrs:
                            continue
                        if category == 'ap':
                            if attrs.morf in ('mp', 'fp'):
                                curr_candidates.append(token[0])
                        elif category == 'as':
                            if attrs.morf in ('ms', 'fs'):
                                curr_candidates.append(token[0])
                        else:
                            if attrs.morf == category:
                                curr_candidates.append(token[0])

                self.computed_categories[(i, category)] = curr_candidates

            candidates.extend(self.computed_categories[(i, category)])

        return candidates

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.tagged_sentences(t)

        if len(tokens) <= 1:
            return 0

        ncandidates = 0
        self.computed_categories = {}
        for isent in range(1, len(tokens)):
            iprev_sents = range(max(isent - self.nsentences, 0), isent)

            for token in tokens[isent]:
                for ref, category in self.referents.items():
                    if self.compiled_referents[ref].match(token[0].lower()):
                        candidates = self.find_candidates(tokens, iprev_sents,
                                                          category, rp)
                        ncandidates += len(candidates)
        return ncandidates / (len(tokens) - 1) if len(tokens) - 1 else 0


class AnaphoricReferencesBaseList(base.Metric):
    """Docstring for AnaphoricReferencesBase. """

    referents = {r'^elas$': 'fp',
                 r'^nelas$': 'fp',
                 r'^delas$': 'fp',
                 r'^.*-nas$': 'fp',
                 r'^.*-las$': 'fp',
                 r'^.*-as$': 'fp',
                 r'^eles$': 'mp',
                 r'^neles$': 'mp',
                 r'^deles$': 'mp',
                 r'^.*-nos$': 'mp',
                 r'^.*-los$': 'mp',
                 r'^.*-os$': 'mp',
                 r'^ela$': 'fs',
                 r'^nela$': 'fs',
                 r'^dela$': 'fs',
                 r'^.*-na$': 'fs',
                 r'^.*-la$': 'fs',
                 r'^.*-a$': 'fs',
                 r'^ele$': 'ms',
                 r'^nele$': 'ms',
                 r'^dele$': 'ms',
                 r'^.*-no$': 'ms',
                 r'^.*-lo$': 'ms',
                 r'^.*-o$': 'ms',
                 r'^lhes$': 'ap',
                 r'^lhe$': 'as',
                 }

    def __init__(self, nsentences=1):
        """Form an AnaphoricReferencesBase object.

        :nsentences: the number of sentences to look back for anaphoric
            references.
        """

        super(AnaphoricReferencesBaseList, self).__init__()

        self.nsentences = nsentences

        self.compiled_referents = {}
        for regex, category in self.referents.items():
            self.compiled_referents[regex] = re.compile(regex)

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.tagged_sentences(t)
        prefix = ''
        sufix = ''
        points = [',', '.', '!', '?', ':', ';']

        candidates = []

        self.computed_categories = {}
        iterator = iter(range(len(tokens)))
        for i in iterator:
            iterator2 = iter(range(len(tokens[i])))
            for j in iterator2:
                for ref, category in self.referents.items():
                    if self.compiled_referents[ref].match(tokens[i][j][0].lower()):
                        if j - 1 >= 0:
                            prefix = tokens[i][j - 1][0]

                        if j + 1 < len(tokens[i]):
                            sufix = ' ' + tokens[i][j + 1][0]

                        for point in points:
                            if point in sufix:
                                if len(sufix.strip()) == 1:
                                    sufix = sufix.strip() + ' '
                                else:
                                    sufix = sufix + ' '
                                break

                        value = prefix + ' ' + tokens[i][j][0] + sufix

                        candidates.append(value)

                        prefix = ''
                        sufix = ''

        return candidates


class AdjacentAnaphoricReferences(AnaphoricReferencesBase):
    """
        **Nome da Métrica**: adjacent_refs

        **Interpretação**: quanto maior a métrica, maior a complexidade textual

        **Descrição da métrica**: Média de candidatos a referente, na sentença anterior, por pronome anafórico

        **Definição dos termos que aparecem na descrição da métrica**: pronomes anafóricos são aqueles que retomam um
        referente que ocorreu antes no texto. No caso desta métrica, o referente do pronome anafórico é procurado na
        sentença adjacente anterior. Usa-se uma lista de pronomes, com suas respectivas etiquetas de gênero e número,
        para identificar os pronomes anafóricos.

        **Forma de cálculo da métrica**: Identificam-se os pronomes de uma sentença, usando uma lista de pronomes (e
        não POS tagger). Para cada pronome, procuram-se, na sentença anterior, substantivos candidatos a referente que
        tenham o mesmo gênero (masculino ou feminino) e o mesmo número (singular ou plural). Somam-se os candidatos e
        divide-se o resultado pelo número de pronomes anafóricos identificados, a fim de obter a média de candidatos
        por pronome. Apenas os substantivos constantes do léxico DELAF são considerados.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, para identificar os substantivos e DELAF – léxico de
        formas do português, para identificar gênero (masculino, feminino ou comum de dois gêneros) e número (singular
        ou plural). São 6 as combinações possíveis para gênero e número dos substantivos no DELAF: ms, mp, fs, fp, as,
        ap (m=masculino, f=feminino, a=comum de dois gêneros, s=singular e p=plural).

        **Limitações da métrica**: se o referente for um substantivo que não está no DELAF ou se tiver gênero e número
        diferente do pronome anafórico, não será identificado.

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As principais propostas apresentadas na última convenção do partido foram feitas pelas mulheres.
        Elas estão engajadas na missão de reformar o estatuto até o final do ano. Mas muitos integrantes do partido não
        querem que ele seja reformado.

        **Contagens**: 2 pronomes anafóricos: “elas” tem 2 candidatos a referente na sentença anterior (propostas,
        mulheres) e “ele” tem 3 candidatos a referente na sentença anterior (estatuto, final, ano).

        **Resultado Esperado**: 5/2 = 2,5

        **Resultado Obtido**: 2,5

        **Status**: correto
    """

    name = 'Ratio of candidates to anaphoric reference in adjacente sentences'
    column_name = 'adjacent_refs'

    def __init__(self):
        super(AdjacentAnaphoricReferences, self).__init__(nsentences=1)


class AnaphoricReferences(AnaphoricReferencesBase):
    """
        **Nome da Métrica**: anaphoric_refs

        **Interpretação**: quanto maior a métrica, maior a complexidade textual

        **Descrição da métrica**: Média de candidatos a referente, em até 5 sentenças anteriores, por pronome anafórico

        **Definição dos termos que aparecem na descrição da métrica**: pronomes anafóricos são aqueles que retomam um
        referente que ocorreu antes no texto. No caso desta métrica, o referente do pronome anafórico é procurado em
        até 5 sentenças anteriores. Usa-se uma lista de pronomes, com suas respectivas etiquetas de gênero e número,
        para identificar os pronomes anafóricos.

        **Forma de cálculo da métrica**: Identificam-se os pronomes de uma sentença, usando uma lista de pronomes (e
        não POS tagger). Para cada pronome, procuram-se, nas 5 sentenças anteriores, substantivos candidatos a referente
        que tenham o mesmo gênero (masculino ou feminino) e o mesmo número (singular ou plural). Somam-se os candidatos
        e divide-se o resultado pelo número de pronomes anafóricos identificados, a fim de obter a média de candidatos
        por pronome. Apenas os substantivos constantes do léxico DELAF são considerados.

        **Recursos de PLN utilizados durante o cálculo**: DELAF – léxico de formas do português

        **Limitações da métrica**: A métrica não elimina os candidatos a referentes repetidos. No exemplo do teste, por
        exemplo, as palavras “alunos”, “professores”, “trabalhos” e “relatórios” foram contados duas vezes para o
        segundo “eles”.

        **Crítica**: o ideal seria eliminar candidatos redundantes

        **Projeto**: Coh-Metrix-Port

        **Teste**: Os professores recomendaram aos alunos que fizessem seus trabalhos de conclusão de curso com muita
        dedicação. Eles também lhes recomendaram que não deixassem os relatórios finais para serem escritos na última
        hora. São recomendações importantes, porque todos os anos os alunos pedem prorrogação dos prazos de entrega dos
        trabalhos e acabam entregando relatórios escritos às pressas e cheios de erros de português. Eles têm
        dificuldade em se planejar com antecedência.

        **Contagens**: 4 sentenças, 3 pronomes (eles, eles, lhes), 17 candidatos: 3 para o primeiro “eles” (professores,
        alunos, trabalhos); 3 para o “lhes” (professores, alunos, trabalhos); 11 para o segundo “eles” (todos, anos,
        erros, relatórios, trabalhos, prazos, alunos, relatórios, trabalhos, alunos, professores)

        **Resultado Esperado**: 15/3 = 5,667

        **Resultado Obtido**: 5,667

        **Status**: correto
    """

    name = 'Ratio of candidates to anaphoric reference in five previous sentences'
    column_name = 'anaphoric_refs'

    def __init__(self):
        super(AnaphoricReferences, self).__init__(nsentences=5)


class Anaphoras(base.Category):
    """"""

    name = 'Anaphoras'
    table_name = 'anaphoras'

    def __init__(self):
        super(Anaphoras, self).__init__()
        self.metrics = [AdjacentAnaphoricReferences(),
                        AnaphoricReferences(), ]
        self.metrics.sort(key=lambda m: m.name)
