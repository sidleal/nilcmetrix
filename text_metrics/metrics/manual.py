# -*- coding: utf-8 -*-
# Copyright (C) 2015  Nathan Siegle Hartmann
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
from text_metrics.utils import ilen, count_occurrences_for_all
from text_metrics.tools import pos_tagger
from text_metrics.metrics.basic_counts import Sentences
from text_metrics.metrics.anaphoras import AnaphoricReferencesBase
from text_metrics.metrics.ambiguity import AdjectiveAmbiguity, AdverbAmbiguity
from text_metrics.metrics.ambiguity import NounAmbiguity, VerbAmbiguity
from itertools import chain
import re


class EasyConjunctions(base.Metric):
    """
    ## Razão de palavras do texto que correspondem a conjunções fáceis.

    Calcula-se a razão de palavras do texto que correspondem a conjunções
    fáceis. A lista de conjunções fáceis foi compilada por Livia Cucatto com
    base nas ocorrências do córpus da empresa.

    ### Exemplo:

    *"Eles brincaram o dia todo e foi muito divertido. Além disso, fizeram
    muitos amigos."*

    Com 14 palavras e 2 conjunções fáceis compostas ao todo por 3 palavras
    (__e__ e __além disso__), o valor da métrica é 0,214.
    """

    name = 'Easy Conjunctions'
    column_name = 'easy_conjunctions_ratio'

    def value_for_text(self, t, rp=default_rp):
        conj = rp._conjuncoes_fund1()
        lower = ' '.join([' '] + [i.lower() for i in rp.all_words(t)] + [' '])
        count = 0
        occur = []
        for c in conj:
            count += lower.count(' ' + c + ' ') * len(c.split())
            if lower.count(' ' + c + ' ') * len(c.split()) > 0:
                if len(occur) < 12:
                    occur += [c]
        print(occur)
        try:
            return count / len(rp.all_words(t))
        except ZeroDivisionError:
            return 0


class HardConjunctions(base.Metric):
    """
    ## Razão de palavras do texto que correspondem a conjunções difíceis.

    Calcula-se a razão de palavras do texto que correspondem a conjunções
    difíceis. A lista de conjunções difíceis foi compilada por Livia Cucatto
    com base nas ocorrências do córpus da empresa.

    ### Exemplo:

    *"Visto que muitas pessoas sairam feridas, foi necessário tomar uma medida
    imediata a fim de neutralizar os danos causados e reverter a situação."*

    Com 23 palavras e 2 conjunções difíceis compostas ao todo por 5 palavras
    (__a fim de__ e __visto que__), o valor da métrica é 0,217.
    """

    name = 'Hard Conjunctions'
    column_name = 'hard_conjunctions_ratio'

    def value_for_text(self, t, rp=default_rp):
        conj = rp._conjuncoes_fund2()
        lower = ' '.join([' '] + [i.lower() for i in rp.all_words(t)] + [' '])
        count = 0
        occur = []
        for c in conj:
            count += lower.count(' ' + c + ' ') * len(c.split())
            if len(occur) < 12:
                occur += [c]
        print(occur)
        try:
            return count / len(rp.all_words(t))
        except ZeroDivisionError:
            return 0


class DifficultWords25(base.Metric):
    """
    ## Palavras de Conteúdo com Frequência menor que 25.

    Calcula-se a soma do log da frequência de cada palavra de conteúdo do texto
    no córpus compilado de palavras difíceis.
    O córpus foi compilado com o PLN-Br, um dump da Wikipédia e um dump do G1.

    ### Exemplo:

    *""*
    """

    name = 'Difficult Words of Frequency Lower than 25'
    column_name = 'difficult_words_25'

    def value_for_text(self, t, rp=default_rp):
        dificeis = rp.palavras_dificeis()
        cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
        occur = []
        for i in cw:
            if i in dificeis[25]:
                print(i)
                occur += [i]
        print(occur)
        return rp.log_for_words(cw, dificeis[25])


class DifficultWords200(base.Metric):
    """
    ## Palavras de Conteúdo com Frequência menor que 200.

    Calcula-se a soma do log da frequência de cada palavra de conteúdo do texto
    no córpus compilado de palavras difíceis.
    O córpus foi compilado com o PLN-Br, um dump da Wikipédia e um dump do G1.

    ### Exemplo:

    *""*
    """

    name = 'Difficult Words of Frequency Lower than 200'
    column_name = 'difficult_words_200'

    def value_for_text(self, t, rp=default_rp):
        dificeis = rp.palavras_dificeis()
        cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
        occur = []
        for i in cw:
            if i in dificeis[200]:
                print(i)
                occur += [i]
        print(occur)
        return rp.log_for_words(cw, dificeis[200])


