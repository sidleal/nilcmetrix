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
from text_metrics.utils import find_subtrees, ilen

import nltk


# class NounPhraseRatio(base.Metric):
#     """
#         **Nome da Métrica**: np_ratio
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de sintagmas nominais em relação à quantidade de palavras do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: NP (noun phrase) é sintagma nominal, um
#         constituinte sintático cujo núcleo é um nome ou pronome pessoal e cujos acessórios são determinantes (artigos,
#         pronomes possessivos, pronomes demonstrativos, numerais) e modificadores (adjetivos).
#
#         **Forma de cálculo da métrica**: contam-se todos os segmentos etiquetados com “NP” na árvore sintática, mesmo
#         que um NP esteja contido em outro NP. Divide-se o resultado pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: LX-Parser
#
#         **Limitações da métrica**: a precisão da métrica está condicionada ao desempenho do LX-parser.
#
#         **Crítica**: esta métrica foi substituída por outras mais precisas, que computam apenas os NPs que não sejam
#         filhos de outros NPs. Por esse motivo, será comentada no programa.
#
#         **Projeto**: Coh-Metrix Portuguese
#
#         **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
#         proposta.
#
#         **Contagens**: 5 sintagmas nominais reconhecidos (adolescentes, o boné, um dos itens que compõem a vestimenta
#         idealizada pela proposta, a vestimenta idealizada pela proposta, a proposta) e 17 palavras
#
#         **Resultado Esperado**: 5/17 = 0,294
#
#         **Resultado Obtido**: 0,294
#
#         **Status**: correto, embora o primeiro NP não tenha sido reconhecido pelo LX-Parser (Acessório utilizado por
#         adolescentes)
#     """
#
#     name = 'Noun Phrase Ratio'
#     column_name = 'np_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         parse_trees = rp.parse_trees(t)
#         tagged_sents = rp.tagged_sentences(t)
#
#         sent_indices = []
#         for i, tree in enumerate(parse_trees):
#             nps = len(find_subtrees(tree, 'NP'))
#             words = len([word for word in tagged_sents[i]
#                          if not rp.pos_tagger().tagset.is_punctuation(word)])
#
#             if words != 0:
#                 sent_indices.append(nps / words)
#
#         return sum(sent_indices) / len(sent_indices) if sent_indices else 0


class WordsBeforeMainVerb(base.Metric):
    """
        **Nome da Métrica**: words_before_main_verb

        **Interpretação**: quanto maior a métrica, maior a carga de memória exigida e maior a complexidade textual

        **Descrição da métrica**: quantidade média de palavras antes dos verbos principais das orações principais das
        sentenças

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: localiza-se a etiqueta “main_verb” na árvore sintática e contam-se as palavras
        que a precedem. Se não houver “main_verb”, localiza-se o primeiro verbo flexionado da sentença e procede-se à
        contagem de palavras que o precedem.

        **Recursos de PLN utilizados durante o cálculo**: MaltParser e a POS tagger do nlpnet.

        **Limitações da métrica**: o código da métrica, ao invés de identificar verbos nas formas nominais usando
        etiquetas morfossintáticas, usa 4 terminações, insuficientes: ('do', 'ar', 'er', 'ir'). As terminações de
        infinitivo seriam –ar, -er, -ir, -or; as de gerúndio, -ando, -endo, -indo, -ondo e as de particípio regulares
        seriam –ado e –ido, mas há ainda muitas formas irregulares de particípio. Seria muito melhor usar etiquetas
        para isso.

        A contagem de palavras antes do verbo identificado como principal inclui sinais de pontuação.

        **Críticas**:

        **Projeto**: Coh-Metrix-Port

        **Teste 1**:

        O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma emenda
        aprovada na Comissão de Educação do Senado em outubro.

        **Contagens**: 2 orações, 1 principal (entrou) e 1 subordinada adjetiva restritiva reduzida de particípio
        (aprovada); 3 palavras antes da oração principal (o, acessório, polêmico).

        **Resultado Esperado**: 3

        **Resultado Obtido**: 3

        **Status**: correto

        **Teste 2**:

        Se a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 orações, 1 principal (receberão) e 1 subordinada adverbial condicional (aprovada), 1
        subordinada adjetiva explicativa reduzida de particípio (completados); 8 palavras antes da oração principal,
        considerando a vírgula (se, a, ideia, for, aprovada, “,”, os, estudantes).

        **Resultado Esperado**: 8

        **Resultado Obtido**: 8

        **Status**: correto

        **Teste 3**:

        Nas inserções que já circulam, o PMDB ataca as denúncias feitas pela Procuradoria Geral da República (PGR)
        contra o presidente Michel Temer, por conta da Operação Lava Jato, e faz comparações entre a situação econômica
        de hoje e a do governo Dilma Rousseff.

        **Contagens**: 4 orações, 1 subordinada adjetiva restritiva (circulam) e 1 coordenada assindética (ataca), 1
        subordinada adjetiva restritiva reduzida de particípio (aprovada), 1 coordenada sindética (faz). 8 palavras
        antes do primeiro verbo da oração “atacam”, considerando a vírgula (nas, inserções, que, já, circulam, “,”,
        o, PMDB)

        **Resultado Esperado**: 8

        **Resultado Obtido**: 8

        **Status**: correto
    """

    name = 'Mean words before main verb of sentences'
    column_name = 'words_before_main_verb'

    def value_for_text(self, t, rp=default_rp):
        trees = rp.dep_trees(t)
        words = rp.tagged_words_in_sents(t)

        dep_tagset = rp.dep_parser().tagger.tagset
        tagset = rp.pos_tagger().tagset

        sent_scores = []
        for tree, tagged_sent in zip(trees, words):
            i_main_verb = 0

            node_list = [node['rel'] for node in tree.nodes.values()]
            if 'ROOT' not in node_list:
                continue
            # i_root = node_list.index('ROOT')

            for node in tree.nodes.values():
                if node['rel'] == 'ROOT':
                    i_root = int(node['address'])

            if dep_tagset.is_verb(
                    ('', list(tree.nodes.values())[i_root]['tag'])):
                # If the root of the dep. tree is a verb, use it.
                i_main_verb = i_root - 1
            else:
                # Otherwise, use the first verb that is not in the gerund,
                #   in the participle, or in the infinitive.
                for i, token in enumerate(tagged_sent):
                    if tagset.is_verb(token) \
                            and token[0][-2:] not in ('do', 'ar', 'er', 'ir'):
                        i_main_verb = i
                        break

            sent_scores.append(i_main_verb)

        return sum(sent_scores) / len(sent_scores) if sent_scores else 0


class Constituents(base.Category):
    """"""

    name = 'Constituents'
    table_name = 'constituents'

    def __init__(self):
        super(Constituents, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
