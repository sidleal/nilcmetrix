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

# --- Base classes ---


class CoreferenceBase(base.Metric):
    """Docstring for CoreferenceBase. """

    def get_sentences(self, text, rp):
        """TODO: Docstring for get_sentences.

        :text: TODO
        :rp: TODO
        :returns: TODO

        """
        raise NotImplementedError('Subclasses must override this method.')

    @staticmethod
    def word_pairs(s1, s2):
        """TODO: Docstring for generate_word_pairs.

        :s1: TODO
        :s2: TODO
        :returns: TODO

        """
        for w1 in s1:
            for w2 in s2:
                yield w1.lower(), w2.lower()

    def sentence_pairs(self, text, rp):
        """TODO: Docstring for is_match.

        :src: TODO
        :dst: TODO
        :returns: TODO

        """
        raise NotImplementedError('Subclasses must override this method.')

    def value_for_text(self, t, rp=default_rp):
        if len(rp.sentences(t)) <= 1:
            return 0

        matches = 0
        pairs = 0
        for s1, s2 in self.sentence_pairs(t, rp):
            for w1, w2 in self.word_pairs(s1, s2):
                if w1 == w2:
                    matches += 1
            pairs += 1

        return matches / pairs if pairs else 0


class AdjacentOverlapBase(CoreferenceBase):
    """Docstring for AdjacentOverlapBase. """

    def sentence_pairs(self, text, rp):
        sentences = self.get_sentences(text, rp)

        for i in range(1, len(sentences)):
            yield sentences[i], sentences[i - 1]


class OverlapBase(CoreferenceBase):
    """Docstring for OverlapBase. """

    def sentence_pairs(self, text, rp):
        sentences = self.get_sentences(text, rp)

        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                yield sentences[i], sentences[j]


class ArgumentBase(CoreferenceBase):

    def get_sentences(self, text, rp):
        sentences = []
        tagset = rp.pos_tagger().tagset
        for sentence in rp.tagged_sentences(text):
            sentences.append([token[0] for token in sentence
                              if tagset.is_noun(token)
                              or tagset.is_pronoun(token)])

        return sentences


# --- Metric classes ---


class AdjacentArgumentOverlap(AdjacentOverlapBase, ArgumentBase):
    """
        **Nome da Métrica**: adj_arg_ovl

        **Interpretação**: repetição de referentes é um recurso de simplificação; portanto, quanto maior a métrica,
        menor a complexidade textual (exceto em textos constituídos de uma única sentença)

        **Descrição da métrica**: Quantidade média de referentes que se repetem nos pares de sentenças adjacentes do
         texto

        **Definição dos termos que aparecem na descrição da métrica**: pares de sentenças adjacentes são todas as
        possíveis combinações de 2 sentenças em sequência, por exemplo: 1-2, 2-3, 3-4, 4-5 (em um texto com 5
        sentenças); referentes são substantivos e pronomes.

        **Forma de cálculo da métrica**: em cada par de sentenças adjacentes, procuram-se referentes em comum. Cada
        coincidência identificada nos pares de sentenças adjacentes acumula 1 no contador. Ao final, divide-se o
        resultado do contador pela quantidade de pares de sentenças adjacentes do texto.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador nltk, POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As crianças aprendem muito rápido. Pesquisas mostram que até os três anos de vida, o desenvolvimento
        do cérebro ocorre num ritmo bem acelerado. O que os pais fazem no dia-a-dia, como ler, cantar e demonstrar
        carinho, é crucial para o desenvolvimento saudável da criança. Mas de acordo com certo estudo, apenas cerca da
        metade dos pais com crianças entre dois e oito anos lê diariamente para elas. Você talvez se pergunte: ‘Será
        que ler para o meu filho realmente faz diferença?’

        **Contagens**:

        5 sentenças, 4 pares de sentenças adjacentes (o sentenciador, porém, reconheceu 6 sentenças, o que produziu 5
        pares de sentenças adjacentes).

        2 referentes que se repetem em sentenças adjacentes: desenvolvimento (2-3), pais (3-4)

        **Resultado Esperado**: 0,50 (2/4)

        **Resultado Obtido**: 0,40 (2/5)

        **Status**: correto, considerando a limitação do sentenciador
    """

    name = 'Ratio of adjacent argument overlap'
    column_name = 'adj_arg_ovl'