# class RatioOfPresentVerbs(base.Metric):
#     """
#         **Nome da Métrica**: present_to_tenses_ratio
#
#         **Interpretação**: sem a especificação do modo verbal, não é clara a relação da métrica com a complexidade
#         textual
#
#         **Descrição da métrica**: Proporção de Verbos no Presente em relação à quantidade de verbos flexionados no
#         texto.
#
#         **Definição dos termos que aparecem na descrição da métrica**: Verbos no tempo Presente, sem definir o modo
#         (pode ser no Indicativo, no Subjuntivo ou no Imperativo). Todo verbo flexionado tem um modo e um tempo verbal.
#         A etiqueta de verbos flexionados é VFIN. As etiquetas de modo são: IND (indicativo), SUBJ (subjuntivo),
#         IMP (imperativo). As etiquetas de tempo verbal são: PR (presente), IMPF (imperfeito), OS (perfeito simples),
#         MQP (mais-que-perfeito), FUT (futuro), COND (futuro do pretérito ou condicional).
#
#         **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*PR. e divide-se o resultado pelo
#         total de verbos flexionados do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**: os modos verbais têm diferentes complexidades. Juntar os tempos, sem especificar o
#         modo, mistura flexões complexas com flexões simples.
#
#         **Crítica**: Há duas métricas de verbos no presente: esta, da Guten, e a indicative_present_ratio, do AIC.
#         Esta está sendo comentada no programa para evitar redundância.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado
#         no tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais
#         de 6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
#         frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
#         Estados Unidos. É possível que esse vídeo faça uma enorme diferença na mudança dos hábitos alimentares dos
#         americanos e provoque um decréscimo dos índices de colesterol da população.
#
#         **Contagens**: 8 verbos, 6 no presente (4 no Indicativo), 2 no pretérito perfeito
#
#         **Resultado Esperado**: 6/8 = 0,75
#
#         **Resultado Obtido**: 0,75
#
#         **Status**: correto
#     """
#
#     name = 'Ratio of Present Tense Verbs to All Verbs'
#     column_name = 'present_to_tenses_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             present = len(re.findall('V.*PR', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             present = 0
#         try:
#             imperfect = len(re.findall('V.*IMPF', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             imperfect = 0
#         try:
#             perfect = len(re.findall('V.*PS', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             perfect = 0
#         try:
#             pluperfect = len(re.findall('V MQP', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             pluperfect = 0
#         try:
#             future = len(re.findall('V.*FUT', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             future = 0
#         try:
#             conditional = len(re.findall('V.*COND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             conditional = 0
#         tenses = [present, imperfect, perfect, pluperfect, future, conditional]
#         # return tenses.index(max(tenses))
#         occur = []
#         count = 0
#         for i in re.findall('\[(.*)\].*V.*PR', flat):
#             print(i)
#             count += 1
#             if count <= 12:
#                 occur += [i]
#         print(occur)
#         return tenses[0] / sum(tenses)


class AdjectiveRatio(base.Metric):
    """
        ## Taxa de Adjetivos:

        Taxa de adjetivos em um texto.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        POS tagger do nlpnet.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Com 6 adjetivos (__polêmico__, __municipais__, __estaduais__,
        __federais__, __solares__ e __anuais__) e 95 palavras, a Taxa de
        adjetivos é 63,157 (número de adjetivos/número de palavras).
    """

    name = 'Adjective Ratio'
    column_name = 'adjective_ratio'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        occur = []
        count = 0
        for i in adjectives:
            print(i)
            count += 1
            if count <= 12:
                occur += [i[0]]
        print(occur)
        return ilen(adjectives) / ilen(rp.all_words(t))


class ContentWordsAmbiguity(base.Metric):
    """
        ## Ambiguidade de Palavras de Conteúdo:

        Calcula a ambiguidade referente a adjetivos, advérbios, substantivos e
        verbos em um texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"O menino estudou para a prova e se saiu bem nela."*

        Com o valor 0 para ambiguidade de adjetivos, 6 para ambiguidade de
        advérbios, 5 para ambiguidade de substantivos e 11 para ambiguidade
        de verbos, e um total de 11 palavras, o valor da métrica é 2,0.
    """

    name = 'Content Words Ambiguity'
    column_name = 'content_words_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        adjectives = AdjectiveAmbiguity().value_for_text(t)
        adverbs = AdverbAmbiguity().value_for_text(t)
        nouns = NounAmbiguity().value_for_text(t)
        verbs = VerbAmbiguity().value_for_text(t)
        palavras = len(rp.all_words(t))
        try:
            return (adjectives + adverbs + nouns + verbs) / palavras
        except:
            return 0


class SimpleWords(base.Metric):
    """
        ## Taxa de palavras simples:

        Calcula-se a taxa de palavras simples sobre o total de palavras de
        conteúdo do texto.
        É utilizada a lista de palavras simples da XXXXXXX

        ### Exemplo:

        *"O menino colou na prova, embora soubesse que poderia ser pego."*

        VALIDAR LISTA
    """

    name = 'Ratio of Simple Words'
    column_name = 'simple_word_ratio'

    def value_for_text(self, t, rp=default_rp):
        sw = rp.simple_words()
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        content_words = list(map(lambda t: t[0], content_tokens))
        count = 0
        for word in sw:
            if word in content_words:
                count += 1
                if count <= 12:
                    print(word)
        return count / len(content_words)


class SimpleVerbs(base.Metric):
    """
    ## Taxa de verbos simples.

    Calcula-se a razão de verbos simples sobre os verbos do texto.
    É utilizada a lista de palavras simples da XXXXXXX

    ### Exemplo:

    *"O menino colou na prova, embora soubesse que poderia ser pego."*

    VALIDAR LISTA
    """

    name = 'Ratio of Simple Verbs'
    column_name = 'simple_verb_ratio'

    def value_for_text(self, t, rp=default_rp):
        sw = rp.simple_words()
        verbs = [t for t in rp.tagged_words(t)
                 if pos_tagger.tagset.is_verb(t) or
                 pos_tagger.tagset.is_auxiliary_verb(t) or
                 pos_tagger.tagset.is_participle(t)]
        verbs = list(map(lambda t: t[0], verbs))
        count = 0
        occur = []
        for word in sw:
            if word in verbs:
                print(word)
                count += 1
                if count <= 12:
                    occur += [word]
        print(occur)
        return count / len(verbs)


class WordsPerSentence(base.Metric):
    """
        ## Palavras por Sentenças:

        Número de palavras dividido pelo número de sentenças.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Neste exemplo o número de palavras é 95 e o número de sentenças é
            4. Portanto,o número de palavras por sentenças é 23,75.
    """

    name = 'Mean words per sentence'
    column_name = 'words_per_sentence'

    def value_for_text(self, t, rp=default_rp):
        print('%d palavras e %d sentenças'%(Words().value_for_text(t), Sentences().value_for_text(t)))
        return Words().value_for_text(t) / Sentences().value_for_text(t)


