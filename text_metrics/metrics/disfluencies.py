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
import idd3
from text_metrics import base
from text_metrics.resource_pool import rp as default_rp


class MeanPauseDuration(base.Metric):
    """
        ## Duração média das pausas

        Duração total das pausas dividida pelo número total de palavras.
        Pausas são marcadas como ((pausa XX segundos)).

        ### Exemplo:

        *uma moça está agradando um cavalo ... ((pausa 14 segundos)) essa
        moça vai à festa ((pausa 8 segundos)) a mocinha está limpando a
        parede ... ((pausa 12 segundos)) ... ela ficou brava .. ((pausa
        5 segundos))*

        Nesse caso, há um total de 14 + 8 + 12 + 5 = 39s de pausa, e 20
        palavras, correspondendo a uma duração média de pausas de 39/20 =
        1,95.
    """

    name = 'Mean pause duration'
    column_name = 'mean_pause'

    pause_pattern = re.compile(r'\(\(pausa\s+(\d+)\s*\w*\)\)')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        pauses = [int(duration)
                  for duration in self.pause_pattern.findall(content)]

        return sum(pauses) / len(words) if words else 0


class MeanShortPauses(base.Metric):
    """
        ## Duração média das pausas curtas

        Número de pausas curtas dividido pelo número total de palavras.
        Pausas curtas são indicadas por três pontos (...).

        ### Exemplo:

        *uma moça está agradando um cavalo ... ((pausa 14 segundos)) essa
        moça vai à festa ((pausa 8 segundos)) a mocinha está limpando a
        parede ... ((pausa 12 segundos)) ... ela ficou brava .. ((pausa
        5 segundos))*

        No exemplo, há 4 pausas curtas e 20 palavras, resultando num valor
        de 4/20 = 0,2.
    """

    name = "Mean number of short pauses"
    column_name = 'mean_short_pauses'

    short_pause_pattern = re.compile(r'\.\.\.')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        pauses = self.short_pause_pattern.findall(content)

        return len(pauses) / len(words) if words else 0


class MeanVowelStretchings(base.Metric):
    """
        ## Número médio de prolongamentos de vogais

        Número de prolongamentos de vogais dividido pelo
        total de palavras. Prolongamentos de vogais são
        marcados com dois dois-pontos (::).

        ### Exemplo:

        *É:: colocou-a:: trancada no quarto...((pausa 5 segundos))
        então aquele moço que::...fez uma festa trouxe o sapato
        para acertar no pé pé de outro não deu certo ... ((pausa 17
        segundos)) e:: ... ((pausa 8 segundos)) esse moço trouxe
        um sapato para ela serviu...((pausa 4 segundos))*

        O fragmento de exemplo possui 4 marcações de prolongamentos
        de vogais, e 34 palavras, produzindo um valor de métrica de
        4/34 = 0,12.
    """

    name = 'Mean number of vowel stretchings'
    column_name = 'mean_vowel'

    stretching_pattern = re.compile(r'::+')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        stretchings = self.stretching_pattern.findall(content)

        return len(stretchings) / len(words) if words else 0


class MeanEmpty(base.Metric):
    """
        ## Número médio de palavras vazias

        Número de palavras em emissões vazias dividido pelo total de palavras
        (inclusas as emissões vazias). Emissões vazias são marcadas com
        <empty> e </empty>.

        ### Exemplo:

        *uma moça está agradando um cavalo ... <empty>mais?</empty> ...
        essa moça vai à festa ((pausa 8 segundos)) a mocinha está limpando a
        parede ... <empty>como que fala esse</empty> ... filha do:: ...
        <empty>como que é</empty> ... ((pausa 5 segundos)) sogro e fala
        <empty>será?</empty> ficou brava*

        No exemplo, há 1 + 4 + 3 + 1 = 9 palavras em emissões vazias, e um total
        de 33 palavras, correspondendo a um valor de métrica de 9/33 = 0,27.
    """

    name = "Mean number of empty words"
    column_name = 'mean_empty'

    def value_for_text(self, t, rp=default_rp):
        if 'empty' not in t.meta:
            return 0

        words = rp.raw_words(t)

        empty_length = []
        for e in t.meta['empty']:
            text = re.sub(r"\.\.\.", ' ', e.text, re.U)
            text = re.sub(r'::', ' ', text, re.U)

            empty_words = [w for w in text.split(' ') if w]
            empty_length.append(len(empty_words))

        return sum(empty_length) / len(words) if words else 0


