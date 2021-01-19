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
from text_metrics.utils import base_path, count_occurrences, count_occurrences_for_all


class LogicOperatorsRatio(base.Metric):
    """
    ## Proporção de Operadores Lógicos em relação à quantidade de palavras do texto

    **Identificador da métrica:** logic_operators

    **Interpretação:** não está clara a relação entre a métrica e a complexidade textual

    **Descrição da métrica:** Proporção de Operadores Lógicos em relação à quantidade de palavras do texto

    **Definição dos termos que aparecem na descrição da métrica:** operadores lógicos são palavras que estabelecem relações lógicas no texto, como por exemplo: ou, e, se, não.

    **Forma de cálculo da métrica:** contam-se as palavras do texto que correspondam ao léxico de operadores lógicos, depois divide-se o resultado pela quantidade de palavras do texto

    **Recursos de PLN utilizados durante o cálculo:** 

    **Limitações da métrica:**  

    **Crítica:** 

    **Origem:** CMP

    **Teste:** Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora do Departamento Pedagógico da SEC, Sonia Balzano.

    **Contagens:** 38 palavras, 4 operadores lógicos (não, nenhuma, e, não)

    **Resultado Esperado:** 4/38 = 0,105

    **Resultado Obtido:** 0,105

    **Status:** correto
    """

    name = 'Logic operators Ratio'
    column_name = 'logic_operators'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        logic_operators = rp.pos_tagger().tagset.LOGIC_OPERATORS
        occurrences = [count_occurrences_for_all(sent, logic_operators,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class AndRatio(base.Metric):
    """
        **Nome da Métrica**: and_ratio

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção do  Operador Lógico “E” em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: operadores lógicos são palavras que estabelecem
        relações lógicas no texto, como por exemplo: ou, e, se, não.

        **Forma de cálculo da métrica**: contam-se as ocorrências de “E” no texto e depois divide-se o resultado pela
        quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora
        do Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 38 palavras, 1 operador lógico E

        **Resultado Esperado**: 1/38 = 0,026

        **Resultado Obtido**: 0,026

        **Status**: correto

    """

    name = 'Ratio of ANDs'
    column_name = 'and_ratio'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _and = rp.pos_tagger().tagset.AND
        occurrences = [count_occurrences(sent, _and, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class OrRatio(base.Metric):
    """
        **Nome da Métrica**: or_ratio

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção do Operador Lógico “OU” em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: operadores lógicos são palavras que estabelecem
        relações lógicas no texto, como por exemplo: ou, e, se, não.

        **Forma de cálculo da métrica**: contam-se as ocorrências de “OU” no texto e depois divide-se o resultado pela
        quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Ou ele ou você terá que resolver esse problema.

        **Contagens**: 9 palavras, 2 operadores lógicos OU

        **Resultado Esperado**: 2/9 = 0,222

        **Resultado Obtido**: 0,222

        **Status**: correto
    """

    name = 'Ratio of ORs'
    column_name = 'or_ratio'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _or = rp.pos_tagger().tagset.OR
        occurrences = [count_occurrences(sent, _or, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class IfRatio(base.Metric):
    """
        **Nome da Métrica**: if_ratio

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção do Operador Lógico “SE” em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: operadores lógicos são palavras que estabelecem
        relações lógicas no texto, como por exemplo: ou, e, se, não.

        **Forma de cálculo da métrica**: contam-se as ocorrências de “SE” no texto e depois divide-se o resultado pela
        quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Se você vier me ver esta noite, por favor traga o livro que lhe pedi.

        **Contagens**: 15 palavras, 1 operador lógico SE

        **Resultado Esperado**: 1/15 = 0,066

        **Resultado Obtido**: 0,066

        **Status**: correto

    """

    name = 'Ratio of IFs'
    column_name = 'if_ratio'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _if = rp.pos_tagger().tagset.IF
        occurrences = [count_occurrences(sent, _if, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class NegationRatio(base.Metric):
    """
        **Nome da Métrica**: negation_ratio

        **Interpretação**: a negação é mais complexa que a afirmação, portanto, quanto maior a métrica, maior a
        complexidade textual

        **Descrição da métrica**: proporção de palavras que denotam negação em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: as palavras que denotam negação para fins desta
        métrica são: não, nem, nunca, tampouco, jamais (sempre que forem ADV).

        **Forma de cálculo da métrica**: contam-se as ocorrências de palavras de negação no texto e divide-se o
        resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet.

        **Limitações da métrica**: a precisão da métrica depende do desempenho do nlpnet.

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: É importante que as refeições sejam equilibradas, não forneçam nem mais e nem menos daquilo que o
        nosso corpo precisa.

        **Contagens**: 20 palavras, 3 negações (não, nem, nem)

        **Resultado Esperado**: 3/20 = 0,15

        **Resultado Obtido**: 0,15

        **Status**: correto
    """

    name = 'Ratio of negations'
    column_name = 'negation_ratio'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        negations = rp.pos_tagger().tagset.NEGATIONS
        occurrences = [count_occurrences_for_all(sent, negations,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class LogicOperators(base.Category):
    """
        **Nome da Métrica**: logic_operators

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção de Operadores Lógicos em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: operadores lógicos são palavras que estabelecem
        relações lógicas no texto, como por exemplo: ou, e, se, não.

        **Forma de cálculo da métrica**: contam-se as palavras do texto que correspondam ao léxico de operadores
        lógicos, depois divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora
        do Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 38 palavras, 4 operadores lógicos (não, nenhuma, não, e)

        **Resultado Esperado**: 4/38 = 0,105

        **Resultado Obtido**: 0,105

        **Status**: correto
    """

    name = 'Logic operators'
    table_name = 'logic_operators'

    def __init__(self):
        super(LogicOperators, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp, ignore_pos=False):
        metrics_values = base.ResultSet([(m, round(m.value_for_text(t), 5))
                                         for m in self.metrics])
        return metrics_values