class NotSVO(base.Metric):
    """
    ## Razão de orações de um texto que não estão no formato SVO.

    Calcula-se a razão entre o número de orações de um texto que não estão
    no formato SVO para o número total de orações de um texto.


    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Segundo o relato do delator da operação lava-jato, foi roubado
    dinheiro dos cofres públicos."*
    """

    name = 'Ratio of not SVO clauses to all clauses'
    column_name = 'non_svo_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lines = flat.split('\n')
        count = 0
        found = False
        for line in lines:
            if ('@ADVL>' in line or 'APP' in line or '<SUBJ' in line) and not found:
                found = True
                count += 1
            if ' V ' in line and '<aux>' not in line:
                found = False
        nverbs = flat.count(' V ') - flat.count('<aux>')
        try:
            print('%d não SVO de um total de %d orações'%(count, nverbs))
            return count / nverbs
        except ZeroDivisionError:
            return 0


class CoordinateClausesPredominance(base.Metric):
    """
        ## Razão de orações coordenadas:

        Retorna a proporção de oração coordenadas por todas as orações
        coordenadas e subordinadas.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"O menino estudou para a prova e se saiu bem nela."*

        De 2 orações, 1 é iniciada por conjunções coordenadas (__e__) e não há
        orações iniciadas por conjunções subordinadas, resultando no valor da
        métrica de 1,0.
    """

    name = 'Ratio of Coordinate Clauses to Coordinate and Subordinate Ones'
    column_name = 'coordinate_clauses_predominance'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        for i in re.findall('.* KC ', flat):
            print(i)
        coord_clauses = flat.count(' KC ')
        subord_clauses = flat.count(' KS ')     # relativa explicativa
        rel = flat.count('<rel>')   # relativas restritivas
        try:
            return coord_clauses / (coord_clauses + subord_clauses + rel)
        except ZeroDivisionError:
            return 0


class SubordinateAdjectives(base.Metric):
    """
        ## Predominância de orações subordinadas adjetivas restritivas e
        explicativas:

        Retorna 1 se houver predominância de orações subordinadas restritivas
        e explicativas, do contrário 0.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"Jamais teria chegado aqui, não fosse a gentileza de um homem que
        passava naquele momento. O homem, que se considera racional, muitas
        vezes age animalescamente."*

        De 2 orações, 1 é iniciada por conjunções coordenadas (__e__) e não há
        orações iniciadas por conjunções subordinadas, resultando no valor da
        métrica de 1.
    """

    name = '''Ratio of Subordinate Adjectives Clauses to Coordinate and
    Subordite Ones'''
    column_name = 'subordinate-adjectives_predominance'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        expression = re.compile('''
                                <rel>|
                                [que].*KS
                                ''',
                                re.VERBOSE)
        expression2 = re.compile('''
                                 KC|
                                 KS|
                                 <rel>
                                 ''',
                                 re.VERBOSE)
        expression3 = re.compile('''
                                .*<rel>|
                                .*[que].*KS
                                ''',
                                re.VERBOSE)
        adjectives = len(re.findall(expression, flat))
        for i in re.findall(expression3, flat):
            print(i)
        clauses = len(re.findall(expression2, flat))
        try:
            return adjectives / clauses
        except ZeroDivisionError:
            return 0