class MeanDisf(base.Metric):
    """
        ## Número médio de disfluências

        Número de palavras em emissões disfluentes dividido pelo total de
        palavras (inclusas as disfluências). Disfluências são marcadas com
        <disf> e </disf>.

        ### Exemplo:

        *aí ela ficou triste foi no jardim e <disf>a:: a::</disf> estava
        triste ... ((pausa 8 segundos)) ai ... ficou na rua encontrou ...
        e mediu mediu a:: ... <disf>fa</disf> fez o vestido novo esse aqui*

        No fragmento, há 2 + 1 = 3 palavras em emissões disfluentes, e um
        total de 28 palavras, e o valor correspondente da métrica é 3/28 =
        0,11.
    """

    name = "Mean number of disfluent words"
    column_name = 'mean_disf'

    def value_for_text(self, t, rp=default_rp):
        if 'disf' not in t.meta:
            return 0

        words = rp.raw_words(t)

        disf_length = []
        for e in t.meta['disf']:
            text = re.sub(r"\.\.\.", ' ', e.text, re.U)
            text = re.sub(r'::', ' ', text, re.U)

            disf_words = [w for w in text.split(' ') if w]
            print(disf_words)
            disf_length.append(len(disf_words))

        return sum(disf_length) / len(words) if words else 0


class Repetition(base.Metric):
    """
        ## Número médio de palavras repetidas

        Número de palavras repetidas dividido pelo total de palavras
        (incluindo-se as repetidas). Palavras são consideradas repetidas
        apenas quando aparecem em sequência. Por exemplo, em *Maria foi foi
        ao mercado*, é contada uma repetição da palavra __foi__, mas em *Maria
        foi ao mercado, e então foi à padaria*, não é contada repetição de
        __foi__, pois ambas não ocorrem em sequência.

        Não são contadas repetições no interior de emissões disfluentes.

        ### Exemplo:

        *aí ela ficou triste foi no jardim e <disf>a:: a::</disf> estava
        triste ... ((pausa 8 segundos)) ai ... ficou na rua encontrou ...
        e mediu mediu a:: ... <disf>fa</disf> fez o vestido novo esse aqui*

        No exemplo, houve 1 repetição da palavra __mediu__, e 28 palavras,
        correspondendo a um valor de métrica de 1/28 = 0,036.
    """

    name = "Ratio of repeated words"
    column_name = 'repetition'

    def value_for_text(self, t, rp=default_rp):
        raw_words = rp.raw_words(t)

        n_repeated_words = 0
        i = 0
        while i < len(raw_words):
            run_length = 0
            for j in range(i + 1, len(raw_words)):
                if raw_words[j] == raw_words[i]:
                    run_length += 1
                else:
                    break
            n_repeated_words += run_length

            i += run_length + 1

        return n_repeated_words / len(raw_words) if raw_words else 0


class TotalIdeaDensity(base.Metric):
    """
        ## Densidade de ideias total

        Número de proposições presentes no texto, para cada dez palavras.
        Para o cálculo das proposições, não são levadas em conta proposições
        vazias ou disfluentes, e o cálculo é feito sobre o texto revisado,
        para melhor desempenho da ferramenta de extração.

        A extração de proposições encontra-se descrita em:

        CUNHA, A.; SOUSA, L. Bender de; MANSUR, L.; ALUISIO, S. Automatic
        proposition extraction from dependency trees: Helping early prediction
        of alzheimer’s disease from narratives. In: __Computer-Based Medical
        Systems (CBMS), 2015 IEEE 28th International Symposium on
        Computer-Based Medical Systems__, 2015. p. 127–130.

        ### Exemplo:

        *uma moça está agradando um cavalo ... ((pausa 14 segundos)) essa
        moça vai à festa ((pausa 8 segundos)) a mocinha está limpando a
        parede ... ((pausa 12 segundos)) ... ela ficou brava .. ((pausa
        5 segundos))*

        No texto, as proposições presentes são:

        1. está agradando, uma moça, um cavalo
        2. vai, essa moça
        3. à festa
        4. está limpando, a mocinha, a parede
        5. ficou brava, ela

        Portanto, há 5 proposições para 20 palavras, totalizando um valor
        de densidade de ideias de 4 / 20 * 10 = 2,0.
    """

    name = 'Total Idea Density'
    column_name = 'total_id'

    def value_for_text(self, t, rp=default_rp):
        engine = rp.idd3_engine()
        graphs = rp.dep_trees(t)
        raw_words = rp.raw_words(t)

        total_nprops = 0
        for index in range(len(graphs)):
            relations = []
            for relation in graphs[index].nodes.values():
                relations.append(idd3.Relation(**relation))

            # print('Propositions:')
            try:
                engine.analyze(relations)
                # for i, prop in enumerate(engine.props):
                #     print(str(i + 1) + ' ' + str(prop))

                n_props = len(engine.props)
            except Exception as e:
                n_props = 0

            # print(len(sents[index]), n_props / len(sents[index]) )
            total_nprops += n_props

        return total_nprops / len(raw_words) if raw_words else 0


class Disfluencies(base.Category):
    name = 'Disfluencies'
    table_name = 'disfluencies'

    def __init__(self):
        super(Disfluencies, self).__init__()
        self._set_metrics_from_module(__name__)
