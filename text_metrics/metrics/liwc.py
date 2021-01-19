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
from text_metrics.conf import config
import codecs
import re
from itertools import chain


def count_regex_matches(strings, regexes):
    """
    Count how many `strings` are matched by any of the `regexes`.

    :param strings: List of strings to be matched.
    :param regexes: List of regexes to match `strings` with.
    :rtype: int.
    """
    #return sum(1 for s in strings
    #             if any(re.fullmatch(r, s) for r in regexes))
    all = ""
    for s in strings:
        all += s + "|"
    ret = 0
    for r in regexes:
        matches = re.findall(r, all)
        ret += len(matches)

    return ret


class PositiveWords(base.Metric):
    """
        **Nome da Métrica**: positive_words

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção de palavras com polaridade positiva em relação a todas as palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: polaridade positiva é uma característica
        psicolinguística das palavras de conteúdo

        **Forma de cálculo da métrica**: identificam-se todas as palavras do texto que estão na lista de palavras com
        polaridade positiva no dicionário do LIWC; calcula-se a quantidade dessas palavras e divide-se o resultado pela
        quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: lista de palavras positivas do dicionário LWIC

        **Limitações da métrica**:

        **Crítica**: como apenas palavras de conteúdo possuem polaridade, deveria haver uma pré-seleção das palavras
        de conteúdo antes de consultar a lista de palavras positivas. A divisão do resultado deveria ser pela quantidade
        de palavras de conteúdo.

        **Projeto**: Coh-Metrix-Dementia

        **Teste**: Embora o celular seja lento, sua bateria é muito boa.

        **Contagens**: 10 palavras, 2 palavras de polaridade positiva (muito e boa),

        **Resultado Esperado**: 0,20

        **Resultado Obtido**: 0,20

        **Status**: correto
    """

    name = 'Ratio of Positive Words of LIWC Dictionary'
    column_name = 'positive_words'

    def value_for_text(self, t, rp=default_rp):
        pos = rp.positive_words()
        words = list(chain.from_iterable(rp.content_words(t)))
        return count_regex_matches(words, pos) / len(words)


class NegativeWords(base.Metric):
    """
        **Nome da Métrica**: negative_words

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção de palavras com polaridade negativa em relação a todas as palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: polaridade negativa é uma característica
        psicolinguística das palavras de conteúdo

        **Forma de cálculo da métrica**: identificam-se todas as palavras do texto que estão na lista de palavras com
        polaridade negativa do dicionário do LIWC; calcula-se a quantidade dessas palavras e divide-se o resultado pela
        quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: lista de palavras negativas do dicionário LWIC

        **Limitações da métrica**:

        **Crítica**: como apenas palavras de conteúdo possuem polaridade, deveria haver uma pré-seleção das palavras de
        conteúdo antes de consultar a lista de palavras negativas. A divisão do resultado deveria ser pela quantidade
        de palavras de conteúdo.

        **Projeto**: Coh-Metrix-Dementia

        **Teste**: Embora o celular seja lento, sua bateria é muito boa.

        **Contagens**: 10 palavras, 2 palavras de polaridade negativa (lento),

        **Resultado Esperado**: 0,10

        **Resultado Obtido**: 0,10

        **Status**: correto
    """

    name = 'Ratio of Negative Words of LIWC Dictionary'
    column_name = 'negative_words'

    def value_for_text(self, t, rp=default_rp):
        neg = rp.negative_words()
        words = list(chain.from_iterable(rp.content_words(t)))
        return count_regex_matches(words, neg) / len(words)


class LIWC(base.Category):
    name = 'LIWC'
    table_name = 'liwc'

    def __init__(self):
        super(LIWC, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
