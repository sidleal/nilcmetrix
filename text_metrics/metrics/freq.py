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
from text_metrics import base
from text_metrics.resource_pool import rp as default_rp
from itertools import chain


class ContentWordsFrequency(base.Metric):
    """
        **Nome da Métrica**: cw_freq

        **Interpretação**: teoricamente, quanto maior a frequência das palavras, menor a complexidade do texto

        **Descrição da métrica**: Média das frequências absolutas das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: frequência absoluta é a quantidade de vezes que
        uma palavra ocorre em um corpus, portanto, varia em função do tamanho do corpus; palavras de conteúdo são
        substantivos, verbos, adjetivos e advérbios.

        **Forma de cálculo da métrica**: identificam-se todas as palavras de conteúdo no texto. Para cada uma delas,
        procura-se a frequência na lista de frequências do Corpus Brasileiro. Somam-se todas as frequências e divide-se
        o resultado pela quantidade de palavras de conteúdo do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet e lista de frequências do Corpus Brasileiro

        **Limitações da métrica**:

        **Crítica**:

        O Corpus Brasileiro possui muitos vieses devido ao desbalanceamento de suas fontes de textos, portanto, suas
        frequências não são um bom reflexo das frequências de palavras na língua geral.

        As formas do corpus não possuem classe gramatical e somam ocorrências de classes diferentes que possuem a mesma
        grafia (ex: “forma” – substantivo e “forma” – 3ª pessoa do singular do presente do indicativo do verbo formar).
        Por isso, ao se buscar uma palavra de conteúdo na lista de frequências, nem sempre se encontra apenas a
        frequência da palavra na categoria gramatical almejada.

        A formatação do resultado está incorreta

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
        proposta.

        **Contagens**: palavras de conteúdo: acessório, utilizado, adolescentes, boné, é, itens, compõem, vestimenta,
        idealizada, proposta. Frequências respectivas: 1.616, 78.716, 53.937, 1.615, 5.325.656, 32.350, 17.961, 773,
        1.908, 135.451.

        **Resultado Esperado**: 5.649.983

        **Resultado Obtido**: 564998.3

        **Status**: correto
    """

    name = 'Mean content words frequency'
    column_name = 'cw_freq'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.cw_freq(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumContentWordsFrequency(base.Metric):
    """
        **Nome da Métrica**: min_cw_freq

        **Interpretação**: teoricamente, quanto maior a frequência, menor a complexidade da palavra

        **Descrição da métrica**: Média das frequências absolutas das palavras de conteúdo mais raras das sentenças do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: frequência absoluta é a quantidade de vezes que
        uma palavra ocorre em um corpus, portanto, varia em função do tamanho do corpus; palavras de conteúdo são substantivos, verbos, adjetivos e advérbios; as palavras mais raras são as que têm a menor frequência em comparação com as outras palavras de conteúdo de cada sentença.

        **Forma de cálculo da métrica**: identificam-se todas as palavras de conteúdo no texto. Para cada uma delas,
        procura-se a frequência na lista de frequências do Corpus Brasileiro. Identificam-se as palavras que apresentam
        a menor frequência entre as palavras de conteúdo de cada sentença. Somam-se essas frequências mínimas e
        divide-se o resultado pela quantidade de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet e lista de frequências do Corpus Brasileiro

        **Limitações da métrica**:

        O Corpus Brasileiro possui muitos vieses devido ao desbalanceamento de suas fontes de textos, portanto, suas
        frequências não são um bom reflexo das frequências de palavras na língua geral.

        A lista de palavras do corpus não traz categorias gramaticais e junta as frequências de formas homônimas, como
        por exemplo, o "a" artigo, o "a" preposição e o "a" pronome ou o pronome “sua” com a forma verbal “sua” (3ª
        pessoa do singular do presente do indicativo do verbo “suar”). Por isso, ao se buscar uma palavra de conteúdo
        na lista de frequências, nem sempre se encontra apenas a frequência da palavra na categoria gramatical almejada. 

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste 1**: A Casa tem em torno de 160 contratos para serem analisados.

        **Contagens**:
            palavras de conteúdo: 'Casa', 'tem', 'contratos', 'serem', 'analisados'
            frequências: [350476, 899042, 32471, 94817, 29643], respectivamente.
            frequência mínima: 29643

        **Resultado Esperado**: 29643.0 (29643/1)

        **Resultado Obtido**: 29643 (a palavra que tem menor frequência tem 29643 ocorrências)

        **Status**: correto

        **Teste 2**: Os partidos estão mais cautelosos.

        **Contagens**:
            palavras de conteúdo: 'partidos', 'estão', 'mais', 'cautelosos'
            Frequências [55099, 390250, 2326660, 635], respectivamente.
            Frequência mínima 635

        **Resultado Esperado**: 635 (635/1)

        **Resultado Obtido**: 635

        **Status**: correto
    """

    name = 'Mean minimum among content words frequencies'
    column_name = 'min_cw_freq'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.cw_freq(t)
        # TODO: Check the len(f) > 0 (not a problem in Python 3!)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class ContentWordsFrequencyBrWaC(base.Metric):
    """"""
    name = 'Mean content words frequency in brWaC'
    column_name = 'cw_freq_brwac'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.cw_freq_brwac(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumContentWordsFrequencyBrWaC(base.Metric):
    """"""
    name = 'Mean minimum among content words frequencies in brWaC'
    column_name = 'min_cw_freq_brwac'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.cw_freq_brwac(t)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class WordsFrequencyBrWaC(base.Metric):
    """"""
    name = 'Mean words frequency in brWaC'
    column_name = 'freq_brwac'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.freq_brwac(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumWordsFrequencyBrWaC(base.Metric):
    """"""
    name = 'Mean minimum among content words frequencies in brWaC'
    column_name = 'min_freq_brwac'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.freq_brwac(t)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class ContentWordsFrequencyBrasileiro(base.Metric):
    """"""
    name = 'Mean content words frequency in corpus Brasileiro'
    column_name = 'cw_freq_bra'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.cw_freq_brasileiro(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumContentWordsFrequencyBrasileiro(base.Metric):
    """"""
    name = 'Mean minimum among content words frequencies in corpus Brasileiro'
    column_name = 'min_cw_freq_bra'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.cw_freq_brasileiro(t)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class WordsFrequencyBrasileiro(base.Metric):
    """"""
    name = 'Mean words frequency in corpus Brasileiro'
    column_name = 'freq_bra'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.freq_brasileiro(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumWordsFrequencyBrasileiro(base.Metric):
    """"""
    name = 'Mean minimum among content words frequencies in corpus Brasileiro'
    column_name = 'min_freq_bra'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.freq_brasileiro(t)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class Frequencies(base.Category):
    """"""

    name = 'Content word frequencies'
    table_name = 'cw_frequencies'

    def __init__(self):
        super(Frequencies, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Frequencies, self).values_for_text(t, rp)
