
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
from text_metrics.utils import count_occurrences_for_all


_all_connectives = None


def convert(conn_list):
    """Converts a list of connectives into the format that is accepted by
    utils.count_occurrences and utils.count_occurrences_for_all.
    """

    def conn_to_list(conn):
        return [(word, 'NO_POS') for word in conn.connective.split(' ')]

    return [conn_to_list(conn) for conn in conn_list]


def load_connectives(rp):
    global _all_connectives
    if _all_connectives is None:
        _all_connectives = rp.db_helper().get_all_connectives()


def get_all_conn(rp):
    load_connectives(rp)
    return convert(_all_connectives)


def get_add_pos_conn(rp):
    load_connectives(rp)
    add_pos_conn = [conn for conn in _all_connectives if conn.additive_pos]

    return convert(add_pos_conn)


def get_add_neg_conn(rp):
    load_connectives(rp)
    add_neg_conn = [conn for conn in _all_connectives if conn.additive_neg]

    return convert(add_neg_conn)


def get_tmp_pos_conn(rp):
    load_connectives(rp)
    tmp_pos_conn = [conn for conn in _all_connectives if conn.temporal_pos]

    return convert(tmp_pos_conn)


def get_tmp_neg_conn(rp):
    load_connectives(rp)
    tmp_neg_conn = [conn for conn in _all_connectives if conn.temporal_neg]

    return convert(tmp_neg_conn)


def get_cau_pos_conn(rp):
    load_connectives(rp)
    cau_pos_conn = [conn for conn in _all_connectives if conn.causal_pos]

    return convert(cau_pos_conn)


def get_cau_neg_conn(rp):
    load_connectives(rp)
    cau_neg_conn = [conn for conn in _all_connectives if conn.causal_neg]

    return convert(cau_neg_conn)


def get_log_pos_conn(rp):
    load_connectives(rp)
    log_pos_conn = [conn for conn in _all_connectives if conn.logic_pos]

    return convert(log_pos_conn)


def get_log_neg_conn(rp):
    load_connectives(rp)
    log_neg_conn = [conn for conn in _all_connectives if conn.logic_neg]

    return convert(log_neg_conn)


class ConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: proporção de conectivos em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos são palavras que “ligam” partes do
        discurso, estabelecendo algum tipo de relação discursiva. O termo tem sobreposição com o termo “marcador
        discursivo”.

        **Forma de cálculo da métrica**: contam-se todos os conectivos do texto, usando uma lista de conectivos para
        identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual. A lista de conectivos apresenta
        dois tipos de atributos: função (aditivo, causal, lógico ou temporal) e efeito no evento (conectivos positivos
        estendem eventos, enquanto que conectivos negativos param eventos)

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 6 conectivos (e, e, como, e, se, e), 95 palavras

        **Resultado Esperado**: 6/95 = 0,063

        **Resultado Obtido**: 0,063

        **Status**: correto
    """

    name = 'Connectives Ratio'
    column_name = 'conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_all_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class AddPosConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: add_pos_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos aditivos positivos em relação à quantidade de palavras do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos aditivos positivos são, por exemplo:
        “bem como”, “além disso”, “em vez de”

        **Forma de cálculo da métrica**: contam-se todos os conectivos aditivos positivos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 5 conectivos aditivos positivos (e, e, como, e, e), 95 palavras

        **Resultado Esperado**: 5/95 = 0,053

        **Resultado Obtido**: 0,053

        **Status**: correto
    """

    name = 'Ratio of additive positive connectives'
    column_name = 'add_pos_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class AddNegConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: add_neg_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos aditivos negativos em relação à quantidade de palavras do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos aditivos negativos são, por exemplo:
        “mas”, “porém”, “antes”, “todavia”.

        **Forma de cálculo da métrica**: contam-se todos os conectivos aditivos negativos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual. Os conectivos aditivos
        negativos são, em sua maioria, conjunções adversativas.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Entretanto, foram encontrados vários problemas clássicos.

        **Contagens**: 1 conectivo aditivo negativo (entretanto) e 6 palavras

        **Resultado Esperado**: 1/6 = 0,16

        **Resultado Obtido**: 0,16

        **Status**: correto

    """

    name = 'Ratio of additive negative connectives'
    column_name = 'add_neg_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class TmpPosConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: tmp_pos_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos temporais positivos em relação à quantidade de palavras do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos temporais positivos são, por exemplo:
        “assim”, ”outra vez”, ”imediatamente”

        **Forma de cálculo da métrica**: contam-se todos os conectivos temporais positivos do texto, usando uma lista
        de conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Enquanto isso, mais de 100 pessoas tentaram resolver o problema, o que finalmente começou a dar
        resultados.

        **Contagens**: 2 conectivos temporais (enquanto, finalmente), 17 palavras

        **Resultado Esperado**: 2/17 = 0,118

        **Resultado Obtido**: 0,118

        **Status**: correto
    """

    name = 'Ratio of temporal positive connectives'
    column_name = 'tmp_pos_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class TmpNegConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: tmp_neg_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos temporais negativos em relação à quantidade de palavras do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: só há 1 conectivo temporal negativo na lista de
        conectivos: “até que”

        **Forma de cálculo da métrica**: contam-se todos os conectivos temporais negativos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diversas categorias utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino colou na prova até que a professora descobriu sua artimanha.

        **Contagens**: 1 conectivos temporal negativo (até que), 12 palavras

        **Resultado Esperado**: 1/12 = 0,083

        **Resultado Obtido**: 0,083

        **Status**: correto
    """

    name = 'Ratio of temporal negative connectives'
    column_name = 'tmp_neg_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class CauPosConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: cau_pos_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos causais positivos em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos causais positivos são, por exemplo:
        “habilita”, “para”, “se”, “somente se”, “assim”

        **Forma de cálculo da métrica**: contam-se todos os conectivos causais positivos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino queria ir bem na prova. Para isso, ele resolveu colar.

        **Contagens**: 1 conectivo causal positivo (para isso), 12 palavras

        **Resultado Esperado**: 1/12 = 0,083

        **Resultado Obtido**: 0,083

        **Status**: correto

    """

    name = 'Ratio of causal positive connectives'
    column_name = 'cau_pos_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class CauNegConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: cau_neg_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos causais negativos em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: há 6 conectivos causais negativos na lista de
        conectivos: mesmo embora, contudo, no entanto, apesar de, apesar disso, apesar disto, a menos que.

        **Forma de cálculo da métrica**: contam-se todos os conectivos causais negativos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Embora tenha colado na prova, o menino não obteve uma boa nota.

        **Contagens**: 1 conectivo causal negativo (embora), 12 palavras

        **Resultado Esperado**: 1/12 = 0,083

        **Resultado Obtido**: 0,083

        **Status**: correto
    """

    name = 'Ratio of causal negative connectives'
    column_name = 'cau_neg_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class LogPosConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: log_pos_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: Proporção de conectivos lógicos positivos em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos lógicos positivos são, por exemplo:
        similarmente, por outro lado, de novo, somente se, assim, para este fim.

        **Forma de cálculo da métrica**: contam-se todos os conectivos lógicos positivos do texto, usando uma lista de
        conectivos para identificá-los, e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Vários deles estão em mais de uma categoria e alguns não são conjunções nem locuções adverbiais
        clássicos. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Desde que o menino começou a colar nas provas, ele não estuda mais.

        **Contagens**: 1 conectivo lógico positivo (desde que), 13 palavras

        **Resultado Esperado**: 1/13 = 0,076

        **Resultado Obtido**: 0,076

        **Status**: correto
    """

    name = 'Ratio of logical positive connectives'
    column_name = 'log_pos_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class LogNegConnectivesRatio(base.Metric):
    """
        **Nome da Métrica**: log_neg_conn_ratio

        **Interpretação**: não está clara a relação entre proporção de conectivos e complexidade textual

        **Descrição da métrica**: proporção de conectivos lógicos negativos em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: conectivos lógicos negativos são, por exemplo:
        pelo contrário, ainda, cada vez que, embora.

        **Forma de cálculo da métrica**: contam-se todos os conectivos lógicos negativos do texto, usando uma lista de
        conectivos para identificá-los e divide-se o resultado pela quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: lista de conectivos

        **Limitações da métrica**: por usar uma lista de palavras, pode haver imprecisão, pois uma mesma palavra pode
        funcionar como conectivo em alguns contextos e não em outros

        **Crítica**: os conectivos são palavras funcionais de diferentes categorias, utilizados para análise das funções
        discursivas. Não está clara sua utilidade para aferição de complexidade textual.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino colou na prova, embora soubesse que poderia ser pego.

        **Contagens**: 1 conectivo lógico negativo (embora), 11 palavras

        **Resultado Esperado**: 1/11 = 0,090

        **Resultado Obtido**: 0,090

        **Status**: correto

    """

    name = 'Ratio of logical negative connectives'
    column_name = 'log_neg_conn_ratio'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class Connectives(base.Category):
    """"""

    name = 'Connectives'
    table_name = 'connectives'

    def __init__(self):
        super(Connectives, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
