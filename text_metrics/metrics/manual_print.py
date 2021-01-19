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
import text_metrics
from text_metrics import base
from text_metrics.resource_pool import rp as default_rp
from text_metrics.utils import ilen, count_occurrences_for_all
from text_metrics.tools import pos_tagger
from text_metrics.metrics.basic_counts import Sentences
from text_metrics.metrics.anaphoras import AnaphoricReferencesBase
from text_metrics.metrics.anaphoras import AnaphoricReferencesBaseList
from text_metrics.metrics.ambiguity import AdjectiveAmbiguity, AdverbAmbiguity
from text_metrics.metrics.ambiguity import NounAmbiguity, VerbAmbiguity
from itertools import chain
import re


class SubjunctiveFutureVerbRatio(base.Metric):
    """
    ## Taxa de Verbos no Futuro do Subjuntivo.

    Taxa de verbos no futuro do subjuntivo em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Quando eu falar a verdade vocês vão me criticar."*

    Com 3 verbo (__falar__, __vão__ e __criticar__) e 1 verbo no subjuntivo
    (__falar__), o valor da métrica é 0,333.
    """

    name = 'Ratio of Future Imperfect mood'
    column_name = 'subjunctive_future_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*FUT.*SUBJ', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class SubjunctivePresentVerbRatio(base.Metric):
    """
    ## Taxa de Verbos no Presente do Subjuntivo.

    Taxa de verbos no presente do subjuntivo em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Espero que todos nós sejamos felizes"*

    Com 2 verbo (__Espero__ e __sejamos__) e 1 verbo no subjuntivo
    (__sejamos__), o valor da métrica é 0,5.
    """

    name = 'Ratio of Subjunctive Present mood'
    column_name = 'subjunctive_present_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*PR.*SUBJ', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class SubjunctiveImperfectVerbRatio(base.Metric):
    """
    ## Taxa de Verbos no Pretérito Imperfeito do Subjuntivo.

    Taxa de verbos no pretérito imperfeito do subjuntivo em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Se eu falasse a verdade ninguém acreditaria."*

    Com 2 verbo (__falasse__ e __acreditaria__) e 1 verbo no subjuntivo
    (__falasse__), o valor da métrica é 0,5.
    """

    name = 'Ratio of Subjunctive Imperfect mood'
    column_name = 'subjunctive_imperfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*IMPF.*SUBJ', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class IndicativeFutureMoodRatio(base.Metric):
    """
    ## Taxa de Verbos Indicativos no Futuro do Presente.

    Taxa de verbos indicativos no futuro do presente em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Trabalharei o dia todo."*

    Com 1 verbo (__trabalharei__) e 1 verbo indicativo no
    futuro do presente (__trabalharei__), o valor da métrica é 1.
    """

    name = 'Ratio of Indicative Future mood'
    column_name = 'indicative_future_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*FUT.*IND', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class IndicativeConditionVerbRatio(base.Metric):
    """
    ## Taxa de Verbos Indicativos no Futuro do Pretérito.

    Taxa de verbos indicativos no futuro do pretérito em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Trabalharia o dia todo."*

    Com 1 verbo (__trabalharia__) e 1 verbo indicativo no
    futuro do presente (__trabalharia__), o valor da métrica é 1.
    """

    name = 'Ratio of Indicative Condition Mood'
    column_name = 'indicative_condition_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*COND', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class IndicativePresentMoodRatio(base.Metric):
    """
    ## Taxa de Verbos Indicativos no Presente.

    Taxa de verbos indicativos no presente em um texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Acessório utilizado por adolescentes, o boné é um dos itens que
        compõem a vestimenta idealizada pela proposta."*

    Com 4 verbos (__utilizado__, __é__, __compõem__ e __idealizada__) e 1
    verbo no presente indicativo (__compõem__), o valor da métrica é 0,250.
    """

    name = 'Ratio of Indicative Present Mood'
    column_name = 'indicative_present_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*PR.*IND', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class IndicativeImperfectMoodRatio(base.Metric):
    """
    ## Taxa de Verbos no Pretérito Imperfeito Indicativo.

    Taxa de verbos no pretérito imperfeito indicativo.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser PALAVRAS.

    ### Exemplo:

    *"Ela fazia questão de tirar sempre dez."*

    Com 2 verbos (__fazia__ e __tirar__) e 1 verbo indicativo no
    pretérito imperfeito simples (__fazia__), o valor da métrica é 0,500.
    """

    name = 'Ratio of Indicative Imperfect Mood'
    column_name = 'indicative_imperfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*V.*IMPF.*IND', flat):
            if len(occur) < 12:
                occur += [i]
        return occur


class IndefinitePronounsDiversity(base.Metric):
    """
    ## Diversidade de pronomes indefinidos no texto.

    Calcula-se a diversidade de pronomes indefinidos no texto.

    ### Exemplo:

    *"A personagem foi atuada com perfeição. Ninguém imaginou que aquele era
    um ator substituto. Alguém tinha que atuar."*

    Com apenas 2 pronome indefinido (__Ninguém__ e __Alguém__) distintos, o
    valor da métrica é 0,5.
    """

    name = 'Indefinite Pronouns Diversity'
    column_name = 'indefinite_pronouns_diversity'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        nouns = filter(pos_tagger.tagset.is_pronoun, words)
        nouns = [n[0].lower() for n in nouns]
        indefinite_list = rp._pronomes_indefinidos()
        match = [n for n in nouns if n in indefinite_list]
        occur = []
        for i in match:
            if len(occur) < 12:
                occur += [i]
        return occur


# class EasyConjunctions(base.Metric):
#     """
#     ## Razão de palavras do texto que correspondem a conjunções fáceis.

#     Calcula-se a razão de palavras do texto que correspondem a conjunções
#     fáceis. A lista de conjunções fáceis foi compilada por Livia Cucatto com
#     base nas ocorrências do córpus da empresa.

#     ### Exemplo:

#     *"Eles brincaram o dia todo e foi muito divertido. Além disso, fizeram
#     muitos amigos."*

#     Com 14 palavras e 2 conjunções fáceis compostas ao todo por 3 palavras
#     (__e__ e __além disso__), o valor da métrica é 0,214.
#     """

#     name = 'Easy Conjunctions'
#     column_name = 'easy_conjunctions_ratio'

#     def value_for_text(self, t, rp=default_rp):
#         conj = rp._conjuncoes_fund1()
#         lower = ' '.join([' '] + [i.lower() for i in rp.all_words(t)] + [' '])
#         count = 0
#         occur = []
#         for c in conj:
#             count += lower.count(' ' + c + ' ') * len(c.split())
#             if lower.count(' ' + c + ' ') * len(c.split()) > 0:
#                 if len(occur) < 12:
#                     occur += [c]
#         #print(occur)
#         return occur


# class HardConjunctions(base.Metric):
#     """
#     ## Razão de palavras do texto que correspondem a conjunções difíceis.

#     Calcula-se a razão de palavras do texto que correspondem a conjunções
#     difíceis. A lista de conjunções difíceis foi compilada por Livia Cucatto
#     com base nas ocorrências do córpus da empresa.

#     ### Exemplo:

#     *"Visto que muitas pessoas sairam feridas, foi necessário tomar uma medida
#     imediata a fim de neutralizar os danos causados e reverter a situação."*

#     Com 23 palavras e 2 conjunções difíceis compostas ao todo por 5 palavras
#     (__a fim de__ e __visto que__), o valor da métrica é 0,217.
#     """

#     name = 'Hard Conjunctions'
#     column_name = 'hard_conjunctions_ratio'

#     def value_for_text(self, t, rp=default_rp):
#         conj = rp._conjuncoes_fund2()
#         lower = ' '.join([' '] + [i.lower() for i in rp.all_words(t)] + [' '])
#         count = 0
#         occur = []
#         for c in conj:
#             count += lower.count(' ' + c + ' ') * len(c.split())
#             if lower.count(' ' + c + ' ') * len(c.split()) > 0:
#                 if len(occur) < 12:
#                     occur += [c]
#         #print(occur)
#         return occur



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
                # print(i)
                occur += [i]
        return occur


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
                # print(i)
                occur += [i]
        return occur


class RatioOfPresentVerbs(base.Metric):
    """
        ## Razão de verbos no presente:

        Razão entre verbos no presente e todos os verbos no texto.

        Retorna um valor entre 0 e 1 que representa a razão entre a quantidade
        de verbos no presente e o total de verbos no texto.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        parser PALAVRAS.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Com 6 verbos (__podemos__, __acrescentar__, __temos__, __precisamos__ e
        __justifica__) e 4 verbos no presente (__podemos__, __temos__,
        __precisamos__ e __justifica__), o valor da métrica é 0,66.

    """

    name = 'Ratio of Present Tense Verbs to All Verbs'
    column_name = 'present_to_tenses_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present = len(re.findall('V.*PR', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present = 0
        try:
            imperfect = len(re.findall('V.*IMPF', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect = 0
        try:
            perfect = len(re.findall('V.*PS', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect = 0
        try:
            pluperfect = len(re.findall('V MQP', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect = 0
        try:
            future = len(re.findall('V.*FUT', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future = 0
        try:
            conditional = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional = 0
        tenses = [present, imperfect, perfect, pluperfect, future, conditional]
        # return tenses.index(max(tenses))
        occur = []
        count = 0
        for i in re.findall('\[(.*)\].*V.*PR', flat):
            # print(i)
            count += 1
            if count <= 12:
                occur += [i]
        return occur


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
            # print(i)
            count += 1
            if count <= 12:
                occur += [i[0]]
        # print(occur)
        return occur


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

    def calculate_ambiguity(self, rp, t, delaf_tag, tep_tag, checker):
        words = [word.lower() for (word, tag) in rp.tagged_words(t)
                 if checker((word, tag))]

        word_stems = [rp.stemmer().get_lemma(word, delaf_tag) for word in words]
        # word_stems = [word for word in word_stems if word is not None]

        meanings_count = [rp.db_helper().get_tep_words_count(stem, tep_tag)
                          for stem in word_stems]
        # meanings_count = [m for m in meanings_count if m is not None]

        # return sum(meanings_count) / len(words) if words else 0
        return [words[i] for i, m in enumerate(meanings_count) if m > 0]

    def value_for_text(self, t, rp=default_rp):
        adjectives = self.calculate_ambiguity(rp, t, 'A', 'Adjetivo',
                                              rp.pos_tagger().tagset.is_adjective)
        adverbs = self.calculate_ambiguity(rp, t, 'ADV', 'Advérbio',
                                           rp.pos_tagger().tagset.is_adverb)
        nouns = self.calculate_ambiguity(rp, t, 'N', 'Substantivo',
                                         rp.pos_tagger().tagset.is_noun)
        verbs = self.calculate_ambiguity(rp, t, 'V', 'Verbo',
                                         rp.pos_tagger().tagset.is_verb)
        # adjectives = AdjectiveAmbiguity().value_for_text(t)
        # adverbs = AdverbAmbiguity().value_for_text(t)
        # nouns = NounAmbiguity().value_for_text(t)
        # verbs = VerbAmbiguity().value_for_text(t)
        # palavras = len(rp.all_words(t))

        # print('adjetivos', adjectives)
        # print('adverbios', adverbs)
        # print('substantivos', nouns)
        # print('verbos', verbs)

        return [adjectives, adverbs, nouns, verbs]
        # try:
        #     return (adjectives + adverbs + nouns + verbs) / palavras
        # except:
        #     return 0


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
        occur = []
        for word in sw:
            if word in content_words:
                count += 1
                if count <= 12:
                    occur += [word]
        return occur


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
                # print(word)
                count += 1
                if count <= 12:
                    occur += [word]
        return occur


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
        # print('%d palavras e %d sentenças'%(Words().value_for_text(t), Sentences().value_for_text(t)))
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
            # print('%d não SVO de um total de %d orações'%(count, nverbs))
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
            # print(i)
            pass
        coord_clauses = flat.count(' KC ')
        subord_clauses = flat.count(' KS ')  # relativa explicativa
        rel = flat.count('<rel>')  # relativas restritivas
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
            # print(i)
            pass
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
            # print(i)
            pass
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),  # final
                lower.count('depois de'),  # temporal
                lower.count('depois que'),  # temporal
                lower.count('antes que'),  # condicional
                lower.count('sem que'),  # condicional
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
                # print(marcador)
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
            # print(i)
            pass
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
                # print(i)
                if count <= 12:
                    occur += [i]
                    # print(occur)
        return occur


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
            # print(i)
            pass
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),  # final
                lower.count('depois de'),  # temporal
                lower.count('depois que'),  # temporal
                lower.count('antes que'),  # condicional
                lower.count('sem que'),  # condicional
                lower.count('apesar que'),  # concessiva

            ]
        )
        if 'para que' in lower:
            # print('para que')
            pass
        if 'depois de' in lower:
            # print('depois de')
            pass
        if 'depois que' in lower:
            # print('depois que')
            pass
        if 'antes que' in lower:
            # print('antes que')
            pass
        if 'sem que' in lower:
            # print('sem que')
            pass
        if 'apesar que' in lower:
            # print('apesar que')
            pass
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


class DiscursivesMarks(base.Metric):
    """
    ## Marcadores Discursivos

    Essa métrica retorna a presença de marcadores de coesão profunda no texto.
    Esses marcadores fazem parte de uma lista pre-definida declarado na variavel
    marks'.

    """

    name = 'Discursive Marks'
    column_name = 'DiscursivesMarks'

    def value_for_text(self, t, rp=default_rp):
        marks = ['por um lado', 'por outro lado', 'em primeiro lugar', 'após', 'antes', 'depois', 'em seguida', 'seguidamente', 'até que', 'por último', 'para concluir', 'ou seja', 'isto é', 'quer dizer', 'por outras palavras', 'quer dizer', 'ou melhor', 'dizendo melhor', 'ou antes', 'como se pode ver', 'é o caso de', 'como vimos', 'quer isto dizer', 'significa isto que', 'não se pense que', 'pelo que referi anteriormente', 'de fato', 'na verdade', 'na realidade', 'com efeito', 'por exemplo', 'efetivamente', 'note-se que', 'repare-se', 'veja-se', 'mais concretamente', 'é evidente que', 'a meu ver', 'estou em crer que', 'em nosso entender', 'certamente', 'decerto', 'com toda a certeza', 'naturalmente', 'evidentemente', 'com isto', 'com isso', 'pretendemos', 'por outras palavras', 'ou seja', 'em resumo', 'em suma', 'em contrapartida', 'nem', 'tampouco', 'bem como', 'não só', 'mas também', 'além disso', 'mais ainda', 'igualmente', 'ainda', 'nesse cenário', 'nesse contexto', 'por ora', 'em vias de', 'com intuito de', 'em relação ao', 'ou', 'ora', 'seja', 'alternativamente', 'em alternativa', 'opcionalmente', 'mas', 'porém', 'todavia', 'contudo', 'no entanto', 'contrariamente', 'pelo contrário', 'embora', 'ainda que', 'mesmo que', 'conquanto', 'apesar de', 'malgrado', 'não obstante', 'mesmo assim', 'ainda assim', 'quando', 'mal', 'assim que', 'logo que', 'enquanto', 'entretanto', 'depois que', 'desde que', 'antes de', 'mais tarde', 'ao mesmo tempo', 'para', 'para que', 'a fim de', 'a fim de que', 'de modo', 'de forma a', 'com o objetivo de', 'com o propósito de', 'com vistas a', 'como', 'tal como', 'assim como', 'bem como', 'também', 'mais', 'menos do que', 'porque', 'visto que', 'dado que', 'como', 'uma vez que', 'já que', 'se', 'caso', 'desde que', 'a não ser que', 'contanto que', 'por isso', 'daí que', 'de tal forma', 'que', 'tanto', 'tal', 'tão', 'portanto', 'assim', 'logo', 'por conseguinte', 'concluindo', 'para concluir', 'em conclusão', 'em consequência', 'daí', 'então', 'deste modo', 'por isso', 'por este motivo', 'por esse motivo', 'dado que', 'por exemplo', 'a ilustrar', 'documentando', 'exemplificando', 'primeiro', 'primeiramente', 'em segundo lugar', 'em terceiro lugar', 'sintetizando', 'prosseguindo', 'concluindo', 'recapitulando', 'para começar', 'para concluir', 'a seguir', 'para encerrar', 'em seguida', 'concomitantemente', 'paralelamente', 'sobretudo', 'além de tudo', 'acima']
        result = set()

        for mark in marks:
            if mark in t.raw_content:
                result.add(mark)

        return list(result)


class AdjacentDemonstrativePronounList(base.Metric):
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

    name = '''Ratio of candidates of demonstrative pronouns to anaphoric
            reference in adjacente sentences'''
    column_name = 'demonstrative_pronoun_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if sentence.count('<dem>') > 0:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                iterator = iter(range(len(content)))
                for i in iterator:
                    if content[i].strip() != '' and '<dem>' in content[i]:
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()

                        if i - 1 >= 0:
                            prefix = content[i - 1].replace("b\'", "")
                            prefix = self.treat_fix(prefix)
                            if '=' in prefix:
                                prefix = prefix.replace('=', ' ').split(' ')[1] + ' '

                        if i + 1 < len(content):
                            sufix = content[i + 1].replace("b\'", "")
                            sufix = self.treat_fix(sufix)
                            if '<dem>' in content[i + 1].replace("b\'", ""):
                                sufix = ' ' + sufix + self.treat_fix(content[i + 2].replace("b\'", "")).strip()
                                next(iterator, None)
                            else:
                                sufix = ' ' + sufix

                            if '=' in sufix:
                                sufix = ' ' + sufix.replace('=', ' ').split(' ')[1]

                            for point in points:
                                if point in sufix:
                                    if len(sufix.strip()) == 1:
                                        sufix = sufix.strip() + ' '
                                    else:
                                        sufix = sufix + ' '
                                    break

                        if len(sufix) > 2:
                            sufix = sufix.rstrip()

                        value = prefix + line.split('\t')[0].strip() + sufix

                        if '--' in value:
                            value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                        result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


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
            # print(i)
            pass
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
            # print(i)
            count += 1
            if count <= 12:
                occur += [i]
        # print(occur)
        return occur


class AdjectivesNlpNet2(base.Metric):
    name = "adjectives nlpnet2"
    column_name = "teste"

    def value_for_text(self, text, rp=default_rp):
        # tagged = rp.tagged_words(text) #return only words outside of sentences, no pontuation.
        tagged = rp.tagged_tokens(text)  # same above + pontuation
        # tagged3 = rp.tagged_sentences(text) #return sentences with words tagged inside + pontuation.

        iterator = iter(range(len(tagged)))
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for i in iterator:
            if tagged[i][1] == 'ADJ':
                if i - 1 >= 0:
                    prefix = tagged[i - 1][0]
                    prefix = self.treat_fix(prefix)

                if i + 1 < len(tagged):
                    sufix = tagged[i + 1][0]
                    sufix = self.treat_fix(sufix).strip()
                    if 'ADJ' in tagged[i + 1][1]:
                        sufix = ' ' + sufix + self.treat_fix(tagged[i + 2][0]).strip()
                        next(iterator, None)
                    else:
                        sufix = ' ' + sufix

                    for point in points:
                        if point in sufix:
                            if len(sufix.strip()) == 1:
                                sufix = sufix.strip() + ' '
                            else:
                                sufix = sufix + ' '
                            break

                value = prefix + tagged[i][0].strip() + sufix

                if '--' in value:
                    value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class AdjectivesNlpNet(base.Metric):
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
        for i in adjectives:
            occur.append(i[0])

        return occur


class PalavrasResult(base.Metric):
    name = 'Palavras Result'
    column_name = 'Result of the Palavras'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')

        return flat


class AdjectivesPalavras(base.Metric):
    name = 'Adjective Ratio'
    column_name = 'adjective_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if sentence.count(' ADJ ') > 0:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                for i in range(len(content) - 1):
                    if content[i].strip() != '' and ' ADJ ' in content[i]:
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()

                        result.append(line.split('\t')[0].strip())

        return result


class AdjectivesList(base.Metric):
    name = 'Adjectives List'
    column_name = 'adjectives List'

    def value_for_text(self, t, rp=default_rp):
        result = []

        resultA = Adjectives(t).value_for_text(t)
        resultB = AdjectivesNlpNet2(t).value_for_text(t)

        for a in resultA:
            result.append(a)

        for b in resultB:
            if result.count(b) <= 0:
                result.append(b)

        return result


class Adjectives(base.Metric):
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
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if sentence.count(' ADJ ') > 0:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                iterator = iter(range(len(content)))
                for i in iterator:
                    if content[i].strip() != '' and ' ADJ ' in content[i]:
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()

                        if i - 1 >= 0:
                            prefix = content[i - 1].replace("b\'", "")
                            prefix = self.treat_fix(prefix)

                        if i + 1 < len(content):
                            sufix = content[i + 1].replace("b\'", "")
                            sufix = self.treat_fix(sufix).strip()
                            if ' ADJ ' in content[i + 1].replace("b\'", ""):
                                sufix = ' ' + sufix + self.treat_fix(content[i + 2].replace("b\'", "")).strip()
                                next(iterator, None)
                            else:
                                sufix = ' ' + sufix

                            for point in points:
                                if point in sufix:
                                    if len(sufix.strip()) == 1:
                                        sufix = sufix.strip() + ' '
                                    else:
                                        sufix = sufix + ' '
                                    break

                        value = prefix + line.split('\t')[0].strip() + sufix

                        if '--' in value:
                            value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                        result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class WordsBeforeMainVerbs(base.Metric):
    """
        ## Palavras Antes de Verbos Principais:

        Média de palavras antes de verbos principais na cláusula principal da
        sentença. Segundo a documentação do Coh-Metrix é um bom índice para
        avaliar a carga da memória de trabalho.

        O desempenho da métrica é diretamente relacionada as árvores sintáticas
        de dependência geradas pelo MaltParser e ao POS tagger do nlpnet.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Como este texto possui uma sentença o valor desta métrica
            corresponde ao valor de palavras antes do verbo desta única
            sentença que, neste caso, é 1 (a palavra acessório é a única que
            antecede o verbo).
    """

    name = 'Mean words before main verb of sentences'
    column_name = 'words_before_main_verb'

    def value_for_text(self, t, rp=default_rp):
        result = {}
        words = []
        trees = rp.dep_trees(t)

        for tree in trees:
            for node in tree.nodes:
                if tree.nodes[node]['tag'] == 'VERB':
                    result[tree.nodes[node]['word']] = words.copy()
                    words.clear()

                if tree.nodes[node]['word'] != None:
                    words.append(tree.nodes[node]['word'])

            words.clear()

        return result


class LogicOperator(base.Metric):
    """
        ## Taxa de Operadores Lógicos:

        Taxa de operadores lógicos em um texto. Consideramos como
        operadores lógicos: e, ou, se, negações e um número de condições.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Como há 4 operadores lógicos e 38 palavras a Taxa de
            operadores lógicos é 105,26 (número de operadores lógicos/número
            de palavras).
    """

    name = 'Logic operators Ratio'
    column_name = 'logic_operators'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        # adverbs = filter(pos_tagger.tagset.is_adverb, rp.tagged_words(t))
        # occur = set()
        logic_operators = rp.pos_tagger().tagset.LOGIC_OPERATORS
        # taggedSentences = rp.tagged_sentences(t)

        return logic_operators


class AdverbsInTextList(base.Metric):
    name = 'Adverbs List'
    column_name = 'adverbs list'

    def value_for_text(self, t, rp=default_rp):
        result = []

        resultA = AdverbsInText(t).value_for_text(t)
        resultB = AdverbsInTextNlpNet(t).value_for_text(t)

        for a in resultA:
            result.append(a)

        for b in resultB:
            if result.count(b) <= 0:
                result.append(b)

        return result


class AdverbsInText(base.Metric):
    """
        ## Taxa de Advérbios:

        Taxa de advérbios em um texto.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        POS tagger do nlpnet.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Com 8 advérbios (__não__, __a__, __mais__, __já__, __não__, __por__,
        __exemplo__, __também__) e 38 palavras, a Taxa de adjetivos é
        210,526 (número de advérbios/número de palavras).
    """

    name = 'Adverbs'
    column_name = 'adverbs'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if sentence.count(' ADV ') > 0:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                iterator = iter(range(len(content)))
                for i in iterator:
                    if content[i].strip() != '' and ' ADV ' in content[i]:
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()
                        line = line.split('\t')[0]

                        if i - 1 >= 0:
                            prefix = content[i - 1].replace("b\'", "")
                            prefix = self.treat_fix(prefix)

                        if i + 1 < len(content):
                            sufix = content[i + 1].replace("b\'", "")
                            sufix = self.treat_fix(sufix).strip()
                            if i + 2 < len(content):
                                if ' ADV ' in content[i + 1]:
                                    sufix = sufix + ' ' + self.treat_fix(content[i + 2]).strip()
                                    next(iterator, None)
                                    next(iterator, None)

                            for point in points:
                                if point in sufix:
                                    line = line.strip()
                                    if len(sufix.strip()) == 1:
                                        sufix = sufix.strip() + ' '
                                    else:
                                        sufix = sufix.lstrip() + ' '
                                    break

                        if len(sufix) > 2:
                            sufix = sufix.rstrip()

                        value = prefix + line + sufix

                        if '--' in value:
                            value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                        result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class AdverbsInTextNlpNet(base.Metric):
    name = "Adverbs NLPNET"
    column_name = "Adverbs NLPNET"

    def value_for_text(self, text, rp=default_rp):
        # tagged = rp.tagged_words(text) #return only words outside of sentences, no pontuation.
        tagged = rp.tagged_tokens(text)  # same above + pontuation
        # tagged3 = rp.tagged_sentences(text) #return sentences with words tagged inside + pontuation.

        iterator = iter(range(len(tagged)))
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for i in iterator:
            if tagged[i][1] == 'ADV':
                value2 = tagged[i][0] + ' '
                if i - 1 >= 0:
                    prefix = tagged[i - 1][0]
                    prefix = self.treat_fix(prefix)

                if i + 1 < len(tagged):
                    sufix = tagged[i + 1][0]
                    sufix = self.treat_fix(sufix).strip()
                    if i + 2 < len(tagged):
                        if 'ADV' == tagged[i + 1][1]:
                            sufix = sufix + ' ' + self.treat_fix(tagged[i + 2][0]).strip()
                            next(iterator, None)
                            next(iterator, None)

                    for point in points:
                        if point in sufix:
                            if len(sufix.strip()) == 1:
                                value2 = value2.strip()
                                sufix = sufix.strip() + ' '
                            else:
                                if ' .' in sufix:
                                    sufix = sufix.replace(' .', '. ')
                            break

                value = prefix + value2 + sufix

                if '--' in value:
                    value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class VerbsInText(base.Metric):
    name = 'Verbs'
    column_name = 'Verbs in text'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if sentence.count(' V ') > 0:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                iterator = iter(range(len(content)))
                for i in iterator:
                    if content[i].strip() != '' and ' V ' in content[i]:
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()

                        if i - 1 >= 0:
                            prefix = content[i - 1].replace("b\'", "")
                            prefix = self.treat_fix(prefix)
                            if '=' in prefix:
                                prefix = prefix.replace('=', ' ').split(' ')[1] + ' '

                        if i + 1 < len(content):
                            sufix = content[i + 1].replace("b\'", "")
                            sufix = self.treat_fix(sufix)
                            if ' V ' in content[i + 1].replace("b\'", ""):
                                sufix = ' ' + sufix + self.treat_fix(content[i + 2].replace("b\'", "")).strip()
                                next(iterator, None)
                            else:
                                sufix = ' ' + sufix

                            if '=' in sufix:
                                sufix = ' ' + sufix.replace('=', ' ').split(' ')[1]

                            for point in points:
                                if point in sufix:
                                    if len(sufix.strip()) == 1:
                                        sufix = sufix.strip() + ' '
                                    else:
                                        sufix = sufix + ' '
                                    break

                        if len(sufix) > 2:
                            sufix = sufix.rstrip()

                        value = prefix + line.split('\t')[0].strip() + sufix

                        if '--' in value:
                            value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                        if '-' in value:
                            part = value.partition('-')
                            value = part[0].strip() + part[1] + part[2].strip() + ' '

                        result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class HypernymsVerbsManual(base.Metric):
    """
        ## Hiperônimos de Verbos:

        Para cada verbo soma-se o número de hiperônimos e divide o total pelo
        número de verbos. Hiperonímia é uma relação, definida na Wordnet.Br
        (Dias-da-Silva et. al., 2002; Dias-da-Silva, 2003; Dias-da-Silva, 2005;
        Dias-da-Silva et. al., 2008 e Scarton e Aluísio, 2009), de "super tipo
        de". O verbo sonhar, por exemplo, possui 3 hiperônimos: imaginar,
        conceber e ver na mente.

        O desempenho da métrica é diretamente relacionado ao desempenho da
        base Wordnet.Br.

        ### Exemplo:

        *"Ele sonha muito quando está acordado."*

        O verbo sonhar possui 3 hiperônimos e o verbo acordar nenhum.
            Assim, temos o valor de 1,5.
    """

    name = 'Mean number of Wordnet.Br hypernyms per verb'
    column_name = 'hypernyms_verbs'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        verb_tokens = [token[0] for token in rp.tagged_words(t)
                       if rp.pos_tagger().tagset.is_verb(token)
                       or rp.pos_tagger().tagset.is_auxiliary_verb(token)
                       or rp.pos_tagger().tagset.is_participle(token)]
        verbs = [rp.db_helper().get_delaf_verb(verb) for verb in verb_tokens]
        lemmas = [verb.lemma for verb in verbs if verb is not None]
        hyper = [rp.db_helper().get_hypernyms(lemma) for lemma in lemmas]

        result = set()

        for h in hyper:
            for v in verbs:
                if v is not None and \
                                h is not None and \
                                h.word == v.lemma:
                    result.add((v.word, h.hyper_levels))

        return result


class ParticipleVerbsInText(base.Metric):
    """
        ## Taxa de verbos no particípio:

        Calcula-se a a Taxa de verbos no particípio em relação a todos os
        verbos do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"Se colasse poderia ter sido descoberto e ainda zerado a prova."*

        De 6 verbos (__colasse__, __poderia__, __ter__ , __sido__,
        __descoberto__ e __zerado__) temos 3 no particípio (__sido__,
        __descoberto__ e __zerado__), resultando no valor da métrica de 0,5.
    """

    name = 'Ratio of Participle Verbs'
    column_name = 'participle_verbs'

    def value_for_text(self, t, rp=default_rp):
        words = []
        trees = rp.dep_trees(t)

        for tree in trees:
            for node in tree.nodes:
                if tree.nodes[node]['tag'] == 'PCP':
                    words += node.word

        return words


class GerundVerbsInText(base.Metric):
    """
        ## Taxa de verbos no gerúndio:

        Calcula-se a a Taxa de verbos no gerúndio em relação a todos os
        verbos do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"O menino está colando para a prova e por isso acreditamos que ele não
        irá bem."*

        De 4 verbos (__está__, __colando__, __acreditamos__ e __irá__) temos 1
        no gerúndio (__colando__), resultando no valor da métrica de 0,25.
    """

    name = 'Ratio of Gerund Verbs'
    column_name = 'gerund_verbs'

    def value_for_text(self, t, rp=default_rp):
        words = []
        trees = rp.dep_trees(t)

        for tree in trees:
            for node in tree.nodes:
                if tree.nodes[node]['tag'] == 'GER':
                    words += node.word

        return words


class SentencesWithOneClauseList(base.Metric):
    """
        ## Taxa de sentenças que contenham apenas 1 oração:

        Calcula-se a Taxa de sentenças com 1 oração, sobre todas as
        sentenças do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"O menino colou na prova. No entanto, ele foi descoberto e se deu
        mal."*

        Com 2 sentenças, sendo que 1 possui apenas uma oração, o valor da
        métrica é 0,5.
    """

    name = 'Ratio of Sentences With One Clause'
    column_name = 'sentences_with_one_clause'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        sentences = flat.split('</s>')[:-2]
        phrase = ''
        result = []

        for sentence in sentences:
            if sentence.count(' V ') - sentence.count('<aux>') == 1:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                phrase = ''
                for line in content:
                    line = line.replace("b\'", "")
                    if line.strip() != '':
                        line = line.replace("<s>", "").replace("</s>", "").strip()
                        if '$' in line:
                            phrase = phrase.strip()
                            phrase += line[:2].replace('$', "")
                            if '.' not in line:
                                phrase = phrase + ' '
                        else:
                            phrase += line.split('\t')[0].strip() + ' '

                result.append(phrase.strip())

        return result


class SentencesWithMoreThanOneClauseList(base.Metric):
    """
        ## Taxa de sentenças que contenham 7 ou mais orações:

        Calcula-se a Taxa de sentenças com 7 ou mais orações, sobre todas
        as sentenças do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"O menino colou na prova. No entanto, ele foi descoberto e se deu
        mal."*

        Com 2 sentenças, sendo que nenhuma possui 7 ou mais orações, o valor da
        métrica é 0,0.
    """
    name = 'Ratio of Sentences With Seven More Clauses'
    column_name = 'sentences_with_seven_more_clauses'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        sentences = flat.split('</s>')[:-2]
        result = []

        for sentence in sentences:
            if sentence.count(' V ') - sentence.count('<aux>') > 1:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                phrase = ''
                for line in content:
                    line = line.replace("b\'", "")
                    if line.strip() != '':
                        line = line.replace("<s>", "").replace("</s>", "").strip()
                        if '$--' in line:
                            phrase += '–'
                            phrase = ' ' + phrase + ' '
                        elif '$' in line:
                            phrase = phrase.strip()
                            phrase += line[:2].replace('$', "")
                            if '.' not in line:
                                phrase = phrase + ' '
                        else:
                            phrase += line.split('\t')[0].strip() + ' '

                result.append(phrase.strip().replace('=', ' '))

        return result


class NumberOfSentences(base.Metric):
    """
        retorna o numero de sentencas do texto.
    """

    name = 'Number of sentences of a text.'
    column_name = 'number_of_sentences'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        sentences = flat.split('</s>')[:-2]

        return len(sentences)


class NumberOfWordsRegex(base.Metric):
    """
        retorna o numero de sentencas do texto.
    """

    name = 'Number of words of a text using regex.'
    column_name = 'number_of_words_regex'

    def value_for_text(self, t, rp=default_rp):

        if isinstance(t, str):
            value = t
        else:
            value = t.raw_content

        words = re.findall('\w+', value)

        return words


class NumberOfWordsByPalavras(base.Metric):
    """
        retorna o numero de sentencas do texto.
    """

    name = 'Number of words of a text using palavras and nlpnet.'
    column_name = 'number_of_words_palavras'

    def value_for_text(self, t, rp=default_rp):
        result = rp.all_words(t)
        # tagged = rp.tagged_words(t)

        return result


class ObliquePronounsList(base.Metric):
    name = 'Count of Oblique Pronouns'
    column_name = 'oblique_pronouns_count'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t).replace('\monit\n', '\n')
        sentences = flat.split('</s>')[:-2]
        points = [',', '.', '!', '?', ':', ';']
        prefix = ' '
        sufix = ' '
        result = []

        for sentence in sentences:
            if ' PERS ' in sentence and (' ACC ' in sentence or ' DAT ' in sentence):
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                iterator = iter(range(len(content)))
                for i in iterator:
                    if content[i].strip() != '':
                        line = content[i].replace("b\'", "")
                        line = line.replace("<s>", "").replace("</s>", "").strip()
                        line = line.split('\t')[0]

                        if '-' in line \
                                and i + 1 < len(content) \
                                and ' PERS ' in content[i + 1] \
                                and (' ACC ' in content[i + 1] or ' DAT ' in content[i + 1]):
                            line = line + content[i + 1].split('\t')[0]
                            if i + 2 < len(content):
                                sufix = content[i + 2].replace("b\'", "")
                                sufix = self.treat_fix(sufix).strip()

                        if i - 1 >= 0:
                            prefix = content[i - 1].replace("b\'", "")
                            prefix = self.treat_fix(prefix)

                        if i + 1 < len(content) and sufix.strip() != '':
                            sufix = content[i + 1].replace("b\'", "")
                            sufix = self.treat_fix(sufix).strip()
                            if i + 2 < len(content):
                                if ' PERS ' in content[i + 1] \
                                        and (' ACC ' in content[i + 1]
                                             or ' DAT ' in content[i + 1]):
                                    sufix = sufix + ' ' + self.treat_fix(content[i + 2]).strip()
                                    next(iterator, None)
                                    next(iterator, None)

                            for point in points:
                                if point in sufix:
                                    line = line.strip()
                                    if len(sufix.strip()) == 1:
                                        sufix = sufix.strip() + ' '
                                    else:
                                        sufix = sufix.lstrip() + ' '
                                    break

                        if len(sufix) > 2:
                            sufix = sufix.rstrip()

                        value = prefix + line + sufix

                        if '--' in value:
                            value = value.replace('$--', ' \u2013 ').strip()  # \u2013 ( - en dash ascii) travessao

                        result.append(value)

        return result

    def treat_fix(self, value):
        result = value.split('\t')[0].strip()

        if '$' in result:
            result = result.strip()
            result = result[:2].replace('$', "")

        result = result + ' '

        return result


class ObliquePronounsCount(base.Metric):
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

    name = 'Count of Oblique Pronouns'
    column_name = 'oblique_pronouns_count'

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
        ends = ['-me', '-te', '-o', '-no', '-lo', '-a', '-na', '-la', '-nos',
                '-vos', '-os', '-nos', '-as', '-nas', '-las', '-lhe',
                '-lhes', '-los', '-ei', '-eis']
        atonos = ['me', 'te', 'o', 'a', 'nos', 'vos',
                  'os', 'as', 'lhe', 'lhes']
        tagged = rp.tagged_words(t)
        occurances = []
        prefix = ''
        sufix = ' '

        for i in range(len(tagged) - 1):
            if i - 1 >= 0:
                prefix = tagged[i - 1][0]
            if i + 1 < len(tagged):
                sufix = tagged[i + 1][0]

            if sufix[0].isupper():
                sufix = ''
            if tagged[i][0][0].isupper():
                prefix = ''

            # VERBO + "-me, -te, -o, -a, -na, -no, -la, -lo, -nos, -vos, -os, -nas, -nos, -las, -los, -as, -lhe, -lhes"
            if True in [tagged[i][0].endswith(e) for e in ends]:
                occurances.append(prefix + ' ' + tagged[i][0] + ' ' + sufix)
            # "me, te, o, a, nos, vos, os, as, lhe, lhes" + VERBO FLEXIONADO
            elif tagged[i][0] in atonos:
                if tagged[i + 1][1] == 'V' and not tagged[i + 1][0].endswith('r'):
                    occurances.append(prefix + ' ' + tagged[i][0] + ' ' + sufix)
            # PREP + "ela, ele, nós, vós, eles, elas"
            elif tagged[i][1] == 'PREP' and tagged[i + 1][1] == 'PROPESS':
                if i + 2 < len(tagged):
                    sufix = tagged[i + 2][0]
                if tagged[i][0][0].isupper():
                    prefix = ''
                occurances.append(prefix + ' ' + tagged[i][0] + ' ' + tagged[i + 1][0] + ' ' + sufix)

        return occurances


class RelativePronounsCount(base.Metric):
    """
    ## Taxa de Pronomes Relativos.

    Calcula a taxa de pronomes relativos em relação a todos os pronomes do
    texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    POS tagger do nlpnet.

    ### Exemplo:

    *"Regressando de São Paulo, visitei o sítio de minha tia, o qual me
    deixou encantado. Era exatamente o que eu esperava, apesar de nunca ter
    imaginado que eu estaria ali."*

    Com 2 ocorrências de pronomes relativos (__o qual__ e __que__) e um total
    de 9 pronomes (__minha__, __o__, __qual__, __me__, __o__, __que__, __eu__,
    __que__ e __eu__), o valor da métrica é 0,222.
    """

    name = 'Count of Relative Pronouns'
    column_name = 'relative_pronouns_count'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        sentences = flat.split('</s>')[:-2]
        relativos = []

        for sentence in sentences:
            if sentence.count('<rel>') >= 1:
                phrase = sentence.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                content = phrase.split('\n')[:-1]
                for i in range(len(content)):
                    value = ''
                    if "<rel>" in content[i]:
                        if i - 1 >= 0 and i + 1 < len(content):
                            prefix = content[i - 1].split('\t')[0].strip() + ' '
                            if "$" in prefix:
                                prefix = ''

                            sufix = content[i + 1].split('\t')[0].strip()
                            if "$" in sufix:
                                sufix = ''

                            value = prefix + \
                                    content[i].split('\t')[0].strip() + \
                                    ' ' + sufix
                        elif i - 1 >= 0 and i + 1 > len(content):
                            prefix = content[i - 1].split('\t')[0].strip() + ' '
                            if "$" in prefix:
                                prefix = ''

                            value = prefix + \
                                    ' ' + content[i].split('\t')[0].strip()
                        elif i - 1 < 0 and i + 1 < len(content):
                            sufix = content[i + 1].split('\t')[0].strip()
                            if "$" in sufix:
                                sufix = ''

                            value = content[i].split('\t')[0].strip() + \
                                    ' ' + sufix

                        if '-' in value:
                            value += content[i + 2].split('\t')[0].strip()

                        value = value.replace('=', ' ')
                        relativos.append(value)

        return relativos


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
            # print(i)
            pass
        # casos não capturados por expressão regular
        ocorrencias2 = sum(
            [
                lower.count('para que'),  # final
                lower.count('depois de'),  # temporal
                lower.count('depois que'),  # temporal
                lower.count('antes que'),  # condicional
                lower.count('sem que'),  # condicional
                lower.count('apesar que'),  # concessiva
                lower.count('tamanho que'),  # consecutiva
                lower.count('tal que'),  # consecutiva
                lower.count('tanto que'),  # consecutiva

            ]
        )
        if 'para que' in lower:
            # print('para que')
            pass
        if 'depois de' in lower:
            # print('depois de')
            pass
        if 'depois que' in lower:
            # print('depois que')
            pass
        if 'antes que' in lower:
            # print('antes que')
            pass
        if 'sem que' in lower:
            # print('sem que')
            pass
        if 'apesar que' in lower:
            # print('apesar que')
            pass
        if 'tamanho que' in lower:
            # print('tamanho que')
            pass
        if 'tal que' in lower:
            # print('tal que')
            pass
        if 'tanto que' in lower:
            # print('tanto que')
            pass
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


# class DiscourseMarkersLevel3(base.Metric):
#     """
#     ## Razão de marcadores discursivos de nível 3 por número de orações do
#     texto.

#     Calcula a proporção de marcadores discursivos de nível 3 para o número de
#     sentenças do texto. Os marcadores são: não bastasse, além de, de volta e
#     até.

#     O desempenho da métrica é diretamente relacionado ao desempenho do
#     POS tagger do nlpnet.

#     ### Exemplo:
#     *""*
#     """

#     name = '''Ratio of Discourse Markers Level 3 to All Clauses'''
#     column_name = 'discourse_markers_level_3'

#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('não bastasse'),
#                 lower.count('além de'),
#                 lower.count('de volta'),
#                 lower.count('até'),
#             ]
#         )
#         if lower.count('não bastasse') > 0:
#             #print('%d não bastasse'%lower.count('não bastasse'))
#             pass
#         if lower.count('além de') > 0:
#             #print('%d além de'%lower.count('além de'))
#             pass
#         if lower.count('de volta') > 0:
#             #print('%d de volta'%lower.count('de volta'))
#             pass
#         if lower.count('até') > 0:
#             #print('%d até'%lower.count('até'))
#             pass
#         clauses = flat.count(' V ') - flat.count('<aux>')
#         try:
#             return ocorrencias / clauses
#         except ZeroDivisionError:
#             return 0


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
                # print(tagged[i])
                occurances += 1
                if occurances <= 12:
                    occur += [tagged[i][0]]
            # "me, te, o, a, nos, vos, os, as, lhe, lhes" + VERBO FLEXIONADO
            elif tagged[i][0] in atonos:
                if tagged[i + 1][1] == 'V' and not tagged[i + 1][0].endswith('r'):
                    # print(tagged[i], #print(tagged[i+1]))
                    occurances += 1
                    if occurances <= 12:
                        occur += [tagged[i][0]]
            # PREP + "ela, ele, nós, vós, eles, elas"
            elif tagged[i][1] == 'PREP' and tagged[i + 1][1] == 'PROPESS':
                # print(tagged[i], #print(tagged[i+1]))
                occurances += 1
                if occurances <= 12:
                    occur += [tagged[i + 1][0]]
        # print(occur)
        return occur


# class DiscourseMarkersLevel4(base.Metric):
#     """
#     ## Razão de marcadores discursivos de nível 4 por número de orações do
#     texto.

#     Calcula a proporção de marcadores discursivos de nível 4 para o número de
#     sentenças do texto. Os marcadores são: pois, já, embora, também, não só,
#     a fim de.

#     O desempenho da métrica é diretamente relacionado ao desempenho do
#     POS tagger do nlpnet.

#     ### Exemplo:
#     *""*
#     """

#     name = 'Ratio of Discourse Markers Level 4 to All Clauses'
#     column_name = 'discourse_markers_level_4'

#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('pois'),
#                 lower.count('já'),
#                 lower.count('embora'),
#                 lower.count('também'),
#                 lower.count('não só'),
#                 lower.count('a fim de')
#             ]
#         )
#         if lower.count('pois') > 0:
#             #print('%d pois'%lower.count('pois'))
#             pass
#         if lower.count('já') > 0:
#             #print('%d já'%lower.count('já'))
#             pass
#         if lower.count('embora') > 0:
#             #print('%d embora'%lower.count('embora'))
#             pass
#         if lower.count('também') > 0:
#             #print('%d também'%lower.count('também'))
#             pass
#         if lower.count('não só') > 0:
#             #print('%d não só'%lower.count('não só'))
#             pass
#         if lower.count('a fim de') > 0:
#             #print('%d a fim de'%lower.count('a fim de'))
#             pass
#         clauses = flat.count(' V ') - flat.count('<aux>')
#         try:
#             return ocorrencias / clauses
#         except ZeroDivisionError:
#             return 0


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
            # print('%d eu'%words.count('eu'))
            pass
        if words.count('tu') > 0:
            # print('%d tu'%words.count('tu'))
            pass
        if words.count('você') > 0:
            # print('%d você'%words.count('você'))
            pass
        if words.count('vocês') > 0:
            # print('%d vocês'%words.count('vocês'))
            pass

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
                    # print(i)
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
            # print('%d diz que'%lower.count('diz que'))
            if len(occur) < 12:
                occur += ['diz que']
        if lower.count('disse que') > 0:
            # print('%d disse que'%lower.count('disse que'))
            if len(occur) < 12:
                occur += ['disse que']
        if lower.count('disseram') > 0:
            # print('%d disseram'%lower.count('disseram'))
            if len(occur) < 12:
                occur += ['disseram']
        if lower.count('afirma') > 0:
            # print('%d afirma'%lower.count('afirma'))
            if len(occur) < 12:
                occur += ['afirma']
        if lower.count('afirmam') > 0:
            # print('%d afirmam'%lower.count('afirmam'))
            if len(occur) < 12:
                occur += ['afirmam']
        # print(occur)
        return occur


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
                            # print(sent[i+j][0])
                            new += [sent[i + j][0]]
                        except:
                            pass
                    occur += [new]
        return occur


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
        occur = []
        for i in range(len(flat) - 1):
            if flat[i].count('<aux>'):
                if flat[i + 1].count('V PCP'):
                    occurences += 1
                    aux = re.findall('\[(.*)\].*<aux>', flat[i])[0]
                    main = re.findall('\[(.*)\].*V PCP', flat[i + 1])[0]
                    occur.append([aux, main])
        return occur


class AppositionPerClause(base.Metric):
    """
        ## Média de apostos especificadores por oração:

        Calcula-se a média de apostos especificadores por oração entre as
        orações do texto.

        O desempenho da métrica é diretamente relacionado ao desempenho das
        árvores flat geradas pelo parser PALAVRAS.

        ### Exemplo:

        *"A prova mais difícil que eu fiz, a de matemática, foi fácil."*

        Com 2 orações e 1 aposto especificador, a métrica vale 0,5.
    """

    name = 'Mean Apposition Per Clause'
    column_name = 'apposition_per_clause'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        occur = []
        for i in re.findall('\[(.*)\].*APP', flat):
            occur += [i]
        return occur


# class DiscourseMarkersLevel5(base.Metric):
#     """
#     ## Razão de marcadores discursivos de nível 5 por número de orações do
#     texto.

#     Calcula a proporção de marcadores discursivos de nível 5 para o número de
#     sentenças do texto. Os marcadores são: até então, cerca de, caso, à tona,
#     caso, bem como e outrossim.

#     O desempenho da métrica é diretamente relacionado ao desempenho do
#     POS tagger do nlpnet.

#     ### Exemplo:
#     *""*
#     """

#     name = 'Ratio of Discourse Markers Level 5 to All Clauses'
#     column_name = 'discourse_markers_level_5'

#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('até então'),
#                 lower.count('cerca de'),
#                 lower.count('caso '),
#                 lower.count('à tona'),
#                 lower.count('bem como'),
#                 lower.count('outrossim')
#             ]
#         )
#         if lower.count('até então') > 0:
#             #print('%d até então' % lower.count('até então'))
#             pass
#         if lower.count('cerca de') > 0:
#             #print('%d cerca de' % lower.count('cerca de'))
#             pass
#         if lower.count('caso ') > 0:
#             #print('%d caso' % lower.count('caso '))
#             pass
#         if lower.count('à tona') > 0:
#             #print('%d à tona' % lower.count('à tona'))
#             pass
#         if lower.count('bem como') > 0:
#             #print('%d bem como' % lower.count('bem como'))
#             pass
#         if lower.count('outrossim') > 0:
#             #print('%d outrossim' % lower.count('outrossim'))
#             pass
#         clauses = flat.count(' V ') - flat.count('<aux>')
#         try:
#             return ocorrencias / clauses
#         except ZeroDivisionError:
#             return 0


class DiscourseMarkersEasy(base.Metric):
    """
    ## Razão de marcadores discursivos fáceis por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos fáceis para o número de
    sentenças do texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser Palavras.

    ### Exemplo:
    *""*
    """

    name = '''Ratio of Easy Discourse Markers to All Clauses'''
    column_name = 'discourse_markers_easy'

    def value_for_text(self, t, rp=default_rp):
        lower = t.raw_content.lower()
        casos = ['e', 'se', 'que', 'ou', 'para', 'como', 'ora', 'mas', 'tão',
                 'também', 'tal', 'antes', 'por exemplo', 'quando', 'ainda', 'mal',
                 'porque', 'nem', 'tanto', 'primeiro']
        result = []
        for i in casos:
            if i in lower:
                result.append(i)
        return result


class DiscourseMarkersMedium(base.Metric):
    """
    ## Razão de marcadores discursivos medianos por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos medianos para o número de
    sentenças do texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser Palavras.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Medium Discourse Markers to All Clauses'
    column_name = 'discourse_markers_medium'

    def value_for_text(self, t, rp=default_rp):
        lower = t.raw_content.lower()
        casos = ['logo', 'caso', 'assim', 'ou seja', 'então', 'por isso',
                 'para isso', 'após', 'porém', 'enquanto', 'antes de',
                 'já que', 'quer dizer']
        result = []
        for i in casos:
            if i in lower:
                result.append(i)
        return result


class DiscourseMarkersHard(base.Metric):
    """
    ## Razão de marcadores discursivos difíceis por número de orações do
    texto.

    Calcula a proporção de marcadores discursivos difíceis para o número de
    sentenças do texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser Palavras.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Hard Discourse Markers to All Clauses'
    column_name = 'discourse_markers_hard'

    def value_for_text(self, t, rp=default_rp):
        lower = t.raw_content.lower()
        casos = ['embora', 'mas também', 'até que', 'na verdade', 'assim como',
                 'acima', 'daí', 'portanto', 'no entanto', 'não só',
                 'apesar de', 'mesmo que', 'em seguida', 'ao mesmo tempo',
                 'isto é', 'de fato', 'a seguir', 'assim que', 'mais tarde',
                 'em relação ao', 'bem como', 'depois que', 'naturalmente',
                 'ainda que', 'desde que', 'desde que', 'de modo',
                 'certamente', 'sobretudo', 'com isso', 'uma vez que',
                 'mesmo assim', 'ou melhor', 'repare-se', 'a fim de',
                 'igualmente', 'menos do que', 'entretanto', 'para começar',
                 'de forma a', 'contudo', 'com o objetivo de', 'ainda assim',
                 'por outro lado', 'dado que', 'mais ainda', 'além disso',
                 'tal como', 'para concluir', 'pelo contrário', 'logo que',
                 'é o caso de', 'em primeiro lugar', 'por último',
                 'a não ser que', 'em segundo lugar', 'por um lado',
                 'tampouco', 'em consequência', 'na realidade', 'efetivamente',
                 'de tal forma', 'como vimos', 'por esse motivo', 'a ilustrar',
                 'primeiramente']
        result = []
        for i in casos:
            if i in lower:
                result.append(i)
        return result


class DiscourseMarkersVeryHard(base.Metric):
    """
    ## Razão de marcadores discursivos muito difíceis por número de orações do
    texto.
=======
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
            # print('%d até então' % lower.count('até então'))
            pass
        if lower.count('cerca de') > 0:
            # print('%d cerca de' % lower.count('cerca de'))
            pass
        if lower.count('caso ') > 0:
            # print('%d caso' % lower.count('caso '))
            pass
        if lower.count('à tona') > 0:
            # print('%d à tona' % lower.count('à tona'))
            pass
        if lower.count('bem como') > 0:
            # print('%d bem como' % lower.count('bem como'))
            pass
        if lower.count('outrossim') > 0:
            # print('%d outrossim' % lower.count('outrossim'))
            pass
        clauses = flat.count(' V ') - flat.count('<aux>')
        try:
            return ocorrencias / clauses
        except ZeroDivisionError:
            return 0
>>>>>>> 1816e31b6440bf54090ece1e9f7b69ff7538a37d

    Calcula a proporção de marcadores discursivos muito difíceis para o número
    de sentenças do texto.

    O desempenho da métrica é diretamente relacionado ao desempenho do
    parser Palavras.

    ### Exemplo:
    *""*
    """

    name = 'Ratio of Very Hard Discourse Markers to All Clauses'
    column_name = 'discourse_markers_veryhard'

    def value_for_text(self, t, rp=default_rp):
        lower = t.raw_content.lower()
        casos = ['com efeito', 'daí que', 'em terceiro lugar', 'concluindo',
                 'paralelamente', 'ou antes', 'nesse contexto',
                 'em contrapartida', 'visto que', 'como se pode ver',
                 'seguidamente', 'em resumo', 'por ora', 'pretendemos',
                 'evidentemente', 'é evidente que', 'contanto que',
                 'além de tudo', 'com o propósito de', 'por conseguinte',
                 'prosseguindo', 'em alternativa', 'documentando',
                 'a fim de que', 'para encerrar', 'por este motivo',
                 'note-se que', 'com intuito de', 'nesse cenário', 'todavia',
                 'mais concretamente', 'contrariamente',
                 'pelo que referi anteriormente', 'em nosso entender',
                 'dizendo melhor', 'opcionalmente', 'concomitantemente',
                 'com toda a certeza', 'conquanto', 'significa isto que',
                 'quer isto dizer', 'decerto', 'recapitulando',
                 'exemplificando', 'não se pense que', 'em vias de',
                 'por outras palavras', 'estou em crer que', 'sintetizando',
                 'não obstante', 'em conclusão', 'a meu ver', 'com vistas a',
                 'alternativamente', 'deste modo', 'malgrado', 'com isto',
                 'veja-se', 'em suma']
        result = []
        for i in casos:
            if i in lower:
                result.append(i)
        return result


class ManualPrint(base.Category):
    name = 'Manual'
    table_name = 'manual'

    def __init__(self):
        super(ManualPrint, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