class AdverbialsLevel1(base.Metric):
    """
    ## Razão de orações adverbiais de nível 1 por todas as orações.

    Calcula a proporção de orações adverbiais sobre o total de orações
    coordenadas e subordinadas.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Adverbials Level 1 to All Clauses'
    column_name = 'adverbials_01_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        expression = re.compile('''
                                \[a=fim=de\]|                   # final
                                \[a=fim=de=que\]|               # final
                                \[porque\]|                     # final
                                \[já=que\]|        # causal
                                \[porquanto\]|                  # causal
                                \[uma=vez=que\]|                # causal
                                \[visto=que\]|                  # causal
                                \[como\]|                       # causal
                                \[que\].*<rel>|                 # explicativa
                                \[onde\]|                       # explicativa
                                \[quando\]|                     # explicativa
                                \[quem\]|                       # explicativa
                                \[quanto\]|                     # explicativa
                                \[assim=que\]|                  # temporal
                                \[logo=que\]|                   # temporal
                                \[contanto=que\]|               # condicional
                                \[se\].*KS|                     # condicional
                                \[caso\].*KS|                   # condicional
                                \[a=menos=que\]                 # condicional
                                \[a=não=ser=que]   # condicional
                                \[exceto=se\]                   # condicional
                                \[salvo=se\]                    # condicional
                                \[desde=que\]                   # condicional
                                \[se=bem=que\]                  # condicional
                                ''',
                                re.VERBOSE)
        ocorrencias1 = len(re.findall(expression, flat))
        for i in re.findall(expression, flat):
            print(i)
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),      # final
                lower.count('depois de'),     # temporal
                lower.count('depois que'),    # temporal
                lower.count('antes que'),     # condicional
                lower.count('sem que'),       # condicional
            ]
        )
        expression2 = re.compile('''
                                 KC|
                                 KS|
                                 <rel>
                                 ''',
                                 re.VERBOSE)
        clauses = len(re.findall(expression2, flat))
        try:
            return (ocorrencias1 + ocorrencias2) / clauses
        except ZeroDivisionError:
            return 0


class AdjacentPersonalPronounAnaphoricReferences(AnaphoricReferencesBase):
    """
        ## Referência Anafórica de Pronomes Pessoais do Caso Reto Adjacentes:

        Proporção de referências anafóricas de pronomes pessoais do caso reto
        entre sentenças adjacentes.

        ### Exemplo:

        *"Dentro do lago, existem peixes, como a traíra e o dourado. Nele,
        também existe a palometa, um tipo de piranha. Ela é uma espécie
        carnívora que se alimenta de peixes."*
    """
    referents = {r'^elas$': 'fp',
                 r'^eles$': 'mp',
                 r'^ela$': 'fs',
                 r'^ele$': 'ms',
                 }
    name = '''Ratio of candidates of personal pronouns to anaphoric reference
            in adjacente sentences'''
    column_name = 'coreference_pronoum_ratio'

    def __init__(self):
        super(AdjacentPersonalPronounAnaphoricReferences, self).__init__(nsentences=1)


class DiscourseMarkers(base.Metric):
    """
        ## Taxa de marcadores discursivos:

        Calcula-se a Taxa de marcadores discursivos sobre o número de
        palavras do texto.

        É utilizada uma lista de marcadores discursivos compilada no projeto.

        ### Exemplo:

        *"O menino colou na prova. Ainda assim, ele não obteve uma boa nota e
        ainda foi advertido pela escola."*

        Com 3 marcadores discursivos ambíguos encontrados (__ainda__, __assim__
        e __e__), o valor da métrica é 0,15.
    """

    name = 'Ratio of Discourse Markers'
    column_name = 'discourse_markers_ratio'

    def value_for_text(self, t, rp=default_rp):
        marcadores = rp.discourse_markers()
        tokens = rp.all_tokens(t)
        count = 0
        for marcador in marcadores:
            if marcador in tokens:
                print(marcador)
                count += 1
        return count / len(rp.all_words(t))


class Words(base.Metric):
    """
        ## Número de Palavras:

        Número de palavras do texto.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        O exemplo possui 17 palavras.
    """

    name = 'Number of Words'
    column_name = 'words'

    def value_for_text(self, t, rp=default_rp):
        # return ilen(filterfalse(pos_tagger.tagset.is_punctuation,
        #                         rp.tagged_words(t)))
        print(len(rp.tagged_words(t)))
        return len(rp.tagged_words(t))


class TemporalAdjunctRatio(base.Metric):
    """
        ## Proporção de adjuntos advérbiais de tempo em razão dos adjuntos
        advérbiais do texto.

        Calcula a porcentagem de adjuntos advérbiais temporais em razão de
        todas os adjuntos advérbiais do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        POS tagger do nlpnet.

        ### Exemplo:

        *"Foi durante meus experimentos que eu me machuquei. Certamente cometi
        um erro."*

        Com 1 adjunto temporal (__durante__) dentre 2 adjuntos (__durante__ e
        __certamente__), o valor da métrica é 0,5.
    """

    name = 'Ratio of Temporal Adjuncts to All Adjuncts'
    column_name = 'temporal_adjunct_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        adjuncts = re.findall('ADVL', flat)
        temporals = rp.temporal_expressions(t)
        for i in temporals:
            print(i)
        try:
            return len(temporals) / len(adjuncts)
        except ZeroDivisionError:
            return 0


class RelativePronounsDiversity(base.Metric):
    """
    ## Diversidade de Pronomes Relativos.

    Calcula a porcentagem de pronomes relativos distintos entre os pronomes
    relativos de um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Regressando de São Paulo, visitei o sítio de minha tia, o qual me
    deixou encantado. Era exatamente o que eu esperava, apesar de nunca ter
    imaginado que eu estaria ali."*

    Com 2 ocorrências de pronomes relativos distintas (__o qual__ e __que__
    ) e apenas esses 2 pronomes relativos no texto, o valor da métrica é
    1,0.
    """

    name = 'Relative Pronouns Diversity'
    column_name = 'relative_pronouns_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        casos = re.findall('\[.*\].*<rel>', flat)
        occur = []
        count = 0
        if casos:
            relativos = [re.search('\[(.*)\].*<rel>', i).group(1) for i in casos]
            for i in list(set(relativos)):
                count += 1
                print(i)
                if count <= 12:
                    occur += [i]
            print(occur)
            unique = len(set(relativos))
            try:
                return unique / len(relativos)
            except ZeroDivisionError:
                return 0
        else:
            return 0


class AdverbialsLevel2(base.Metric):
    """
    ## Razão de adverbiais de nível 2.

    Calcula a proporção de orações adverbiais sobre o total de orações
    coordenadas e subordinadas.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Adverbials Level 2 to Coordinate and Subordinate Clauses'
    column_name = 'adverbials_02_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        expression = re.compile('''
                                \[a=fim=de\]|                   # final
                                \[a=fim=de=que\]|               # final
                                \[porque\]|                     # final
                                \[já=que\]|        # causal
                                \[porquanto\]|                  # causal
                                \[uma=vez=que\]|                # causal
                                \[visto=que\]|                  # causal
                                \[como\]|                       # causal
                                \[que\].*<rel>|                 # explicativa
                                \[onde\]|                       # explicativa
                                \[quando\]|                     # explicativa
                                \[quem\]|                       # explicativa
                                \[quanto\]|                     # explicativa
                                \[assim=que\]|                  # temporal
                                \[logo=que\]|                   # temporal
                                \[contanto=que\]|               # condicional
                                \[se\].*KS|                     # condicional
                                \[caso\].*KS|                   # condicional
                                \[a=menos=que\]                 # condicional
                                \[a=não=ser=que]|  # condicional
                                \[exceto=se\]|                  # condicional
                                \[salvo=se\]|                   # condicional
                                \[desde=que\]|                  # condicional
                                \[apesar=de=que\]|              # concessiva
                                \[embora\]|                     # concessiva
                                \[mas\]|                        # concessiva
                                \[conquanto\]|                  # concessiva
                                \[ainda=que\]|                  # concessiva
                                \[mesmo=que\]|                  # concessiva
                                \[nem=que\]|                    # concessiva
                                \[por=mais=que\]|               # concessiva
                                \[posto=que\]|                  # concessiva
                                \[por=muito=que\]               # concessiva
                                ''',
                                re.VERBOSE)
        ocorrencias1 = len(re.findall(expression, flat))
        for i in re.findall(expression, flat):
            print(i)
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),      # final
                lower.count('depois de'),     # temporal
                lower.count('depois que'),    # temporal
                lower.count('antes que'),     # condicional
                lower.count('sem que'),       # condicional
                lower.count('apesar que'),    # concessiva

            ]
        )
        if 'para que' in lower:
            print('para que')
        if 'depois de' in lower:
            print('depois de')
        if 'depois que' in lower:
            print('depois que')
        if 'antes que' in lower:
            print('antes que')
        if 'sem que' in lower:
            print('sem que')
        if 'apesar que' in lower:
            print('apesar que')
        expression2 = re.compile('''
                                 KC|
                                 KS|
                                 <rel>
                                 ''',
                                 re.VERBOSE)
        clauses = len(re.findall(expression2, flat))
        try:
            return (ocorrencias1 + ocorrencias2) / clauses
        except ZeroDivisionError:
            return 0


class AdjacentDemonstrativePronounAnaphoricReferences(AnaphoricReferencesBase):
    """
        ## Referência Anafórica de Pronomes Demonstrativos em Sentenças
        Adjacentes:

        Proporção de referências anafóricas de pronomes demonstrativos entre
        sentenças adjacentes.

        ### Exemplo:

        *"Dentro do lago, existem peixes, como a traíra e o dourado. Nele,
        também existe a palometa, um tipo de piranha. Ela é uma espécie
        carnívora que se alimenta de peixes."*
    """
    referents = {r'^este$': 'ms',
                 r'^estes$': 'mp',
                 r'^esta$': 'fs',
                 r'^estas$': 'fp',
                 r'^isto$': 'ms',
                 r'^esse$': 'ms',
                 r'^esses$': 'mp',
                 r'^essa$': 'fs',
                 r'^essas$': 'fp',
                 r'^nesse$': 'ms',
                 r'^nesses$': 'mp',
                 r'^nessa$': 'fs',
                 r'^nessas$': 'fp',
                 r'^neste$': 'ms',
                 r'^nestes$': 'mp',
                 r'^nesta$': 'fs',
                 r'^nestas$': 'fp',
                 r'^isso$': 'ms',
                 r'^nisso$': 'ms',
                 r'^nisto$': 'ms',
                 r'^aquele$': 'ms',
                 r'^aqueles$': 'mp',
                 r'^aquela$': 'fs',
                 r'^aquelas$': 'fp',
                 r'^aquilo$': 'ms',
                 r'^naquele$': 'ms',
                 r'^naqueles$': 'mp',
                 r'^naquela$': 'fs',
                 r'^naquelas$': 'fp',
                 r'^naquilo$': 'sm',
                 r'^deste$': 'ms',
                 r'^destes$': 'mp',
                 r'^desta$': 'fs',
                 r'^destas$': 'fp',
                 r'^desse$': 'ms',
                 r'^desses$': 'mp',
                 r'^dessa$': 'fs',
                 r'^dessas$': 'fp',
                 r'^daquele$': 'ms',
                 r'^daqueles$': 'mp',
                 r'^daquela$': 'fs',
                 r'^daquelas$': 'fp',
                 r'^disto$': 'ms',
                 r'^disso$': 'ms',
                 r'^daquilo$': 'ms',
                 r'^o mesmo$': 'ms',
                 r'^a mesma$': 'fs',
                 r'^os mesmos$': 'mp',
                 r'^as mesmas$': 'fp',
                 r'^o próprio$': 'ms',
                 r'^a própria$': 'fs',
                 r'^os próprios$': 'mp',
                 r'^as próprias$': 'fp',
                 r'^tal$': 'sm',
                 r'^tais$': 'sp',
                 }
    name = '''Ratio of candidates of demonstrative pronouns to anaphoric
            reference in adjacente sentences'''
    column_name = 'demonstrative_pronoun_ratio'

    def __init__(self):
        super(AdjacentDemonstrativePronounAnaphoricReferences, self).__init__(nsentences=1)


class AdverbDiversity(base.Metric):
    """
    ## Diversidade de Advérbios.

    Calcula a porcentagem de advérbios distintos entre os advérbios de um
    texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
        Já não temos recursos suficientes para a manutenção das escolas,
        por exemplo, e também precisamos valorizar o magistério - justifica
        a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

    Com 8 ocorrências de advérbios e 7 sendo advérbios únicos no texto, o
    valor da métrica é 0,875.
    """

    name = 'Adverbs Diversity'
    column_name = 'adverbs_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        adverbs = [i[0].lower() for i in rp.tagged_words(t)
                   if pos_tagger.tagset.is_adverb(i)
                   or pos_tagger.tagset.is_denotative_word(i)]
        unique = len(set(adverbs))
        for i in list(set(adverbs)):
            print(i)
        try:
            return unique / len(adverbs)
        except ZeroDivisionError:
            return 0


class AdjectiveDiversity(base.Metric):
    """
    ## Diversidade de Adjetivos.

    Calcula a porcentagem de adjetivos distintos entre os adjetivos de um
    texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
        Já não temos recursos suficientes para a manutenção das escolas,
        por exemplo, e também precisamos valorizar o magistério - justifica
        a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

    Com 2 adjetivos (__suficientes__ e __Pedagógico__) e todos com
    ocorrências únicas no texto, o valor da métrica é 1,0.
    """

    name = 'Adjective Diversity'
    column_name = 'adjective_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        adjectives = [i[0].lower() for i in adjectives]
        unique = len(set(adjectives))
        occur = []
        count = 0
        for i in list(set(adjectives)):
            print(i)
            count += 1
            if count <= 12:
                occur += [i]
        print(occur)
        try:
            return unique / len(adjectives)
        except ZeroDivisionError:
            return 0


class AdverbialsLevel3(base.Metric):
    """
    ## Razão de adverbiais de nível 3.

    Calcula a proporção de orações adverbiais sobre o total de orações
    coordenadas e subordinadas.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Adverbials Level 3 to Coordinate and Subordinate Clauses'
    column_name = 'adverbials_03_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        expression = re.compile('''
                                \[a=fim=de\]|                   # final
                                \[a=fim=de=que\]|               # final
                                \[porque\]|                     # final
                                \[já=que\]|        # causal
                                \[porquanto\]|                  # causal
                                \[uma=vez=que\]|                # causal
                                \[visto=que\]|                  # causal
                                \[como\]|                       # causal
                                \[que\].*<rel>|                 # explicativa
                                \[onde\]|                       # explicativa
                                \[quando\]|                     # explicativa
                                \[quem\]|                       # explicativa
                                \[quanto\]|                     # explicativa
                                \[assim=que\]|                  # temporal
                                \[logo=que\]|                   # temporal
                                \[contanto=que\]|               # condicional
                                \[se\].*KS|                     # condicional
                                \[caso\].*KS|                   # condicional
                                \[a=menos=que\]                 # condicional
                                \[a=não=ser=que]|  # condicional
                                \[exceto=se\]|                  # condicional
                                \[salvo=se\]|                   # condicional
                                \[desde=que\]|                  # condicional
                                \[apesar=de=que\]|              # concessiva
                                \[embora\]|                     # concessiva
                                \[mas\]|                        # concessiva
                                \[conquanto\]|                  # concessiva
                                \[ainda=que\]|                  # concessiva
                                \[mesmo=que\]|                  # concessiva
                                \[nem=que\]|                    # concessiva
                                \[por=mais=que\]|               # concessiva
                                \[posto=que\]|                  # concessiva
                                \[por=muito=que\]|              # concessiva
                                \[de=forma=que\]|               # consecutiva
                                \[de=modo=que\]|                # consecutiva
                                \[conforme\]|                   # consecutiva
                                \[consoante\]|                  # consecutiva
                                \[segundo\]|                    # consecutiva
                                \[como\]                        # consecutiva
                                ''',
                                re.VERBOSE)
        ocorrencias1 = len(re.findall(expression, flat))
        for i in re.findall(expression, flat):
            print(i)
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),      # final
                lower.count('depois de'),     # temporal
                lower.count('depois que'),    # temporal
                lower.count('antes que'),     # condicional
                lower.count('sem que'),       # condicional
                lower.count('apesar que'),    # concessiva
                lower.count('tamanho que'),   # consecutiva
                lower.count('tal que'),       # consecutiva
                lower.count('tanto que'),     # consecutiva

            ]
        )
        if 'para que' in lower:
            print('para que')
        if 'depois de' in lower:
            print('depois de')
        if 'depois que' in lower:
            print('depois que')
        if 'antes que' in lower:
            print('antes que')
        if 'sem que' in lower:
            print('sem que')
        if 'apesar que' in lower:
            print('apesar que')
        if 'tamanho que' in lower:
            print('tamanho que')
        if 'tal que' in lower:
            print('tal que')
        if 'tanto que' in lower:
            print('tanto que')
        expression2 = re.compile('''
                                 KC|
                                 KS|
                                 <rel>
                                 ''',
                                 re.VERBOSE)
        clauses = len(re.findall(expression2, flat))
        try:
            return (ocorrencias1 + ocorrencias2) / clauses
        except ZeroDivisionError:
            return 0


class DiscourseMarkersLevel3(base.Metric):
    """
    ## Razão de marcadores discursivos de nível 3 por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos de nível 3 para o número de
    sentenças do texto. Os marcadores são: não bastasse, além de, de volta e
    até.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = '''Ratio of Discourse Markers Level 3 to All Clauses'''
    column_name = 'discourse_markers_level_3'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        ocorrencias = sum(
            [
                lower.count('não bastasse'),
                lower.count('além de'),
                lower.count('de volta'),
                lower.count('até'),
            ]
        )
        if lower.count('não bastasse') > 0:
            print('%d não bastasse'%lower.count('não bastasse'))
        if lower.count('além de') > 0:
            print('%d além de'%lower.count('além de'))
        if lower.count('de volta') > 0:
            print('%d de volta'%lower.count('de volta'))
        if lower.count('até') > 0:
            print('%d até'%lower.count('até'))
        clauses = flat.count(' V ') - flat.count('<aux>')
        try:
            return ocorrencias / clauses
        except ZeroDivisionError:
            return 0


class ObliquePronounsRatio(base.Metric):
    """
        ## Razão de pronomes oblíquos sobre os pronomes do texto.

        Calcula a porcentagem de pronomes do texto que são pronomes oblíquos.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        POS tagger do nlpnet.

        ### Exemplo:

        *"Foi durante meus experimentos que eu me machuquei. Certamente cometi
        um erro."*

        Com 1 pronome oblíquo (__me__) e 4 pronomes identificados (__meus__,
        __que__, __eu__ e __me__), o valor da métrica é 0,25.
    """

    name = 'Ratio of Oblique Pronouns to All Pronouns'
    column_name = 'oblique_pronouns_ratio'

    def value_for_text(self, t, rp=default_rp):
        # obliques_list = [
        #     # Casos Tônicos
        #     ('mim', 'PROPESS'), ('comigo', 'PREP+PROPESS'), ('ti', 'PROPESS'),
        #     ('contigo', 'ADJ'), ('contigo', 'N'), ('contigo', 'PROPESS'),
        #     ('si', 'PROPESS'), ('consigo', 'PROPESS'),
        #     ('nós', 'PROPESS'), ('conosco', 'PROPOSS'), ('conosco', 'ADV'),
        #     ('vós', 'PROPESS'), ('vós', 'N'), ('vós', 'ADJ'),
        #     ('convosco', 'PROPESS'), ('convosco', 'N'), ('convosco', 'ADJ'),
        #     ('eles', 'PROPESS'), ('elas', 'PROPESS'),
        #     # Casos Átonos
        #     ('me', 'PROPESS'), ('te', 'PROPESS'), ('lhe', 'PROPESS'),
        #     ('se', 'PROPESS'), ('o', 'PROPESS'), ('a', 'PROPESS'),
        #     ('nos', 'PROPESS'), ('vos', 'PROPESS'), ('os', 'PROPESS'),
        #     ('as', 'PROPESS'), ('lhes', 'PROPESS')
        # ]
        # tagged_words = [(i[0].lower(), i[1]) for i in rp.tagged_words(t)]
        # pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        # try:
        #     obliques = map(tagged_words.count, obliques_list)
        #     return sum(list(obliques)) / ilen(pronouns)
        # except ZeroDivisionError:
        #     return 0
        ends = ['-me', '-te', '-o', '-a', '-nos',
                '-vos', '-os', '-as', '-lhe', '-lhes']
        atonos = ['me', 'te', 'o', 'a', 'nos', 'vos',
                        'os', 'as', 'lhe', 'lhes']
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        tagged = rp.tagged_words(t)
        occurances = 0
        occur = []
        for i in range(len(tagged) - 1):
            # VERBO + "-me, -te, -o, -a, -nos, -vos, -os, -as, -lhe, -lhes"
            if True in [tagged[i][0].endswith(e) for e in ends]:
                print(tagged[i])
                occurances += 1
                if occurances <= 12:
                    occur += [tagged[i][0]]
            # "me, te, o, a, nos, vos, os, as, lhe, lhes" + VERBO FLEXIONADO
            elif tagged[i][0] in atonos:
                if tagged[i+1][1] == 'V' and not tagged[i+1][0].endswith('r'):
                    print(tagged[i], print(tagged[i+1]))
                    occurances += 1
                    if occurances <= 12:
                        occur += [tagged[i][0]]
            # PREP + "ela, ele, nós, vós, eles, elas"
            elif tagged[i][1] == 'PREP' and tagged[i+1][1] == 'PROPESS':
                print(tagged[i], print(tagged[i+1]))
                occurances += 1
                if occurances <= 12:
                    occur += [tagged[i][0]]
        print(occur)
        try:
            return occurances / ilen(pronouns)
        except ZeroDivisionError:
            return 0


class DiscourseMarkersLevel4(base.Metric):
    """
    ## Razão de marcadores discursivos de nível 4 por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos de nível 4 para o número de
    sentenças do texto. Os marcadores são: pois, já, embora, também, não só,
    a fim de.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Discourse Markers Level 4 to All Clauses'
    column_name = 'discourse_markers_level_4'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        ocorrencias = sum(
            [
                lower.count('pois'),
                lower.count('já'),
                lower.count('embora'),
                lower.count('também'),
                lower.count('não só'),
                lower.count('a fim de')
            ]
        )
        if lower.count('pois') > 0:
            print('%d pois'%lower.count('pois'))
        if lower.count('já') > 0:
            print('%d já'%lower.count('já'))
        if lower.count('embora') > 0:
            print('%d embora'%lower.count('embora'))
        if lower.count('também') > 0:
            print('%d também'%lower.count('também'))
        if lower.count('não só') > 0:
            print('%d não só'%lower.count('não só'))
        if lower.count('a fim de') > 0:
            print('%d a fim de'%lower.count('a fim de'))
        clauses = flat.count(' V ') - flat.count('<aux>')
        try:
            return ocorrencias / clauses
        except ZeroDivisionError:
            return 0


class TalkToReader(base.Metric):
    """
    ## Taxa de pronomes pessoais que indicam uma conversa com o leitor.

    Calcula a razão entre o número de pronomes pessoais "eu", "tu", "você" e
    "vocês" para o número total de pronomes pessoais presentes no texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Você sabia que os dinossauros já dominaram o planeta Terra? Eles eram os
    grandes habitantes de todo o plante."*

    Com 2 pronomes pessoais (__Você__ e __Eles__) e 1 pronome que marca
    conversa com o leitor (__Você__), o valor da métrica é 0,5.
    """

    name = 'Pronouns that Delimits a Talk to Reader'
    column_name = 'dialog_pronoun_ratio'

    def value_for_text(self, t, rp=default_rp):
        words = [i.lower() for i in rp.all_words(t)]
        if words.count('eu') > 0:
            print('%d eu'%words.count('eu'))
        if words.count('tu') > 0:
            print('%d tu'%words.count('tu'))
        if words.count('você') > 0:
            print('%d você'%words.count('você'))
        if words.count('vocês') > 0:
            print('%d vocês'%words.count('vocês'))

        try:
            return sum(
                [
                    words.count('eu'),
                    words.count('tu'),
                    words.count('você'),
                    words.count('vocês'),
                ]
            ) / sum(
                [
                    words.count('eu'),
                    words.count('tu'),
                    words.count('você'),
                    words.count('vocês'),
                    words.count('ele'),
                    words.count('ela'),
                    words.count('nós'),
                    words.count('vós'),
                    words.count('eles'),
                    words.count('elas'),
                ])
        except ZeroDivisionError:
            return 0


class DiscourseVoices(base.Metric):
    """
    ## Razão de vozes no discurso (Polifonia) por todas as palavras do texto.

    Calcula a razão entre o número de vozes no discurso (Polifonia) e o
    número de palavras do texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Segundo o relato do delator da operação lava-jato, foi roubado
    dinheiro dos cofres públicos."*

    Com 17 palavras (considerando descontração do = de + o, da = de + a,
    e dos = de + os) e a presença de uma voz no discurso (__Segundo__), o
    valor da métrica é 0,05
    """

    name = 'Ratio of Discourse Voices to all Words'
    column_name = 'discourse_voices_ratio'

    def value_for_text(self, t, rp=default_rp):
        lower = t.raw_content.lower()
        flat = rp.palavras_flat(t)
        lines = flat.split('\n')
        ocorrencias = 0
        words = 0
        occur = []
        expression = re.compile('''
                                de=acordo|
                                afirma|
                                [segundo] <com>
                                ''',
                                re.VERBOSE)
        for line in lines:
            if len(line) > 10:
                words += 1
                ocorrencias += len(re.findall(expression, line))
                for i in re.findall(expression, line):
                    print(i)
                    if len(occur) < 12:
                        occur += [i]
        ocorrencias2 = sum(
            [
                lower.count('diz que'),
                lower.count('disse que'),
                lower.count('disseram'),
                lower.count('afirma'),
                lower.count('afirmam'),

            ]
        )
        if lower.count('diz que') > 0:
            print('%d diz que'%lower.count('diz que'))
            if len(occur) < 12:
                occur += ['diz que']
        if lower.count('disse que') > 0:
            print('%d disse que'%lower.count('disse que'))
            if len(occur) < 12:
                occur += ['disse que']
        if lower.count('disseram') > 0:
            print('%d disseram'%lower.count('disseram'))
            if len(occur) < 12:
                occur += ['disseram']
        if lower.count('afirma') > 0:
            print('%d afirma'%lower.count('afirma'))
            if len(occur) < 12:
                occur += ['afirma']
        if lower.count('afirmam') > 0:
            print('%d afirmam'%lower.count('afirmam'))
            if len(occur) < 12:
                occur += ['afirmam']
        print(occur)
        try:
            return (ocorrencias + ocorrencias2) / words
        except ZeroDivisionError:
            return 0


class NegationRatio(base.Metric):
    """
        ## Taxa de negação:

        Taxa de Negações. Consideramos como negações: não, nem, nenhum,
        nenhuma, nada, nunca e jamais.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        No exemplo aparecem 3 negações. Como o mesmo possui 38 palavras a
            Taxa de negações é 78,947 (número de negações/número de
            palavras).
    """

    name = 'Ratio of negations'
    column_name = 'negation_ratio'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        negations = rp.pos_tagger().tagset.NEGATIONS
        occurrences = [count_occurrences_for_all(sent, negations,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        negacao = [i[0][0] for i in negations]
        occur = []
        for sent in rp.tagged_sentences(t):
            for i, token in enumerate(sent):
                if token[0] in negacao:
                    new = []
                    for j in range(-2, 3):
                        try:
                            print(sent[i+j][0])
                            new += [sent[i+j][0]]
                        except:
                            pass
                    occur += [new]
        print(occur)
        return sum(occurrences) / len(rp.all_words(t)) \
            if len(rp.all_words(t)) else 0


class PassiveSentences(base.Metric):
    """
        ## Taxa de sentenças na voz passiva:

        Calcula-se a taxa de sentenças na voz passiva em relação a todas
        as sentenças do time.

        ### Exemplo:

        *"O menino colou na prova. No entanto, ele foi descoberto."*

        Com 2 sentenças, sendo 1 na voz passiva, o valor da métrica é 0,5.
    """

    name = 'Ratio of Passive Sentences'
    column_name = 'passive_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).split('\n')
        occurences = 0
        for i in range(len(flat) - 1):
            if flat[i].count('<aux>'):
                if flat[i + 1].count('V PCP'):
                    occurences += 1
                    print(flat[i])
                    print(flat[i+1])
        try:
            return occurences / (flat.count('</s>') - 1)
        except ZeroDivisionError:
            return 0


class DiscourseMarkersLevel5(base.Metric):
    """
    ## Razão de marcadores discursivos de nível 5 por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos de nível 5 para o número de
    sentenças do texto. Os marcadores são: até então, cerca de, caso, à tona,
    caso, bem como e outrossim.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Discourse Markers Level 5 to All Clauses'
    column_name = 'discourse_markers_level_5'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lower = t.raw_content.lower()
        ocorrencias = sum(
            [
                lower.count('até então'),
                lower.count('cerca de'),
                lower.count('caso '),
                lower.count('à tona'),
                lower.count('bem como'),
                lower.count('outrossim')
            ]
        )
        if lower.count('até então') > 0:
            print('%d até então' % lower.count('até então'))
        if lower.count('cerca de') > 0:
            print('%d cerca de' % lower.count('cerca de'))
        if lower.count('caso ') > 0:
            print('%d caso' % lower.count('caso '))
        if lower.count('à tona') > 0:
            print('%d à tona' % lower.count('à tona'))
        if lower.count('bem como') > 0:
            print('%d bem como' % lower.count('bem como'))
        if lower.count('outrossim') > 0:
            print('%d outrossim' % lower.count('outrossim'))
        clauses = flat.count(' V ') - flat.count('<aux>')
        try:
            return ocorrencias / clauses
        except ZeroDivisionError:
            return 0


class IndicativePerfectMoodRatio(base.Metric):
    """
    ## Taxa de Verbos Indicativos no Pretérito Perfeito Simples.

    Taxa de verbos indicativos no pretérito perfeito simples em um
    texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Tu foste mandado embora?"*

    Com 2 verbos (__foste__ e __mandado__) e 1 verbo indicativo no
    pretérito perfeito simples (__foste__), o valor da métrica é 0,500.
    """

    name = 'Ratio of Indicative Preterite Perfect Mood'
    column_name = 'indicative_preterite_perfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            return len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            return 0


class Manual(base.Category):
    name = 'Manual'
    table_name = 'manual'

    def __init__(self):
        super(Manual, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
