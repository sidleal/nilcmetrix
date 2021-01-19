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
from text_metrics.utils import find_subtrees
from collections import Counter
from math import log


class PersonalPronounsRatio(base.Metric):
    """
        **Nome da Métrica**: personal_pronouns

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção de pronomes pessoais em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados pronomes pessoais: eu, tu, ele,
        ela, você, nós, vós, eles, elas, vocês.

        **Forma de cálculo da métrica**: Divide-se a quantidade de pronomes pessoais pela quantidade de palavras do
        texto.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização Limitações da
        métrica: a métrica não reconhece a forma “a gente”, que é frequente na língua falada em substituição á forma
        “nós”.

        **Crítica**:

        **Projeto**: Coh-Metrix-Dementia

        **Teste**: Eles lotearam carros e a padaria teve um atraso de apenas meia hora na venda dos 2 mil pães.

        **Contagens**: 19 palavras, 1 pronome pessoal (eles)

        **Resultado Esperado**: 0,53

        **Resultado Obtido**: 0,53

        **Status**: correto
    """

    name = 'Personal pronouns Ratio'
    column_name = 'personal_pronouns'

    personal_pronouns = ['eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles',
                         'elas', 'você', 'vocês']

    def __init__(self):
        super(PersonalPronounsRatio, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        words = [word.lower() for word in rp.all_words(t)]
        return rp.mattr_relative(words, self.personal_pronouns)
        #n_personal_pronouns = sum([word in self.personal_pronouns
        #                           for word in words])
        #return n_personal_pronouns / len(words) \
        #    if words else 0


# class PronounsPerNounPhrase(base.Metric):
#     """
#         **Nome da Métrica**: pronouns_per_np
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção média de pronomes por sintagma nominal nas sentenças
#
#         **Definição dos termos que aparecem na descrição da métrica**: NP (noun phrase) é sintagma nominal, um
#         constituinte sintático cujo núcleo é um nome ou pronome pessoal e cujos acessórios são determinantes (artigos,
#         pronomes possessivos, pronomes demonstrativos, numerais) e modificadores (adjetivos).
#
#         **Forma de cálculo da métrica**: contam-se os pronomes de cada sentença e divide-se o resultado pela quantidade
#         de NPs da sentença. Depois somam-se as proporções de todas as sentenças e divide-se o resultado pela quantidade
#         de sentenças.
#
#         **Recursos de PLN utilizados durante o cálculo**: parse trees do LX-Parser
#
#         **Limitações da métrica**: O desempenho desta métrica é diretamente relacionado ao desempenho das árvores
#         sintáticas de constituintes geradas pelo LX-Parser.
#
#         **Crítica**: a forma de cálculo da métrica captura os NPs pais e filhos na árvore sintática. O ideal seria
#         capturar apenas os NPs pais, para não duplicar a contagem de um mesmo conteúdo. No exemplo abaixo, a primeira
#         sentença tem 9 NPs: “o lago”, “peixes”, “a traíra e o dourado”, “a traíra”, “o dourado”, “palometa”, “um tipo
#         de piranha”, “um tipo”, “piranha”. Os 3 que são filhos de outros NPs maiores não deveriam ser contados. Além
#         disso, o pronome da segunda sentença ocorre fora do NP (é um “se” reflexivo, ligado ao VP e não ao NP). Devido
#         ao erro conceitual, esta métrica deve ser comentada.
#
#         **Projeto**: Coh-Metrix Portuguese
#
#         **Teste**: Dentro do lago, existem peixes, como a traíra e o dourado, além da palometa, um tipo de piranha.
#         Ela é uma espécie carnívora que se alimenta de peixes.
#
#         **Contagens**: 9 SN na primeira sentença e nenhum pronome, 5 SN na segunda sentença e 1 pronome
#
#         **Resultado Esperado**: ((0/9) + (1/5)/2 => 0,20/2 = 0,10
#
#         **Resultado Obtido**: 0,10
#
#         **Status**: correto
#     """
#
#     name = 'Mean pronouns per noun phrase'
#     column_name = 'pronouns_per_np'
#
#     def value_for_text(self, t, rp=default_rp):
#         parse_trees = rp.parse_trees(t)
#
#         sent_indices = []
#         for i, tree in enumerate(parse_trees):
#             nps = 0
#             prons = 0
#
#             for np in find_subtrees(tree, 'NP'):
#                 prons += len([tt for tt in np
#                               if tt.label() in ('PRS')])
#                 nps += 1
#
#             if nps != 0:
#                 sent_indices.append(prons / nps)
#
#         return sum(sent_indices) / len(sent_indices) \
#             if sent_indices else 0


class TypeTokenRatio(base.Metric):
    """
        **Nome da Métrica**: ttr (type  token ratio)

        **Interpretação**: quanto maior o valor da métrica, mais complexo o texto

        **Descrição da métrica**: Proporção de palavras sem repetições (types) em relação ao total de palavras com
        repetições (tokens). Não se usa lematização das palavras, ou seja, cada flexão é computada como um type
        diferente.

        **Definição dos termos que aparecem na descrição da métrica**: Types são as palavras que ocorrem em um texto,
        descontando suas repetições. Tokens são todas as palavras que ocorrem em um texto, sem descontar as repetições.

        **Forma de cálculo da métrica**: contam-se todos os types e divide-se pela quantidade de tokens.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador nltk

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 95 palavras, 58 das quais palavras de conteúdo, 57 types (só repete a palavra “senador”).

        **Resultado Esperado**: 78/95=0,821

        **Resultado Obtido**: 0,821 (está computando todos os tokens e não só palavras de conteúdo)

        **Status**: correto
    """

    name = 'Type to token ratio'
    column_name = 'ttr'

    def __init__(self):
        super(TypeTokenRatio, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        # tokens = rp.all_words(t)
        # types = rp.token_types(t)

        # ttr = len(types) / len(tokens) if tokens else 0

        # return ttr
        tokens = [i.lower() for i in rp.all_words(t)]
        return rp.mattr(tokens)


class BrunetIndex(base.Metric):
    """
        **Nome da Métrica**: brunet

        **Interpretação**: Os valores típicos da métrica variam entre 10 e 20, sendo que uma fala mais rica produz
        valores menores (THOMAS et al., 2005).

        **Descrição da métrica**: Estatística de Brunet é uma forma de type/token ratio que é menos sensível ao tamanho
         do texto.

        **Definição dos termos que aparecem na descrição da métrica**: quantidade de types considera palavras sem
        repetições e quantidade de tokens considera palavras com repetições.

        **Forma de cálculo da métrica**: W = N ** (V ** −0.165) quantidade de types elevada à quantidade de tokens
        elevada à constante -0,165.

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Dementia

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 95 tokens e 78 types

        **Resultado Esperado**: 9,199

        **Resultado Obtido**: 9,199

        **Status**: correto
    """

    name = 'Brunet Index'
    column_name = 'brunet'

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.all_words(t)
        types = rp.token_types(t)

        brunet_index = len(tokens) ** len(types) ** -0.165

        return brunet_index


class HoroneStatistic(base.Metric):
    """
        **Nome da Métrica**: honore

        **Interpretação**: quanto mais alto o valor, mais rico o texto é lexicalmente, o que está associado a maior
        complexidade.

        **Descrição da métrica**: Estatística de Honoré

        **Definição dos termos que aparecem na descrição da métrica**: N é o número total de tokens, V_1 é o número de
        palavras do vocabulário que aparecem uma única vez, e V é o número de palavras lexicais. (HONORÉ, 1979; THOMAS
        et al., 2005):

        **Forma de cálculo da métrica**: R = 100 * logN / (1 - (V_1 / V))

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:  Descrição da métrica: Estatística de Horoné

        **Crítica**:

        **Projeto**: Coh-Metrix-Dementia

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: N= 95 tokens, V_1 = 69 hapax legomena, V = 78 types

        **Resultado Esperado**: 100 * log95 / (1-(69/78) => (100 * 1,97772)/ (1- 0,885) => 197,772/0,115 => 1719,756

        **Resultado Obtido**: 1714,027

        **Status**: correto, considerando arredondamentos
    """

    name = 'Honore Statistic'
    column_name = 'honore'

    def value_for_text(self, t, rp=default_rp):
        tokens = [word.lower() for word in rp.all_words(t)]
        types = rp.token_types(t)

        counter = Counter(tokens)
        one_time_tokens = [word for word, count in counter.items()
                           if count == 1]

        honore_index = 100 * log(len(tokens), 10) /\
            (1 - len(one_time_tokens) / len(types))

        return honore_index


# class MeanClauseSentence(base.Metric):
#     """
#         **Nome da Métrica**: mcu
#
#         **Interpretação**: quanto maior a métrica, maior a complexidade textual
#
#         **Descrição da métrica**: média de orações por sentença
#
#         **Definição dos termos que aparecem na descrição da métrica**:
#
#         **Forma de cálculo da métrica**: Contam-se os VPs na árvore de dependências e divide-se pelo número de sentenças.
#
#         **Recursos de PLN utilizados durante o cálculo**: LX-parser
#
#         **Limitações da métrica**: a métrica depende do desempenho do LX-parser
#
#         **Crítica**: Há outra métrica que mede orações por sentença usando o parser Palavras, cuja precisão é maior. Por
#         isso esta métrica deve ser comentada.
#
#         **Projeto**: Coh-Metrix Portuguese
#
#         **Teste**: Tendemos a pensar que os hereges são pessoas que nadam contra a corrente, indivíduos inclinados a
#         desafiar o conhecimento dominante. Às vezes, porém, um herege é apenas um pensador convencional que permanece
#         olhando na mesma direção, ao passo que todos os demais passaram a olhar na direção contrária. Quando, em 1957,
#         John Yudkin aventou pela primeira vez a possibilidade de o açúcar representar um perigo para a saúde pública, a
#         hipótese foi levada a sério, assim como seu proponente. Ao se aposentar, catorze anos depois, tanto a teoria
#         como seu autor haviam sido ridicularizados e marginalizados. Somente agora, postumamente, é que seu trabalho vem
#         sendo reconduzido ao pensamento científico consolidado.
#
#         **Contagens**: 5 sentenças, 17 orações (se “passar” e “permanecer” não forem considerados auxiliares pelo parser,
#         são 19 orações)
#
#         **Resultado Esperado**: 3,4 ou 3,8
#
#         **Resultado Obtido**: 3,75 (provavelmente o sentenciador contou mais de 5 sentenças)
#
#         **Status**: incorreto
#
#     """
#
#     name = 'Mean Clauses per Sentence'
#     column_name = 'mcu'
#
#     def value_for_text(self, t, rp=default_rp):
#         # We estimate the number of clauses by the number of S nodes in
#         # the syntax tree that have a VP node.
#         trees = rp.parse_trees(t)
#
#         clauses = []
#         for tree in trees:
#             n_clauses = 0
#             for subtree in tree.subtrees(lambda t: t.height() >= 3):
#                 if subtree.label() == 'S':
#                     sub_vps = [t for t in subtree if t.label() == 'VP']
#                     n_clauses += len(sub_vps)
#             clauses.append(n_clauses)
#
#         return sum(clauses) / len(clauses)


class Tokens(base.Category):
    name = 'Pronouns, Types, and Tokens'
    table_name = 'tokens'

    def __init__(self):
        super(Tokens, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Tokens, self).values_for_text(t, rp)