class ArgumentOverlap(OverlapBase, ArgumentBase):
    """
        **Nome da Métrica**: arg_ovl

        **Interpretação**: repetição de referentes é um recurso de simplificação; portanto, quanto maior a métrica,
        menor a complexidade textual (exceto em textos constituídos de uma única sentença)

        **Descrição da métrica**: Quantidade média de referentes que se repetem nos pares de sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: referentes são substantivos ou pronomes; pares
        de sentenças são todas as possíveis combinações de 2 sentenças do texto: 1-2, 1-3, 2-3 (em um texto com 3
        sentenças).

        **Forma de cálculo da métrica**: em cada par de sentenças, procura-se referentes em comum. Cada coincidência
        encontrada acumula 1 no contador. Ao final, divide-se o resultado do contador pela quantidade de pares de
        sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador nltk, POS tagger nlpnet

        **Limitações da métrica**: a precisão da métrica depende do desempenho do sentenciador, do tagger e do stemmer

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As crianças aprendem muito rápido. Pesquisas mostram que até os três anos de vida, o desenvolvimento
        do cérebro ocorre num ritmo bem acelerado. O que os pais fazem no dia-a-dia, como ler, cantar e demonstrar
        carinho, é crucial para o desenvolvimento saudável da criança. Mas de acordo com certo estudo, apenas cerca da
        metade dos pais com crianças entre dois e oito anos lê diariamente para elas. Você talvez se pergunte: ‘Será
        que ler para o meu filho realmente faz diferença?’

        **Contagens**:

        10 pares de sentenças no texto (1-2, 1-3, 1-4, 1-5, 2-3, 2-4, 2-5, 3-4, 3-5, 4-5). O sentenciador, contudo,
        reconheceu 6 sentenças (uma é constituída pelas aspas, totalmente vazia), o que produziu 15 pares de sentenças.

        4 referentes que se repetem nos pares: crianças (1-4), anos (2-4) desenvolvimento (2-3), pais (3-4).

        **Resultado Esperado**: 0,40 (4/10)

        **Resultado Obtido**: 0,267 (4/15)

        **Status**: correto, considerando a limitação do sentenciador
    """

    name = 'Ratio of argument overlap to all sentence pairs'
    column_name = 'arg_ovl'


class AdjacentStemOverlap(AdjacentOverlapBase):
    """
        **Nome da Métrica**: adj_stem_ovl

        **Interpretação**: repetição de referentes é um recurso de simplificação; portanto, quanto maior a métrica,
        menor a complexidade textual (exceto em textos constituídos de uma única sentença).

        **Descrição da métrica**: Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de
        sentenças adjacentes do texto.

        **Definição dos termos que aparecem na descrição da métrica**: radicais são a parte inicial das palavras
        flexionáveis, desprezando-se a parte flexionável (ex: menin é o radical de menino, menina, menininho, meninos,
        etc.); palavras de conteúdo são substantivos, verbos, adjetivos e advérbios; sentenças adjacentes são 2
        sentenças do texto em sequência: 1-2, 2-3, 3-4 (em um texto com 4 sentenças).

        **Forma de cálculo da métrica**: em cada par de sentenças adjacentes, procura-se radicais de palavras de
        conteúdo em comum. Cada coincidência de radical identificada nos pares de sentenças adjacentes acumula 1 no
        contador. Ao final, divide-se o resultado do contador pela quantidade de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador nltk, POS tagger nlpnet e DELAF para reconhecer
        a raiz das palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do sentenciador e do tagger.

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As crianças aprendem muito rápido. Pesquisas mostram que até os três anos de vida, o desenvolvimento
        do cérebro ocorre num ritmo bem acelerado. O que os pais fazem no dia-a-dia, como ler, cantar e demonstrar
        carinho, é crucial para o desenvolvimento saudável da criança. Mas de acordo com certo estudo, apenas cerca da
        metade dos pais com crianças entre dois e oito anos lê diariamente para elas. Você talvez se pergunte: ‘Será
        que ler para o meu filho realmente faz diferença?’

        **Contagens**:

        5 sentenças, 4 pares de sentenças adjacentes (o sentenciador, porém, reconheceu 6 sentenças, o que produziu 5
        pares de sentenças adjacentes)

        5 radicais de palavras de conteúdo que se repetem nas adjacentes: desenvolvimento (2-3), pais (3-4), ler/lê
        (3-4), criança/crianças (3-4), lê/ler (4-5).

        **Resultado Esperado**: 1,25 (5/4)

        **Resultado Obtido**: 1,0 (5/5)

        **Status**: correto, considerando a limitação do sentenciador
    """

    name = 'Ratio of adjacent stem overlap'
    column_name = 'adj_stem_ovl'

    def get_sentences(self, text, rp):
        return rp.stemmed_content_words(text)


class StemOverlap(OverlapBase):
    """
        **Nome da Métrica**: stem_ovl

        **Interpretação**: repetição de referentes é um recurso de simplificação; portanto, quanto maior a métrica,
        menor a complexidade textual (exceto em textos constituídos de uma única sentença).

        **Descrição da métrica**: Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de
        sentenças do texto.

        **Definição dos termos que aparecem na descrição da métrica**: radicais são a parte inicial das palavras
        flexionáveis (despreza-se a parte flexionável: menin- é o radical de menino, menina, menininho, meninos, etc.);
        palavras de conteúdo são substantivos, verbos, adjetivos e advérbios; pares de sentenças são todas as possíveis
        combinações de 2 sentenças do texto: 1-2, 1-3, 2-3 (em um texto com 3 sentenças).

        **Forma de cálculo da métrica**: em cada par de sentenças, procura-se radicais de palavras de conteúdo em comum.
        Cada coincidência de radical identificada nos pares de sentenças adjacentes acumula 1 no contador. Ao final,
        divide-se o resultado do contador pela quantidade de pares de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador nltk, POS tagger nlpnet e DELAF para reconhecer a
        raiz das palavras

        **Limitações da métrica**: a precisão da métrica é dependente do desempenho dos recursos utilizados

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As crianças aprendem muito rápido. Pesquisas mostram que até os três anos de vida, o desenvolvimento
        do cérebro ocorre num ritmo bem acelerado. O que os pais fazem no dia-a-dia, como ler, cantar e demonstrar
        carinho, é crucial para o desenvolvimento saudável da criança. Mas de acordo com certo estudo, apenas cerca da
        metade dos pais com crianças entre dois e oito anos lê diariamente para elas. Você talvez se pergunte: ‘Será que
        ler para o meu filho realmente faz diferença?’

        **Contagens**:

        10 pares de sentenças (1-2, 1-3, 1-4, 1-5, 2-3, 2-4, 2-5, 3-4, 3-5, 4-5). O sentenciador reconheceu mais uma
        sentença, devido aos parênteses na última sentença, o que gerou 15 pares.

        8 radicais que se repetem nos pares de sentenças do texto: criança (1-3), criança (1-4), criança (3-4), ano
        (2-4), desenvolvimento (2-3), pais (3-4), fazer (3-5), ler (3-4), ler (3-5) e ler (4-5).

        **Resultado Esperado**: 1,00 (10/10)

        **Resultado Obtido**: 0,667 (10/15)

        **Status**: correto, considerando a limitação do sentenciador
    """

    name = 'Ratio of stem overlap to all sentence pairs'
    column_name = 'stem_ovl'

    def get_sentences(self, text, rp):
        return rp.stemmed_content_words(text)


class AdjacentContentWordOverlap(AdjacentOverlapBase):
    """
        **Nome da Métrica**: adj_cw_ovl

        **Interpretação**: repetição de referentes é um recurso de simplificação; portanto, quanto maior a métrica,
        menor a complexidade textual (exceto em textos constituídos de uma única sentença).

        **Descrição da métrica**: Quantidade média de palavras de conteúdo que se repetem nos pares de sentenças
        adjacentes do texto.

        **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
        adjetivos e advérbios; pares de sentenças adjacentes são todas as possíveis combinações de 2 sentenças do texto
        em sequência: 1-2, 2-3, 3-4 (em um texto com 4 sentenças).

        **Forma de cálculo da métrica**: em cada par de sentenças adjacentes, procuram-se palavras de conteúdo em comum.
        Cada coincidência identificada acumula 1 no contador. Ao final, divide-se o resultado do contador pela
        quantidade de pares de sentenças adjacentes do texto.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador nltk, POS tagger nlpnet.

        **Limitações da métrica**: a precisão da métrica é dependente do desempenho dos recursos utilizados

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: As crianças aprendem muito rápido. Pesquisas mostram que até os três anos de vida, o desenvolvimento
        do cérebro ocorre num ritmo bem acelerado. O que os pais fazem no dia-a-dia, como ler, cantar e demonstrar
        carinho, é crucial para o desenvolvimento saudável da criança. Mas de acordo com certo estudo, apenas cerca da
        metade dos pais com crianças entre dois e oito anos lê diariamente para elas. Você talvez se pergunte: ‘Será
        que ler para o meu filho realmente faz diferença?’

        **Contagens**:

        4 pares de sentenças adjacentes (o sentenciador, porém, reconheceu 6 sentenças, o que produziu 5 pares de
        sentenças adjacentes),

        2 palavras de conteúdo que se repetem nos pares: desenvolvimento (2-3), pais (3-4)

        **Resultado Esperado**: 0,50 (2/4)

        **Resultado Obtido**: 0,4 (2/5)

        **Status**: correto, considerando a limitação do sentenciador.
    """

    name = 'Ratio of adjacent content word overlap'
    column_name = 'adj_cw_ovl'

    def get_sentences(self, text, rp):
        return rp.content_words(text)


class Coreference(base.Category):
    """"""

    name = 'Coreference'
    table_name = 'coreference'

    def __init__(self):
        super(Coreference, self).__init__()
        self.metrics = [AdjacentArgumentOverlap(),
                        ArgumentOverlap(),
                        AdjacentStemOverlap(),
                        StemOverlap(),
                        AdjacentContentWordOverlap(),
                        ]
