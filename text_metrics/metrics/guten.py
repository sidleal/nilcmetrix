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

from nltk import ngrams
import numpy as np

from text_metrics import base
from text_metrics.resource_pool import rp as default_rp
from text_metrics.utils import ilen
from text_metrics.tools import syllable_separator, pos_tagger
from text_metrics.metrics.anaphoras import AnaphoricReferencesBase
from text_metrics.metrics.ambiguity import get_meanings_count

from itertools import filterfalse
from itertools import chain
import re


def subfinder(mylist, pattern):
    pattern = list(pattern)
    matches = []
    i = 0
    while i < len(mylist):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            i += len(pattern)
        else:
            matches.append(mylist[i])
            i += 1
    return matches


class ConcretudeMean(base.Metric):
    """
        **Nome da Métrica**: concretude_mean

        **Interpretação**: quanto maior a média de concretude, menor a complexidade textual

        **Descrição da métrica**: média dos valores de concretude das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Concretude é uma característica psicolinguística das palavras de
        conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua. Os
        valores variam de 1 a 7 e quanto maior o valor, maior a concretude.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude. Calcula-se a média desses
        valores (somam-se os valores e divide-se o resultado pela quantidade de palavras de conteúdo do texto presentes
        no repositório psicolinguístico).

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Concretude Mean'
    column_name = 'concretude_mean'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['concretude'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.mean(values))
        return np.nan_to_num(retorno)


class ConcretudeStd(base.Metric):
    """
        **Nome da Métrica**: concretude_std

        **Interpretação**: quanto maior o desvio padrão, menos confiável é a média; não tem relação direta com a
        complexidade textual

        **Descrição da métrica**: Desvio padrão do valor de concretude das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
        Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
        palavras abstratas.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude. Calcula-se o desvio-padrão
        desses valores

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Concretude Std'
    column_name = 'concretude_std'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['concretude'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.std(values))
        return np.nan_to_num(retorno)


class Concretude_1_25(base.Metric):
    """
        **Nome da Métrica**: concretude_1_25_ratio

        **Interpretação**: quanto menor a concretude, maior a complexidade textual. Portanto, quanto maior a proporção
        de palavras nessa faixa, maior a complexidade.

        **Descrição da métrica**: proporção de palavras com valor de concretude entre 1 a 2,5, em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
        Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
        palavras abstratas.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude no repositório. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de concretude entre 1 e 2,5. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras procuradas. O
        repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como semente
         listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
         imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O aumento de casos frustrou expectativas e fez as autoridades reverem estratégias.

        **Contagens**:

        8 palavras de conteúdo, com seus respectivos valores de concretude:

        frustrar 2.50
        expectativa 2.82
        rever 3.09
        aumento 3.35
        caso 3.95
        autoridade 3.50
        estratégia 3.86
        fazer 3.88

        8 palavras de conteúdo identificadas: ('aumento', 'N'), ('casos', 'N'), ('frustrou', 'V'),
        ('expectativas', 'N'), ('fez', 'V'), ('autoridades', 'N'), ('reverem', 'V'), ('estratégias', 'N')

        8 palavras lematizadas: ['aumento', 'caso', 'frustrar', 'expectativa', 'fazer', 'autoridade', 'rever',
        'estratégia']

        **Resultado Esperado**: 0,125 (1/8)

        **Resultado Obtido**: 0,125

        **Status**: correto
    """

    name = 'Concretude entre 1 e 2,5'
    column_name = 'concretude_1_25_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['concretude'] < 2.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Concretude_25_4(base.Metric):
    """
        **Nome da Métrica**: concretude_25_4_ratio

        **Interpretação**: quanto menor a concretude, maior a complexidade textual. Portanto, quanto maior a proporção
        de palavras nessa faixa e na inferior, maior a complexidade.

        **Descrição da métrica**: proporção de palavras com valores de concretude entre 2,5 e 4, em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
         imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
         Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
         palavras abstratas.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude no repositório. Contam-se,
         separadamente, as palavras de conteúdo que tenham valor de concretude entre 2,5 e 4. Depois divide-se o
         resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras procuradas. O
        repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como semente
        listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
        imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O aumento de casos frustrou expectativas e fez as autoridades reverem estratégias.

        **Contagens**:

        8 palavras de conteúdo, com seus respectivos valores de concretude:

        frustrar 2.50
        expectativa 2.82
        rever 3.09
        aumento 3.35
        caso 3.95
        autoridade 3.50
        estratégia 3.86
        fazer 3.88

        8 palavras de conteúdo identificadas: ('aumento', 'N'), ('casos', 'N'), ('frustrou', 'V'),
        ('expectativas', 'N'), ('fez', 'V'), ('autoridades', 'N'), ('reverem', 'V'), ('estratégias', 'N')

        8 palavras lematizadas: ['aumento', 'caso', 'frustrar', 'expectativa', 'fazer', 'autoridade', 'rever',
         'estratégia']

        7 palavras no intervalo entre 2,5 e 4,00 de concretude

        **Resultado Esperado**: 0,875 (9/8)

        **Resultado Obtido**: 0,875 (9/8)

        **Status**: correto
    """

    name = 'Concretude entre 2,5 e 4'
    column_name = 'concretude_25_4_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['concretude'] >= 2.5 and rp.psicolinguistico()[word]['concretude'] < 4:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Concretude_menos_4(base.Metric):
#     """
#         **Nome da Métrica**: concretude_menor_4_ratio
#
#         **Interpretação**: quanto menor a concretude, maior a complexidade textual
#
#         **Descrição da métrica**: proporção de palavras com valor de concretude menor que 4, em relação a todas as
#         palavras de conteúdo do texto presentes no repositório psicolinguístico
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
#         para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
#         imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
#         Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
#         palavras abstratas.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, contam-se as
#         palavras de conteúdo que estão no repositório psicolinguístico e procuram-se seus respectivos valores de
#         concretude. Contam-se, separadamente, as palavras de conteúdo que tenham valor de concretude menor que 4.
#         Depois divide-se o resultado pela quantidade total de palavras de conteúdo presentes no repositório
#         psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
#         métrica: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras procuradas. O
#         repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como semente
#         listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
#         imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#
#     """
#
#     name = 'Concretude menor que 4'
#     column_name = 'concretude_menor_4_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['concretude'] < 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class Concretude_4_55(base.Metric):
    """
        **Nome da Métrica**: concretude_4_55_ratio

        **Interpretação**: quanto menor a concretude, maior a complexidade textual. Portanto, quanto maior a proporção
        de palavras nessa faixa e na superior, menor a complexidade.

        **Descrição da métrica**: proporção de palavras com valor de concretude de médio para entre 4 e 5,5, em relação
        a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
        Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
        palavras abstratas.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude no repositório. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de concretude entre 4 e 5,5. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras procuradas. O
        repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como semente
        listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
        imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O aumento de casos frustrou expectativas e fez as autoridades reverem estratégias.

        **Contagens**:

        8 palavras de conteúdo, com seus respectivos valores de concretude:

        frustrar 2.50
        expectativa 2.82
        rever 3.09
        aumento 3.35
        caso 3.95
        autoridade 3.50
        estratégia 3.86
        fazer 3.88

        8 palavras de conteúdo identificadas: ('aumento', 'N'), ('casos', 'N'), ('frustrou', 'V'),
        ('expectativas', 'N'), ('fez', 'V'), ('autoridades', 'N'), ('reverem', 'V'), ('estratégias', 'N')

        8 palavras lematizadas: ['aumento', 'caso', 'frustrar', 'expectativa', 'fazer', 'autoridade', 'rever',
        'estratégia']

        Nenhuma palavra no intervalo de 4,00 a 5,50 de concretude

        **Resultado Esperado**: 0,0

        **Resultado Obtido**: 0,0

        **Status**: correto
    """

    name = 'Concretude entre 4 e 5,5'
    column_name = 'concretude_4_55_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['concretude'] >= 4 and rp.psicolinguistico()[word]['concretude'] < 5.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Concretude_55_7(base.Metric):
    """
        **Nome da Métrica**: concretude_55_7_ratio

        **Interpretação**: quanto menor a concretude, maior a complexidade textual. Portanto, quanto maior a proporção
        de palavras nessa faixa, menor a complexidade.

        **Descrição da métrica**: proporção de palavras com valor de concretude entre 5,5 e 7, em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
        Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
        palavras abstratas.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude no repositório. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de concretude entre 5,5 e 7. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras procuradas. O
        repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como semente
        listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
        imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O aumento de casos frustrou expectativas e fez as autoridades reverem estratégias.

        **Contagens**:

        8 palavras de conteúdo, com seus respectivos valores de concretude:

        frustrar 2.50
        expectativa 2.82
        rever 3.09
        aumento 3.35
        caso 3.95
        autoridade 3.50
        estratégia 3.86
        fazer 3.88

        8 palavras de conteúdo identificadas: ('aumento', 'N'), ('casos', 'N'), ('frustrou', 'V'),
        ('expectativas', 'N'), ('fez', 'V'), ('autoridades', 'N'), ('reverem', 'V'), ('estratégias', 'N')

        8 palavras lematizadas: ['aumento', 'caso', 'frustrar', 'expectativa', 'fazer', 'autoridade', 'rever',
        'estratégia']

        Nenhuma palavra no intervalo de 5,50 a 7,00 de concretude

        **Resultado Esperado**: 0,0

        **Resultado Obtido**: 0,0

        **Status**: correto

    """

    name = 'Concretude entre 5,5 e 7'
    column_name = 'concretude_55_7_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['concretude'] >= 5.5 and rp.psicolinguistico()[word]['concretude'] < 7:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Concretude_4_mais(base.Metric):
#     """
#         **Nome da Métrica**: concretude_4_maior_ratio
#
#         **Interpretação**: quanto menor a concretude, maior a complexidade textual
#
#         **Descrição da métrica**: proporção de palavras com valores de concretude maior ou igual a 4, em relação a todas
#         as palavras de conteúdo do texto presentes no repositório psicolinguístico
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
#         para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
#         imageabilidade. Os valores de concretude variam de 1 a 7 e quanto maior o valor, mais alta a concretude.
#         Palavras com alto valor de concretude são palavras concretas e palavras com baixo valor de concretude são
#         palavras abstratas.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
#         palavras, usando o DELAF, e procuram-se seus respectivos valores de concretude. Contam-se, separadamente, as
#         palavras de conteúdo que tenham valor de concretude maior que 4. Depois divide-se o resultado pela quantidade
#         total de palavras de conteúdo presentes no repositório psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Concretude maior ou igual que 4'
#     column_name = 'concretude_4_maior_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['concretude'] >= 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class ImageabilidadeMean(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_mean

        **Interpretação**: quanto maior a média de imageabilidade, menor a complexidade textual

        **Descrição da métrica**: média dos valores de imageabilidade das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das palavras
        de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Calcula-se a média desses
        valores (somam-se os valores e divide-se o resultado pela quantidade de palavras de conteúdo do texto presentes
        no repositório psicolinguístico).

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Imageabilidade Mean'
    column_name = 'imageabilidade_mean'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['imageabilidade'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.mean(values))
        return np.nan_to_num(retorno)


class ImageabilidadeStd(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_std

        **Interpretação**: quanto maior o desvio padrão, menos confiável é a média; não tem relação direta com a
        complexidade textual

        **Descrição da métrica**: Desvio padrão dos valores de imageabilidade das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das palavras
        de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Calcula-se o desvio-padrão
        desses valores

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN

    """

    name = 'Imageabilidade Std'
    column_name = 'imageabilidade_std'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['imageabilidade'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.std(values))
        return np.nan_to_num(retorno)


class Imageabilidade_1_25(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_1_25_ratio

        **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual. Portanto, quanto maior
        a proporção de palavras nessa faixa, maior a complexidade.

        **Descrição da métrica**: Proporção de palavras de conteúdo do texto com imageabilidade entre 1 e 2,5, em
        relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das palavras
        de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se,
        separadamente, as palavras de conteúdo do texto que tenham valor de imageabilidade entre 1 e 2,5.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente
        (e por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de
        concretude, familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por
        psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Pescadores tentarão retirar o maior número de peixes da espécie, que pode atingir 20 centímetros de
        comprimento e um quilo.

        **Contagens**:

        12 palavras  de conteúdo, com seus respectivos valores de imageabilidade:

        maior 3.48
        número 4.15
        tentar 4.18
        atingir 4.21
        retirar 4.24
        comprimento 4.64
        centímetro 4.77
        espécie 4.87
        podar 4.89
        quilo 5.32
        pescador 5.55
        peixe 6.00

        12 palavras reconhecidas (com suas respectivas etiquetas morfossintáticas): 'Pescadores', 'NPROP'; 'tentarão',
        'V'; 'retirar', 'V'; 'maior', 'ADJ'; 'número', 'N'; 'peixes', 'N'; 'espécie', 'N'; 'pode', 'V'; 'atingir', 'V';
        'centímetros', 'N'; 'comprimento', 'N'; 'quilo', 'N'.

        11 palavras lematizadas: ['tentar', 'retirar', 'maior', 'número', 'peixe', 'espécie', 'podar', 'atingir',
        'centímetro', 'comprimento', 'quilo'].

        A palavra “Pescador” foi anotada como NPROP e por isso não foi lematizada.

        11 palavras encontradas no repositório psicolinguístico (todas, menos “Pescadores”)

        nenhuma palavra com imageabilidade entre 1 e 2,5

        **Resultado Esperado**: 0

        **Resultado Obtido**: 0

        **Status**: correto

    """

    name = 'Imageabilidade entre 1 e 2,5'
    column_name = 'imageabilidade_1_25_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['imageabilidade'] < 2.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Imageabilidade_25_4(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_25_4_ratio

        **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual. Portanto, quanto maior
        o percentual de palavras nessa faixa e na inferior, maior a complexidade.

        **Descrição da métrica**: Proporção de palavras de conteúdo do texto com imageabilidade entre 2,5 e 4, em
        relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das palavras
        de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se, separadamente,
        as palavras de conteúdo que tenham valor de imageabilidade entre 2,5 e 4. Depois divide-se o resultado pela
        quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente
        (e por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de
        concretude, familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por
        psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Pescadores tentarão retirar o maior número de peixes da espécie, que pode atingir 20 centímetros de
        comprimento e um quilo.

        **Contagens**:

        12 palavras  de conteúdo, com seus respectivos valores de imageabilidade:

        maior 3.48
        número 4.15
        tentar 4.18
        atingir 4.21
        retirar 4.24
        comprimento 4.64
        centímetro 4.77
        espécie 4.87
        podar 4.89
        quilo 5.32
        pescador 5.55
        peixe 6.00

        12 palavras reconhecidas (com suas respectivas etiquetas morfossintáticas): 'Pescadores', 'NPROP'; 'tentarão',
        'V'; 'retirar', 'V'; 'maior', 'ADJ'; 'número', 'N'; 'peixes', 'N'; 'espécie', 'N'; 'pode', 'V'; 'atingir', 'V';
        'centímetros', 'N'; 'comprimento', 'N'; 'quilo', 'N'.

        11 palavras lematizadas: ['tentar', 'retirar', 'maior', 'número', 'peixe', 'espécie', 'podar', 'atingir',
        'centímetro', 'comprimento', 'quilo'].

        A palavra “Pescador” foi anotada como NPROP e não foi lematizada)

        11 palavras encontradas no repositório psicolinguístico

        1 palavra com imageabilidade entre 2,5 e 4.0 (maior)

        **Resultado Esperado**: 0,083 (1/12)

        **Resultado Obtido**: 0, 091 (1/11)

        **Status**: correto, considerando as limitações do tagger
    """

    name = 'Imageabilidade entre 2,5 e 4'
    column_name = 'imageabilidade_25_4_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['imageabilidade'] >= 2.5 and rp.psicolinguistico()[word]['imageabilidade'] < 4:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Imageabilidade_menos_4(base.Metric):
#     """
#         **Nome da Métrica**: imageabilidade_menor_4_ratio
#
#         **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual.
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com imageabilidade menor que 4, em relação
#         a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das
#         palavras de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes
#         da língua. Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
#         palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se, separadamente, as
#         palavras de conteúdo que tenham valor de imageabilidade menor que 4. Depois divide-se o resultado pela
#         quantidade total de palavras de conteúdo presentes no repositório psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#
#     """
#
#     name = 'Imageabilidade menor que 4'
#     column_name = 'imageabilidade_menor_4_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['imageabilidade'] < 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class Imageabilidade_4_55(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_4_55_ratio

        **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual. Portanto, quanto maior
        a proporção de palavras nessa faixa e na superior, menor a complexidade textual.

        **Descrição da métrica**: proporção de palavras com valor de imageabilidade entre 4 e 5,5, em relação a todas
        as palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Imageabilidade é uma característica psicolinguística das palavras de conteúdo e significa o
        quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua. Os valores variam de
        1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de imageabilidade entre 4 e 5,5. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. Ele foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados, junto a usuários da língua por psicolinguistas e psicólogos.

        **Projeto**: GUTEN

        **Teste**: Pescadores tentarão retirar o maior número de peixes da espécie, que pode atingir 20 centímetros de
        comprimento e um quilo.

        **Contagens**:

        12 palavras  de conteúdo, com seus respectivos valores de imageabilidade:

        maior 3.48
        número 4.15
        tentar 4.18
        atingir 4.21
        retirar 4.24
        comprimento 4.64
        centímetro 4.77
        espécie 4.87
        podar 4.89
        quilo 5.32
        pescador 5.55
        peixe 6.00

        12 palavras reconhecidas (com suas respectivas etiquetas morfossintáticas): 'Pescadores', 'NPROP'; 'tentarão',
        'V'; 'retirar', 'V'; 'maior', 'ADJ'; 'número', 'N'; 'peixes', 'N'; 'espécie', 'N'; 'pode', 'V'; 'atingir', 'V';
        'centímetros', 'N'; 'comprimento', 'N'; 'quilo', 'N'.

        11 palavras lematizadas: ['tentar', 'retirar', 'maior', 'número', 'peixe', 'espécie', 'podar', 'atingir',
        'centímetro', 'comprimento', 'quilo']. A palavra “Pescador” foi anotada como NPROP e não foi lematizada)

        11 palavras encontradas no repositório psicolinguístico

        **Resultado Esperado**: 0,818 (9/12)

        **Resultado Obtido**: 0,9 (9/11)

        **Status**: correto, considerando a limitação do tagger
    """

    name = 'Imageabilidade entre 4 e 5,5'
    column_name = 'imageabilidade_4_55_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['imageabilidade'] >= 4 and rp.psicolinguistico()[word]['imageabilidade'] < 5.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Imageabilidade_55_7(base.Metric):
    """
        **Nome da Métrica**: imageabilidade_55_7_ratio

        **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual. Portanto, quanto maior
         a proporção de palavras nessa faixa, menor a complexidade.

        **Descrição da métrica**: proporção de palavras com alto valor de imageabilidade (5,5 a 7) em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Imageabilidade é uma característica psicolinguística das palavras de conteúdo e significa o
        quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua. Os valores variam de
        1 a 7 e quanto maior o valor, maior a imageabilidade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de imageabilidade entre 5,5 e 7. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. Ele foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Pescadores tentarão retirar o maior número de peixes da espécie, que pode atingir 20 centímetros de
        comprimento e um quilo.

        **Contagens**:

        12 palavras  de conteúdo, com seus respectivos valores de imageabilidade:

        maior 3.48
        número 4.15
        tentar 4.18
        atingir 4.21
        retirar 4.24
        comprimento 4.64
        centímetro 4.77
        espécie 4.87
        podar 4.89
        quilo 5.32
        pescador 5.55
        peixe 6.00

        12 palavras reconhecidas (com suas respectivas etiquetas morfossintáticas): 'Pescadores', 'NPROP'; 'tentarão',
        'V'; 'retirar', 'V'; 'maior', 'ADJ'; 'número', 'N'; 'peixes', 'N'; 'espécie', 'N'; 'pode', 'V'; 'atingir', 'V';
         'centímetros', 'N'; 'comprimento', 'N'; 'quilo', 'N'.

        11 palavras lematizadas: ['tentar', 'retirar', 'maior', 'número', 'peixe', 'espécie', 'podar', 'atingir',
        'centímetro', 'comprimento', 'quilo']. A palavra “Pescador” foi anotada como NPROP e não foi lematizada)

        11 palavras encontradas no repositório psicolinguístico, 2 entre 5,5 e 7,00

        **Resultado Esperado**: 0,167, (2/12)

        **Resultado Obtido**: 0,091, (1/11)

        **Status**: correto, considerando a limitação do tagger
    """

    name = 'Imageabilidade entre 5,5 e 7'
    column_name = 'imageabilidade_55_7_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['imageabilidade'] >= 5.5 and rp.psicolinguistico()[word]['imageabilidade'] < 7:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Imageabilidade_4_mais(base.Metric):
#     """
#         **Nome da Métrica**: imageabilidade_4_maior_ratio
#
#         **Interpretação**: quanto maior o valor de imageabilidade, menor a complexidade textual.
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com imageabilidade maior ou igual a 4, em
#         relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Imageabilidade é uma característica psicolinguística das palavras
#         de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
#         Os valores variam de 1 a 7 e quanto maior o valor, maior a imageabilidade.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
#         palavras, usando o DELAF, e procuram-se seus respectivos valores de imageabilidade. Contam-se, separadamente, as
#         palavras de conteúdo que tenham valor de imageabilidade maior que 4. Depois divide-se o resultado pela
#         quantidade total de palavras de conteúdo presentes no repositório psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#          evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#
#     """
#
#     name = 'Imageabilidade maior ou igual que 4'
#     column_name = 'imageabilidade_4_maior_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['imageabilidade'] >= 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class FamiliaridadeMean(base.Metric):
    """
        **Nome da Métrica**: familiaridade_mean

        **Interpretação**: quanto menor for a média, maior a familiaridade e menor a complexidade textual

        **Descrição da métrica**: média dos valores de familiaridade das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras
        de conteúdo e representa o quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas.
        Os valores variam de 1 a 7 e quanto menor o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Calcula-se a média desses
        valores (somam-se os valores e divide-se o resultado pela quantidade de palavras de conteúdo do texto presentes
        no repositório psicolinguístico).

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Familiaridade Mean'
    column_name = 'familiaridade_mean'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['familiaridade'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.mean(values))
        return np.nan_to_num(retorno)


class FamiliaridadeStd(base.Metric):
    """
        **Nome da Métrica**: familiaridade_std

        **Interpretação**: quanto maior o desvio padrão, menos confiável é a média. Não tem relação direta com a
        complexidade textual

        **Descrição da métrica**: Desvio padrão dos valores de familiaridade das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras de
        conteúdo e representa o quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas. Os
        valores variam de 1 a 7 e quanto menor o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Calcula-se o desvio-padrão
        desses valores

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Familiaridade Std'
    column_name = 'familiaridade_std'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['familiaridade'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.std(values))
        return np.nan_to_num(retorno)


class Familiaridade_1_25(base.Metric):
    """
        **Nome da Métrica**: familiaridade_1_25_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa, maior a complexidade textual

        **Descrição da métrica**: Proporção de palavras de conteúdo com valores de familiaridade entre 1 a 2,5, em
        relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras
        de conteúdo e representa o quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se, separadamente, as
        palavras de conteúdo que tenham valor de familiaridade entre 1 e 2,5. Depois divide-se o resultado pela
        quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. repositório psicolinguístico tem 26.874 palavras e
        pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e
        por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de concretude,
        familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por psicolinguistas e
         psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Desde que a canonização foi confirmada pelo Vaticano, o movimento no Mosteiro da Luz tem aumentado
        -- e o interesse da imprensa também.

        **Contagens**:

        12 palavras de conteúdo, com os seguintes valores de familiaridade:

        Canonização 2,48; Mosteiro 3,04; Vaticano 3,45; Confirmada 4,38; Movimento 4,84; Luz 5,57; Aumentar 4,89;
        Imprensa 4,90; Interesse 5,31; Também 5,44; Ser 5,50; Ter 5,81

        9 palavras de conteúdo reconhecidas e lematizadas pelo programa: ['canonização', 'ir', 'confirmado',
        'movimento', 'ter', 'aumentado', 'interesse', 'imprensa', 'também'] O programa não reconheceu os Nomes Próprios
        (Vaticano, Mosteiro, Luz) como palavras de conteúdo. O verbo “foi” (que é uma forma ambígua) foi lematizado
        incorretamente para “ir” e não para “ser”.

        7 palavras encontradas no repositório psicolinguístico (os particípios “confirmado” e “aumentado” foram
        lematizado como adjetivos e por isso não foram encontrados no repositório; eles só seriam encontrados se fossem
        lematizados como verbos: confirmar” e “aumentar”).

        1 palavra com familiaridade de 1 a 2,5 (canonização)

        **Resultado Esperado**: 0,083 (1/12)

        **Resultado Obtido**: 0,143 (1/7)

        **Status**: correto, considerando as limitações do tagger e da estratégia de lematização
    """

    name = 'Familiaridade entre 1 e 2,5'
    column_name = 'familiaridade_1_25_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['familiaridade'] < 2.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Familiaridade_25_4(base.Metric):
    """
        **Nome da Métrica**: familiaridade_25_4_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa e na inferior, maior a complexidade textual

        **Descrição da métrica**: Proporção de palavras de conteúdo com familiaridade entre 2,5 e 4, em relação a todas
        as palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras
        de conteúdo e significa o quanto a palavra pode ser traduzida por uma imagem na opinião dos falantes da língua.
        Os valores variam de 1 a 7 e quanto maior o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se, separadamente,
        as palavras de conteúdo que tenham valor de familiaridade entre 2,5 e 4. Depois divide-se o resultado pela
        quantidade total de palavras de conteúdodo texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente
        (e por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de
        concretude, familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por
        psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Desde que a canonização foi confirmada pelo Vaticano, o movimento no Mosteiro da Luz tem aumentado
        -- e o interesse da imprensa também.

        **Contagens**:

        12 palavras de conteúdo, com os seguintes valores de familiaridade:

        Canonização 2,48; Mosteiro 3,04; Vaticano 3,45; Confirmada 4,38; Movimento 4,84; Luz  5,57; Aumentar 4,89;
        Imprensa 4,90; Interesse 5,31; Também 5,44; Ser 5,50; Ter 5,81

        9 palavras de conteúdo reconhecidas e lematizadas pelo programa: ['canonização', 'ir', 'confirmado',
        'movimento', 'ter', 'aumentado', 'interesse', 'imprensa', 'também'] O programa não reconheceu os Nomes
        Próprios (Vaticano, Mosteiro, Luz) como palavras de conteúdo. O verbo “foi” (que é uma forma ambígua) foi
        lematizado incorretamente para “ir” e não para “ser”.

        7 palavras encontradas no repositório psicolinguístico (os particípios “confirmado” e “aumentado” foram
        lematizado como adjetivos e por isso não foram encontrados no repositório; eles só seriam encontrados se
        fossem lematizados como verbos: confirmar” e “aumentar”).

        2 palavras com familiaridade de 2,5 a 4,0: 2 (mosteiro, vaticano)

        **Resultado Esperado**: 0,167 (2/12)

        **Resultado Obtido**: 0,0

        **Status**: correto, considerando as limitações do tagger e da estratégia de lematização
    """

    name = 'Familiaridade entre 2,5 e 4'
    column_name = 'familiaridade_25_4_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['familiaridade'] >= 2.5 and rp.psicolinguistico()[word]['familiaridade'] < 4:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Familiaridade_menos_4(base.Metric):
#     """
#         **Nome da Métrica**: familiaridade_menor_4_ratio
#
#         **Interpretação**: quanto menor for o valor de familiaridade, maior é a familiaridade e menor a complexidade
#         textual
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com valor de familiaridade menor que 4, em
#         relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras
#         de conteúdo e representa o quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas.
#         Os valores variam de 1 a 7 e quanto menor o valor, maior a familiaridade.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
#         palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se, separadamente, as
#         palavras de conteúdo que tenham valor de familiaridade menor que 4. Depois divide-se o resultado pela quantidade
#         total de palavras de conteúdo presentes no repositório psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Familiaridade menor que 4'
#     column_name = 'familiaridade_menor_4_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['familiaridade'] < 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class Familiaridade_4_55(base.Metric):
    """
        **Nome da Métrica**: familiaridade_4_55_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa e na superior, menor a complexidade textual.

        **Descrição da métrica**: proporção de palavras com valor de familiaridade entre 4 a 5,5, em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Familiaridade é uma característica psicolinguística das palavras de conteúdo e representa o
        quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas. Os valores variam de 1 a 7
        e quanto maior o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de familiaridade entre 4 e 5,5. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras e pode não conter
        todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito
        a vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Desde que a canonização foi confirmada pelo Vaticano, o movimento no Mosteiro da Luz tem aumentado
        -- e o interesse da imprensa também.

        **Contagens**:

        12 palavras de conteúdo, com os seguintes valores de familiaridade:

        Canonização 2,48; Mosteiro 3,04; Vaticano 3,45; Confirmada 4,38; Movimento 4,84; Luz 5,57; Aumentar 4,89;
        Imprensa 4,90; Interesse 5,31; Também 5,44; Ser 5,50; Ter 5,81

        9 palavras de conteúdo reconhecidas e lematizadas pelo programa: ['canonização', 'ir', 'confirmado',
        'movimento', 'ter', 'aumentado', 'interesse', 'imprensa', 'também']

        O programa não reconheceu os Nomes Próprios (Vaticano, Mosteiro, Luz) como palavras de conteúdo.
        O verbo “foi” (que é uma forma ambígua) foi lematizado incorretamente para “ir” e não para “ser”.

        7 palavras encontradas no repositório psicolinguístico (os particípios “confirmado” e “aumentado”
         foram lematizado como adjetivos e por isso não foram encontrados no repositório; eles só seriam encontrados
         se fossem lematizados como verbos: confirmar” e “aumentar”).

        6 palavras com familiaridade de 4,0 a 5,5 (confirmar, movimento, aumentar, interesse, imprensa, também)

        **Resultado esperado**: 0,50 (6/12)

        **Resultado obtido**: 0,5710 (4/7)

        **Status**: correto, considerando as limitações do tagger e da estratégia de lematização
    """

    name = 'Familiaridade entre 4 e 5,5'
    column_name = 'familiaridade_4_55_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['familiaridade'] >= 4 and rp.psicolinguistico()[word]['familiaridade'] < 5.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class Familiaridade_55_7(base.Metric):
    """
        **Nome da Métrica**: familiaridade_55_7_ratio

        **Interpretação**: quanto maior for o resultado, maior é a familiaridade e menor a complexidade textual

        **Descrição da métrica**: proporção de palavras com valor de familiaridade entre 5,5 e 7, em relação a todas as
        palavras de conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. O repositório psicolinguístico é um recurso lexical com valores
        para 4 características psicolinguísticas das palavras: concretude, familiaridade, idade de aquisição e
        imageabilidade. Familiaridade é uma característica psicolinguística das palavras de conteúdo e representa o
        quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas. Os valores variam de 1 a 7
        e quanto maior o valor, maior a familiaridade.

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se
        essas palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de familiaridade entre 5,5 e 7. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras e pode não conter
        todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso,
        sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de concretude,
        familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por psicolinguistas
        e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Desde que a canonização foi confirmada pelo Vaticano, o movimento no Mosteiro da Luz tem aumentado
        -- e o interesse da imprensa também.

        **Contagens**:

        12 palavras de conteúdo, com os seguintes valores de familiaridade:

        Canonização 2,48; Mosteiro 3,04; Vaticano 3,45; Confirmada 4,38; Movimento 4,84; Luz  5,57; Aumentar 4,89;
        Imprensa 4,90; Interesse 5,31; Também 5,44; Ser 5,50; Ter 5,81

        9 palavras de conteúdo reconhecidas e lematizadas pelo programa: ['canonização', 'ir', 'confirmado',
        'movimento', 'ter', 'aumentado', 'interesse', 'imprensa', 'também'] O programa não reconheceu os Nomes
        Próprios (Vaticano, Mosteiro, Luz) como palavras de conteúdo. O verbo “foi” (que é uma forma ambígua)
        foi lematizado incorretamente para “ir” e não para “ser”.

        7 palavras encontradas no repositório psicolinguístico (os particípios “confirmado” e “aumentado”
        foram lematizado como adjetivos e por isso não foram encontrados no repositório; eles só seriam encontrados
        se fossem lematizados como verbos: confirmar” e “aumentar”).

        3 palavras com familiaridade de 5,5 a 7,00 (ser, luz, ter)

        **Resultado esperado**: 0,25 (3/12)

        **Resultado Obtido**: 0,286 (2/7)

        **Status**: correto, considerando as limitações do tagger e da estratégia de lematização

    """

    name = 'Familiaridade entre 5,5 e 7'
    column_name = 'familiaridade_55_7_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['familiaridade'] >= 5.5 and rp.psicolinguistico()[word]['familiaridade'] < 7:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class Familiaridade_4_mais(base.Metric):
#     """
#         **Nome da Métrica**: familiaridade_4_maior_ratio
#
#         **Interpretação**: quanto menor for o valor de familiaridade, maior é a familiaridade e menor a complexidade
#         textual
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com valor de familiaridade maior ou igual
#         a 4, em relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Familiaridade é uma característica psicolinguística das palavras
#         de conteúdo e representa o quanto os falantes da língua conhecem e usam uma palavra em suas vidas cotidianas.
#         Os valores variam de 1 a 7 e quanto menor o valor, maior a familiaridade.
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
#         palavras, usando o DELAF, e procuram-se seus respectivos valores de familiaridade. Contam-se, separadamente, as
#         palavras de conteúdo que tenham valor de familiaridade maior que 4. Depois divide-se o resultado pela quantidade
#         total de palavras de conteúdo presentes no repositório psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Familiaridade maior ou igual que 4'
#     column_name = 'familiaridade_4_maior_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['familiaridade'] >= 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class IdadeAquisicaoMean(base.Metric):
    """
        **Nome da Métrica**: idade_aquisicao_mean

        **Interpretação**: quanto menor a média, menor a idade de aquisição e menor a complexidade textual

        **Descrição da métrica**: média dos valores de idade de aquisição das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
        palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de 1 a
        7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de 0 a
        2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
        7 (13 anos ou mais).

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, contam-se as
        palavras de conteúdo que estão no repositório psicolinguístico e procuram-se seus respectivos valores de idade
        de aquisição. Calcula-se a média desses valores (somam-se os valores e divide-se o resultado pela quantidade de
        palavras de conteúdo do texto presentes no repositório psicolinguístico).

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: GUTEN
    """

    name = 'Idade Aquisicao Mean'
    column_name = 'idade_aquisicao_mean'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['idade_aquisicao'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.mean(values))
        return np.nan_to_num(retorno)


class IdadeAquisicaoStd(base.Metric):
    """
        **Nome da Métrica**: idade_aquisicao_std

        **Interpretação**: quanto maior o desvio padrão, menos confiável é a média. Não tem relação direta com a
        complexidade textual

        **Descrição da métrica**: Desvio padrão dos valores de idade de aquisição das palavras de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
        palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
        1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
        0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
        7 (13 anos ou mais).

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, contam-se as
        palavras de conteúdo que estão no repositório psicolinguístico e procuram-se seus respectivos valores de idade
        de aquisição. Calcula-se o desvio-padrão desses valores.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
        palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
        vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
        evitar redundância. Por esse motivo esta métrica foi comentada.

        **Projeto**: Guten
    """

    name = 'Idade Aquisicao Std'
    column_name = 'idade_aquisicao_std'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        values = []
        for word in words:
            if word in rp.psicolinguistico():
                values.append(rp.psicolinguistico()[word]['idade_aquisicao'])
        retorno = 0.0
        if len(values) > 0:
            retorno = float(np.std(values))
        return np.nan_to_num(retorno)


class IdadeAquisicao_1_25(base.Metric):
    """
        **Nome da Métrica**: idade_aquisicao_1_25_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa, menor a complexidade textual

        **Descrição da métrica**: Proporção de palavras de conteúdo do texto com idade de aquisição entre 1 e 2,5 em
        relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
        palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
        1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
        0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
        7 (13 anos ou mais).

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de idade de aquisição. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de idade de aquisição entre 1 e 2,5. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente
        (e por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de
        concretude, familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por
        psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Segundo o chefe substituto do escritório regional, Guaracy Cunha, ainda há tempo para o pedido de
        licença.

        **Contagens**:

        9 palavras de conteúdo e respectivas idades de aquisição (os 2 nomes próprios são palavras de conteúdo, mas não
        têm idade de aquisição, por serem nomes de pessoas):

        tempo (2,39),
        ainda (3,89),
        chefe (4,12),
        licença (4,57).
        há (5,10),
        pedido (5,26),
        escritório (5,35),
        substituto (6,00),
        regional (6,24),

        9 palavras de conteúdo identificadas e lematizadas: 'chefe', 'substituto', 'escritório', 'regional', 'ainda',
        'haver', 'tempo', 'pedido', 'licença'

        **Resultado Esperado**: 0,111 (1/9)

        **Resultado Obtido**: 0,111

        **Status**: correto
    """

    name = 'Idade Aquisicao entre 1 e 2,5'
    column_name = 'idade_aquisicao_1_25_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['idade_aquisicao'] < 2.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class IdadeAquisicao_25_4(base.Metric):
    """
        **Nome da Métrica**: idade_aquisicao_25_4_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa e na inferior, menor a complexidade textual

        **Descrição da métrica**: Proporção de palavras de conteúdo do texto com valores de idade de aquisição entre
        2,5 e 4, em relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
        palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
        1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
        0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
        7 (13 anos ou mais).

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de idade de aquisição. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de idade de aquisição entre 2,5 e 4. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico

        **Limitações da métrica**: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras
        e pode não conter todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente
        (e por isso, sujeito a vieses), usando como semente listas de palavras com seus respectivos valores de
        concretude, familiaridade, idade de aquisição e imageabilidade, levantados junto a usuários da língua por
        psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Segundo o chefe substituto do escritório regional, Guaracy Cunha, ainda há tempo para o pedido de
        licença.

        **Contagens**:

        9 palavras de conteúdo e respectivas idades de aquisição (os 2 nomes próprios são palavras de conteúdo, mas não
        têm idade de aquisição, por serem nomes de pessoas):

        tempo (2,39),
        ainda (3,89),
        chefe (4,12),
        licença (4,57).
        há (5,10),
        pedido (5,26),
        escritório (5,35),
        substituto (6,00),
        regional (6,24),

        9 palavras de conteúdo identificadas e lematizadas: 'chefe', 'substituto', 'escritório', 'regional', 'ainda',
        'haver', 'tempo', 'pedido', 'licença'

        1 palavra no intervalo entre 2,5 e 4,0 (ainda)

        **Resultado Esperado**: 0,111 (1/9)

        **Resultado Obtido**: 0,111

        **Status**: correto
    """

    name = 'Idade Aquisicao entre 2,5 e 4'
    column_name = 'idade_aquisicao_25_4_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['idade_aquisicao'] >= 2.5 and rp.psicolinguistico()[word]['idade_aquisicao'] < 4:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class IdadeAquisicao_menos_4(base.Metric):
#     """
#         **Nome da Métrica**: idade_aquisicao_menor_4_ratio
#
#         **Interpretação**: quanto menor o valor de idade de aquisição, menor a idade de aquisição e menor a complexidade
#         textual
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com valor de idade de aquisição menor que
#         4, em relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico.
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
#         palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
#         1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
#         0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
#         7 (13 anos ou mais).
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, contam-se as
#         palavras de conteúdo que estão no repositório psicolinguístico e procuram-se seus respectivos valores de idade
#         de aquisição. Contam-se, separadamente, as palavras de conteúdo que tenham valor de idade de aquisição menor
#         que 4. Depois divide-se o resultado pela quantidade total de palavras de conteúdo presentes no repositório
#         psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Idade de aquisição menor que 4'
#     column_name = 'idade_aquisicao_menor_4_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['idade_aquisicao'] < 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class IdadeAquisicao_4_55(base.Metric):
    """
**Nome da Métrica**: idade_aquisicao_4_55_ratio

**Interpretação**: quanto maior a proporção de palavras nessa faixa e na superior, maior a complexidade textual.

**Descrição da métrica**: proporção de palavras com valor de idade de aquisição entre 4 e 5,5, em relação a todas as
palavras de conteúdo do texto presentes no repositório psicolinguístico

**Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo: substantivos,
verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das palavras de conteúdo e
representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de 1 a 7 e quanto menor o valor,
menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de 0 a 2 anos); 2 (de 3 a 4 anos), 3 (de
5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos), 7 (13 anos ou mais).

**Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
palavras, usando o DELAF, e procuram-se seus respectivos valores de idade de aquisição. Contam-se, separadamente, as
palavras de conteúdo que tenham valor de idade de aquisição entre 4 e 5,5. Depois divide-se o resultado pela quantidade
total de palavras de conteúdo presentes no repositório psicolinguístico.

**Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da métrica:
depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras e pode não conter todas as palavras
procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a vieses), usando como
semente listas de palavras com seus respectivos valores de concretude, familiaridade, idade de aquisição e
imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

**Crítica**:

**Projeto**: GUTEN

**Teste**: Segundo o chefe substituto do escritório regional, Guaracy Cunha, ainda há tempo para o pedido de licença.

**Contagens**:

9 palavras de conteúdo e respectivas idades de aquisição (os 2 nomes próprios são palavras de conteúdo, mas não têm
idade de aquisição, por serem nomes de pessoas):

tempo (2,39),
ainda (3,89),
chefe (4,12),
licença (4,57).
há (5,10),
pedido (5,26),
escritório (5,35),
substituto (6,00),
regional (6,24),

9 palavras de conteúdo identificadas e lematizadas: 'chefe', 'substituto', 'escritório', 'regional', 'ainda', 'haver',
'tempo', 'pedido', 'licença'

5 palavras no intervalo de 4,00 a 5,50

**Resultado Esperado**: 0,556 (5/9)

**Resultado Obtido**: 0,556

**Status**: correto
    """

    name = 'Idade Aquisicao entre 4 e 5,5'
    column_name = 'idade_aquisicao_4_55_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['idade_aquisicao'] >= 4 and rp.psicolinguistico()[word]['idade_aquisicao'] < 5.5:
                    count += 1
        try:
            return count / total
        except:
            return 0


class IdadeAquisicao_55_7(base.Metric):
    """
        **Nome da Métrica**: idade_aquisicao_55_7_ratio

        **Interpretação**: quanto maior a proporção de palavras nessa faixa, maior a complexidade textual Descrição da
        métrica: proporção de palavras com valor de idade de aquisição entre 5,5 e 7, em relação a todas as palavras de
        conteúdo do texto presentes no repositório psicolinguístico

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
         palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
         1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
         0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
         7 (13 anos ou mais).

        **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, lematizam-se essas
        palavras, usando o DELAF, e procuram-se seus respectivos valores de idade de aquisição. Contam-se,
        separadamente, as palavras de conteúdo que tenham valor de idade de aquisição entre 5,5 e 7. Depois divide-se o
        resultado pela quantidade total de palavras de conteúdo presentes no repositório psicolinguístico.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico Limitações da
        métrica: depende do desempenho do nlpnet. O repositório psicolinguístico tem 26.874 palavras e pode não conter
        todas as palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito
        a vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
        idade de aquisição e imageabilidade, levantados junto a usuários da língua por psicolinguistas e psicólogos.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Segundo o chefe substituto do escritório regional, Guaracy Cunha, ainda há tempo para o pedido de
        licença.

        **Contagens**:

        9 palavras de conteúdo e respectivas idades de aquisição (os 2 nomes próprios são palavras de conteúdo, mas não
        têm idade de aquisição, por serem nomes de pessoas):

        tempo (2,39),
        ainda (3,89),
        chefe (4,12),
        licença (4,57).
        há (5,10),
        pedido (5,26),
        escritório (5,35),
        substituto (6,00),
        regional (6,24),

        9 palavras de conteúdo identificadas e lematizadas: 'chefe', 'substituto', 'escritório', 'regional', 'ainda',
        'haver', 'tempo', 'pedido', 'licença'

        2 palavras no intervalo de 5,5 e 7 de idade de aquisição (substituto e regional)

        **Resultado Esperado**: 0,222 (2/9)

        **Resultado Obtido**: 0,222

        **Status**: correto
    """

    name = 'Idade Aquisicao entre 5,5 e 7'
    column_name = 'idade_aquisicao_55_7_ratio'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
        words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
        words = [i for i in words if i]
        total = 0
        count = 0
        for word in words:
            if word in rp.psicolinguistico():
                total += 1
                if rp.psicolinguistico()[word]['idade_aquisicao'] >= 5.5 and rp.psicolinguistico()[word]['idade_aquisicao'] < 7:
                    count += 1
        try:
            return count / total
        except:
            return 0


# class IdadeAquisicao_4_mais(base.Metric):
#     """
#         **Nome da Métrica**: idade_aquisicao_4_maior_ratio
#
#         **Interpretação**: quanto menor o valor de idade de aquisição, menor a idade de aquisição e menor a complexidade
#         textual
#
#         **Descrição da métrica**: Proporção de palavras de conteúdo do texto com valor de idade de aquisição maior ou
#         igual a 4, em relação a todas as palavras de conteúdo do texto presentes no repositório psicolinguístico
#
#         **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
#         substantivos, verbos, adjetivos e advérbios. Idade de aquisição é uma característica psicolinguística das
#         palavras de conteúdo e representa o intervalo de idade em que a palavra foi adquirida. Os valores variam de
#         1 a 7 e quanto menor o valor, menor a idade de aquisição. Os valores correspondem a faixas de idade. 1 (de
#         0 a 2 anos); 2 (de 3 a 4 anos), 3 (de 5 a 6 anos), 4 (de 7 a 8 anos), 5 (de 9 a 10 anos), 6 (de 11 a 12 anos),
#         7 (13 anos ou mais).
#
#         **Forma de cálculo da métrica**: Identificam-se as palavras de conteúdo do texto. Em seguida, contam-se as
#         palavras de conteúdo que estão no repositório psicolinguístico e procuram-se seus respectivos valores de idade
#         de aquisição. Contam-se, separadamente, as palavras de conteúdo que tenham valor de idade de aquisição maior
#         que 4. Depois divide-se o resultado pela quantidade total de palavras de conteúdo presentes no repositório
#         psicolinguístico.
#
#         **Recursos de PLN utilizados durante o cálculo**: nlpnet, DELAF e repositório psicolinguístico
#
#         **Limitações da métrica**: o repositório psicolinguístico tem 26.874 palavras e pode não conter todas as
#         palavras procuradas. O repositório psicolinguístico foi construído automaticamente (e por isso, sujeito a
#         vieses), usando como semente listas de palavras com seus respectivos valores de concretude, familiaridade,
#         idade de aquisição e imageabilidade levantados junto a usuários da língua por psicolinguistas e psicólogos.
#
#         **Crítica**: havia 8 métricas para cada característica psicolinguística e decidiu-se manter apenas 4, a fim de
#         evitar redundância. Por esse motivo esta métrica foi comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Idade de aquisição maior ou igual que 4'
#     column_name = 'idade_aquisicao_4_maior_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         content_tokens = filter(pos_tagger.tagset.is_content_word, rp.tagged_words(t))
#         words = [rp.stemmer().get_lemma(word, pos) for word, pos in content_tokens]
#         words = [i for i in words if i]
#         total = 0
#         count = 0
#         for word in words:
#             if word in rp.psicolinguistico():
#                 total += 1
#                 if rp.psicolinguistico()[word]['idade_aquisicao'] >= 4:
#                     count += 1
#         try:
#             return count / total
#         except:
#             return 0


class PrepositionDiversity(base.Metric):
    """
        **Nome da Métrica**: preposition_diversity

        **Interpretação**: não está clara a relação entre a diversidade de preposições e a complexidade textual

        **Descrição da métrica**: proporção de preposições distintas em relação ao total de preposições do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**:

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet. Se fosse o Palavras, haveria descontração
        e reconhecimento das locuções prepositivas (multipalavras), pois todas são anotadas como PREP.

        **Limitações da métrica**:

        **Crítica**:

            1) a métrica está utilizando tokenização sem descontração, o que dá muita diferença em matéria de
            preposições. A preposição “por”, por exemplo, é tratada como um caso diferente cada vez que se combina com
            um artigo diferente. Com isso, uma única preposição produz 5 preposições diferentes para fins de cálculo de
            diversidade: por; por+o= pelo; por+a=pela; por+os=pelos; por+as=pelas. O mesmo ocorre para as preposições
            “de” e “a”.

            2) cada um dos tokens que constituem as locuções prepositivas estão sendo tratados como uma preposição. Por
            exemplo, “além de” é contado pelo classificador como duas preposições: “além” e “de”.

        **Projeto**: GUTEN

        **Teste**: Nem é preciso argumentar contra a ineficiência do sistema prisional brasileiro. Ele foi reprovado por
        todas as pessoas para as quais foi solicitada uma avaliação. Nele não se pode confiar e dele não se pode esperar
        nada além do estímulo à violência.

        **Contagens**: 8 preposições, 7 diferentes preposições (contra, de, por, para, em, além de, a)

        **Resultado Esperado**: 0,875

        **Resultado Obtido**: 0,889 (o sistema reconheceu 9 preposições, sendo 8 diferentes)

        **Status**: correto, considerando as limitações da métrica

        **Teste**: Essas pessoas estão vivendo abaixo da linha de pobreza e pouco se pode fazer a respeito disso.

        **Contagens**: 3 preposições, 3 diferentes preposições

        **Resultado Esperado**: 1

        **Resultado Obtido**: 1

        **Status**: correto
    """

    name = 'Preposition Diversity'
    column_name = 'preposition_diversity'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        preps = filter(pos_tagger.tagset.is_preposition, words)
        preps = [p[0].lower() for p in preps]
        if preps:
            return rp.mattr(preps)
        else:
            return 0


class HardConjunctions(base.Metric):
    """
        **Nome da Métrica**: hard_conjunctions_ratio

        **Interpretação**: quanto maior a métrica, maior a complexidade textual

        **Descrição da métrica**: Proporção de conjunções difíceis em relação a todas as palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: “conjunções difíceis” é uma das categorias
        atribuídas por Lívia Cucato, linguista da GUTEN, a um conjunto de conjunções. A lista conjuncoes_fund_2 é de
        conjunções difíceis e a lista conjuncoes_fund_1 é de conjunções fáceis. As duas listas incluem tanto conjunções
        constituídas de uma única palavra quanto locuções conjuntivas (ou seja, duas ou mais palavras que funcionam como
        uma conjunção, como por exemplo: “a fim de que” (conjunção final), “cada vez que” (conjunção temporal) “se bem
        que” (conjunção concessiva)). A lista conjunções_fund_2 é composta das seguintes palavras e expressões: todavia,
        eis, a fim de, ao passo que, para que, conforme, tais, ou seja, contudo, bem como, logo, à medida que,
        entretanto, desde que, mesmo que, ainda que, de acordo com, uma vez que, por sua vez, sobretudo, até, ainda,
        caso, no entanto, nem, quanto, já, como, já que, outrossim, mas também, como também, não só, mas ainda,
        tampouco, senão também, bem assim, ademais, antes, não obstante, sem embargo, ao passo que, de outra forma, em
        todo caso, aliás, de outro modo, por conseguinte, em consequência de, por consequência, consequentemente,
        conseguintemente, isso posto, pelo que, de modo que, de maneira que, de forma que, em vista disso, por onde,
        porquanto, posto que, isto é, ademais, senão, dado que, visto como, vez que, de vez que, pois que, agora, na
        medida em que, sendo que, como que, como quer que, eis que, sendo assim, tal qual, ao invés de, conquanto, por
        muito que, visto que, uma vez que, quanto mais, quanto menos, se bem que, apesar de que, suposto que, ainda
        quando, quando mesmo, a despeito de, conquanto que, sem embargo de que, por outro lado,

        em contrapartida, sem embargo, muito embora, inclusive se, por mais que, por menos que, por pouco que, contanto
        que, salvo se, com tal que, caso que, consoante, tal que, de forma que, à proporção que, ao passo que, mal, tão
        logo, entretanto, sob esse aspecto, sob esse prisma, sob esse ponto de vista, sob esse enfoque, embora,
        portanto, além disso.

        **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de “conjunções difíceis”
        e divide-se pela quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador NLTK

        **Limitações da métrica**:

        **Crítica**:

            1) não se sabe como a lista de conjunções foi compilada, nem o critério para separar as conjunções fáceis
            das difíceis. Há advérbios e preposições misturados na lista, como “agora” e “até” e conjunções ambíguas com
            outras categorias gramaticais, como “mal”.

            2) a proporção deveria ser calculada em relação ao total de conjunções, que é a classe à qual pertencem as
            conjunções difíceis.

        **Projeto**: GUTEN

        **Teste**: Visto que muitas pessoas saíram feridas, foi necessário tomar uma medida imediata a fim de
        neutralizar os danos causados e reverter a situação.

        **Contagens**: 23 palavras e 2 conjunções difíceis (a fim de, visto que)

        **Resultado Esperado**: 2/23 = 0,087

        **Resultado Obtido**: 0,087

        **Status**: correto
    """

    name = 'Hard Conjunctions'
    column_name = 'hard_conjunctions_ratio'

    def value_for_text(self, t, rp=default_rp):
        conj = rp._conjuncoes_fund2()
        lower = ' '.join([' '] + rp.lower_words(t) + [' '])
        count = 0
        for c in conj:
            count += lower.count(' ' + c + ' ') #* len(c.split())
        try:
            return count / len(rp.all_words(t))
        except ZeroDivisionError:
            return 0


class EasyConjunctions(base.Metric):
    """
        **Nome da Métrica**: easy_conjunctions_ratio

        **Interpretação**: quanto maior a métrica, menor a complexidade textual

        **Descrição da métrica**: Proporção de conjunções fáceis em relação a todas as palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: “conjunções fáceis” é uma das categorias
        atribuídas por Lívia Cucato, linguista da GUTEN, a um conjunto de conjunções. A lista conjuncoes_fund_1 é de
        conjunções fáceis e a lista conjuncoes_fund_2 é de conjunções difíceis. As duas listas incluem tanto conjunções
        constituídas de uma única palavra quanto locuções conjuntivas (ou seja, duas ou mais palavras que funcionam como
        uma conjunção, como por exemplo: “a fim de que” (conjunção final), “cada vez que” (conjunção temporal) “se bem
        que” (conjunção concessiva)). A lista conjunções_fund_1 contém as seguintes palavras e expressões: como, se,
        mas, quando, ou, que, porque, e, assim, porém, caso, por isso que

        por isso, por enquanto, enquanto isso, enquanto, pois, além de, então, daí, por exemplo, ou seja, sem que, para
        que, cada vez que, antes que, assim como, tanto quanto, feito, que nem, toda vez que, a não ser que, depois que,
        até que, na medida em que, desde, nem bem, tanto que, segundo, assim que, tanto que, tão que, sem que, ora.

        **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de “conjunções fáceis”
        e divide-se pela quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador NLTK

        **Limitações da métrica**:

        **Crítica**:

            1) A origem do léxico não está descrita. Nenhuma marca é usada para desambiguização é utilizada. Por
            exemplo, o particípio “feito” pode ter várias funções e só esporadicamente é usado como conjunção: “Ele
            chegou feito um foguete”. A ambiguidade afeta a estatística.

            2) Os critérios para separar as conjunções fáceis das difíceis não são claros. Por exemplo, “além de” é
            considerada fácil e “além disso” é considerada difícil.

            3) a proporção deveria ser calculada em relação ao total de conjunções, que é a classe à qual pertencem as
            conjunções fáceis; comparar com o total de palavras enfraquece a métrica.

        **Projeto**: GUTEN

        **Teste**: Eles brincaram o dia todo e foi muito divertido. Além de brincarem, fizeram muitos amigos.

        **Contagens**: 15 palavras e 2 conjunções fáceis (e, além de)

        **Resultado Esperado**: 2/15 = 0,133

        **Resultado Obtido**: 0,133

        **Status**: correto
    """

    name = 'Easy Conjunctions'
    column_name = 'easy_conjunctions_ratio'

    def value_for_text(self, t, rp=default_rp):
        conj = rp._conjuncoes_fund1()
        lower = ' '.join([' '] + rp.lower_words(t) + [' '])
        count = 0
        for c in conj:
            count += lower.count(' ' + c + ' ') #* len(c.split())
        try:
            return count / len(rp.all_words(t))
        except ZeroDivisionError:
            return 0


# class SimpleSentences(base.Metric):
#     """
#         **Nome da Métrica**: single_clause_sentence_ratio
#
#         **Interpretação**: quanto maior o resultado da métrica, menor a complexidade textual
#
#         **Descrição da métrica**: Proporção de sentenças com um único verbo principal em relação à quantidade de
#         sentenças do texto.
#
#         **Definição dos termos que aparecem na descrição da métrica**: verbo principal é todo verbo de conteúdo do
#         texto, ou seja, todo verbo que não é auxiliar
#
#         **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta “V” e subtraem-se as ocorrências da
#         etiqueta “<aux>”. Cada vez que o resultado for 1, acumula-se +1 no contador de sentenças que possuem um único
#         verbo principal. Ao final, divide-se o resultado do contador pela quantidade de sentenças do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:  não há
#
#         **Crítica**: essa métrica já existia sob outra nomenclatura: “Ratio of Sentences With One Clause”, vinda do AIC.
#         Portanto, há duas métricas iguais e uma deve ser excluída.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Apesar de eu não saber se estou entendendo do assunto, eu me esforço ao máximo. No final, vou
#         conseguir.
#
#         **Contagens**: 2 sentenças: a primeira com 4 verbos, um dos quais é auxiliar (estou); a segunda com 2 verbos,
#         um dos quais é auxiliar (vou). Apenas a segunda sentença tem um único verbo principal.
#
#         **Resultado Esperado**: 1 / 2= 0,50
#
#         **Resultado Obtido**: 0,50
#
#         **Status**:correto
#     """
#
#     name = 'Simple Sentences'
#     column_name = 'single_clause_sentence_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         simple_sentences = 0
#         for sentence in sentences:
#             verbs = len(re.findall(' V ', sentence))
#             aux = len(re.findall('<aux>', sentence))
#             # a diferença é 1 se há 1 verbo principal e 0 auxiliar.
#             # a diferença é 0 se há 1 verbo principal e 1 auxiliar.
#             if verbs - aux == 0 or verbs - aux == 1:
#                 simple_sentences += 1
#         try:
#             return simple_sentences / len(sentences)
#         except ZeroDivisionError:
#             return 0


# class DifficultWords25(base.Metric):
#     """
#         **Nome da Métrica**: difficult_words_25
#
#         **Interpretação**: quanto menor a frequência das palavras, maior a complexidade textual
#
#         **Descrição da métrica**: Média dos LOGs das frequências de palavras de conteúdo com frequência menor que 25
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
#         adjetivos e advérbios. O corpus de palavras difíceis é um conjunto de 4 listas de palavras de conteúdo com suas
#         respectivas frequências (frequência menor que 200, menor que 100, menor que 50 e menor que 25). O córpus foi
#         compilado com o PLN-Br, um dump da Wikipédia e um dump do G1. Ele foi anotado com o POS tagger nlpnet para
#         filtragem de palavras de conteúdo.
#
#         **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de palavras difíceis com
#         frequência menor que 25; somam-se os logs das frequências das palavras identificadas e divide-se o resultado
#         pela quantidade dessas mesmas palavras.
#
#         **Recursos de PLN utilizados durante o cálculo**: corpus de palavras difíceis (rp.palavras_dificeis)
#
#         **Limitações da métrica**:  a frequência e o log da frequência variam em função do tamanho do corpus; vieses do
#         corpus podem afetar a frequência.
#
#         **Crítica**: vários motivos tornam recomendável comentar (inibir) esta métrica.
#
#         **Esta métrica está contida em três outras**: a de palavras com frequência menor que 50, 100 e 200. Acreditamos
#         que seria melhor se as faixas fossem mutuamente excludentes. Se um texto tiver 3 palavras com frequência 18, 10
#         e 7, por exemplo, todas as 4 métricas darão o mesmo resultado. O tamanho das listas é muito grande (a de 25 tem
#         664.052, a de 50 tem 686.722, a de 100 tem 703.706 e a de 200 tem 716.928), o que impacta no tempo computacional
#         do cálculo da métrica. Além disso, as listas de palavras não sofreram limpeza para exclusão de palavras erradas,
#         palavras estrangeiras, com caixa alta ou com junção de mais de uma.
#
#         **Projeto**: GUTEN
#
#     """
#
#     name = 'Difficult Words of Frequency Lower than 25'
#     column_name = 'difficult_words_25'
#
#     def value_for_text(self, t, rp=default_rp):
#         dificeis = rp.palavras_dificeis()
#         cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
#
#         return rp.log_for_words(cw, dificeis[25])


# class DifficultWords50(base.Metric):
#     """
#         **Nome da Métrica**: difficult_words_50
#
#         **Interpretação**: quanto menor a frequência das palavras, maior a complexidade textual
#
#         **Descrição da métrica**: Média dos LOGs das frequências de palavras de conteúdo com frequência menor que 50
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
#         adjetivos e advérbios. O corpus de palavras difíceis é um conjunto de 4 listas de palavras de conteúdo com suas
#         respectivas frequências (frequência menor que 200, menor que 100, menor que 50 e menor que 25). O córpus foi
#         compilado com o PLN-Br, um dump da Wikipédia e um dump do G1. Ele foi anotado com o POS tagger nlpnet para
#         filtragem de palavras de conteúdo.
#
#         **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de palavras difíceis com
#         frequência menor que 50; somam-se os logs das frequências das palavras identificadas e divide-se o resultado
#         pela quantidade dessas mesmas palavras.
#
#         **Recursos de PLN utilizados durante o cálculo**: corpus de palavras difíceis (rp.palavras_dificeis); POS tagger
#         nlpnet
#
#         **Limitações da métrica**: a frequência e o log da frequência variam em função do tamanho do corpus; vieses do
#         corpus podem afetar a frequência.
#
#         **Crítica**: vários motivos tornam recomendável comentar (inibir) esta métrica.
#
#         **Esta métrica está contida em duas outras**: a de palavras com frequência menor que 100 e 200. Acreditamos que
#         seria melhor se as faixas fossem mutuamente excludentes. Se um texto tiver 3 palavras com frequência 38, 30 e
#         27, por exemplo, as 3 métricas darão o mesmo resultado.
#
#         O tamanho das listas é muito grande (a de 25 tem 664.052, a de 50 tem 686.722, a de 100 tem 703.706 e a de 200
#         tem 716.928), o que impacta no tempo computacional do cálculo da métrica. Além disso, as listas de palavras não
#         sofreram limpeza para exclusão de palavras erradas, palavras estrangeiras, com caixa alta ou com junção de mais
#         de uma.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Difficult Words of Frequency Lower than 50'
#     column_name = 'difficult_words_50'
#
#     def value_for_text(self, t, rp=default_rp):
#         dificeis = rp.palavras_dificeis()
#         cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
#
#         return rp.log_for_words(cw, dificeis[50])


# class DifficultWords100(base.Metric):
#     """
#         **Nome da Métrica**: difficult_words_100
#
#         **Interpretação**: quanto menor a frequência das palavras, maior a complexidade textual
#
#         **Descrição da métrica**: Média dos LOGs das frequências de palavras de conteúdo com frequência menor que 100
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
#         adjetivos e advérbios. O corpus de palavras difíceis é um conjunto de 4 listas de palavras de conteúdo com suas
#         respectivas frequências (frequência menor que 200, menor que 100, menor que 50 e menor que 25). O córpus foi
#         compilado com o PLN-Br, um dump da Wikipédia e um dump do G1. Ele foi anotado com o POS tagger nlpnet para
#         filtragem de palavras de conteúdo.
#
#         **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de palavras difíceis com
#         frequência menor que 100; somam-se os logs das frequências das palavras identificadas e divide-se o resultado
#         pela quantidade dessas mesmas palavras
#
#         **Recursos de PLN utilizados durante o cálculo**: corpus de palavras difíceis (rp.palavras_dificeis); POS tagger
#         nlpnet
#
#         **Limitações da métrica**:  a frequência e o log da frequência variam em função do tamanho do corpus; vieses do
#         corpus podem afetar a frequência.
#
#         **Crítica**: vários motivos tornam recomendável comentar (inibir) esta métrica.
#
#         **Esta métrica está contida em outra**: a de palavras com frequência menor que 200.  Acreditamos que seria
#         melhor se as faixas fossem mutuamente excludentes. Se um texto tiver 3 palavras com frequência 88, 70 e 67, por
#         exemplo, as 2 métricas darão o mesmo resultado.
#
#         O tamanho das listas é muito grande (a de 25 tem 664.052, a de 50 tem 686.722, a de 100 tem 703.706 e a de 200
#         tem 716.928), o que impacta no tempo computacional do cálculo da métrica. Além disso, as listas de palavras não
#         sofreram limpeza para exclusão de palavras erradas, palavras estrangeiras, com caixa alta ou com junção de mais
#         de uma.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Difficult Words of Frequency Lower than 100'
#     column_name = 'difficult_words_100'
#
#     def value_for_text(self, t, rp=default_rp):
#         dificeis = rp.palavras_dificeis()
#         cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
#
#         return rp.log_for_words(cw, dificeis[100])


# class DifficultWords200(base.Metric):
#     """
#         **Nome da Métrica**: difficult_words_200
#
#         **Interpretação**: quanto menor a frequência das palavras, maior a complexidade textual
#
#         **Descrição da métrica**: Média dos LOGs das frequências de palavras de conteúdo com frequência menor que 200
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
#         adjetivos e advérbios. O corpus de palavras difíceis é um conjunto de 4 listas de palavras de conteúdo com suas
#         respectivas frequências (frequência menor que 200, menor que 100, menor que 50 e menor que 25). O córpus foi
#         compilado com o PLN-Br, um dump da Wikipédia e um dump do G1. Ele foi anotado com o POS tagger nlpnet para
#         filtragem de palavras de conteúdo.
#
#         **Forma de cálculo da métrica**: identificam-se as palavras do texto que estão na lista de palavras difíceis com
#         frequência menor que 200;  somam-se os logs das frequências das palavras identificadas e divide-se o resultado
#         pela quantidade dessas mesmas palavras.
#
#         **Recursos de PLN utilizados durante o cálculo**: corpus de palavras difíceis (rp.palavrass_dificeis); POS
#         tagger nlpnet
#
#         **Limitações da métrica**:  a frequência e o log da frequência variam em função do tamanho do corpus; vieses do
#         corpus podem afetar a frequência. O corte que separa as palavras fáceis das difíceis (frequências abaixo de 200)
#         é totalmente arbitrário e atrelado ao tamanho do corpus escolhido.
#
#         **Crítica**: vários motivos tornam recomendável comentar (inibir) esta métrica.
#
#         Acreditamos que seria melhor se as faixas de frequência das palavras difíceis fossem mutuamente excludentes. O
#         tamanho das listas é muito grande (a de 25 tem 664.052, a de 50 tem 686.722, a de 100 tem 703.706 e a de 200 tem
#         716.928), o que impacta no tempo computacional do cálculo da métrica. Além disso, as listas de palavras não
#         sofreram limpeza para exclusão de palavras erradas, palavras estrangeiras, com caixa alta ou com junção de mais
#         de uma.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Difficult Words of Frequency Lower than 200'
#     column_name = 'difficult_words_200'
#
#     def value_for_text(self, t, rp=default_rp):
#         dificeis = rp.palavras_dificeis()
#         cw = [i.lower() for i in chain.from_iterable(rp.content_words(t))]
#
#         return rp.log_for_words(cw, dificeis[200])


class IndefinitePronounsDiversity(base.Metric):
    """
        **Nome da Métrica**: indefinite_pronouns_diversity

        **Interpretação**: não é clara a relação entre a métrica e a complexidade textual, mas é provável que pronomes
        indefinidos tornem o texto mais complexo

        **Descrição da métrica**: Proporção  de types de  pronomes indefinidos em relação à quantidade de tokens de
        pronomes indefinidos no texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes indefinidos são pronomes genéricos
        (nada, ninguém, alguém, nenhum, algum, qualquer, etc.). Tokens são todas as ocorrências das palavras; types
        são todas as ocorrências das palavras sem considerar repetições.

        **Forma de cálculo da métrica**: contam-se os pronomes indefinidos no texto, usando uma lista de pronomes
        indefinidos. Depois contam-se apenas as ocorrências diferentes, ou seja, se houver três ocorrências de
        “qualquer”, conta-se apenas uma vez. Finalmente, divide-se o resultado pela quantidade de pronomes indefinidos
        do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador e lista de pronomes indefinidos

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Tudo que sempre quisemos é ver nossos filhos felizes. Ninguém imagina que há situações em que nada
        pode ser feito para garantir isso. Por isso, é difícil alguém se conformar diante das doenças terminais que
        acometem crianças. Aliás, ninguém se conforma.

        **Contagens**: 5 tokens de pronomes indefinidos (tudo, ninguém, nada, alguém, ninguém), 4 types (tudo, ninguém,
        nada, alguém)

        **Resultado Esperado**: 4/5 = 0,80

        **Resultado Obtido**: 0,80

        **Status**: correto
    """

    name = 'Indefinite Pronouns Diversity'
    column_name = 'indefinite_pronouns_diversity'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        nouns = filter(pos_tagger.tagset.is_pronoun, words)
        nouns = [n[0].lower() for n in nouns]
        indefinite_list = rp._pronomes_indefinidos()
        match = [n for n in nouns if n in indefinite_list]
        if match:
            return rp.mattr(match)
        else:
            return 0
        # uniques = list(set(match))
        # return len(uniques) / len(match)


class IndefinitePronouns(base.Metric):
    """
        **Nome da Métrica**: indefinite_pronoun_ratio

        **Interpretação**: é provável que pronomes indefinidos contribuam para maior complexidade textual

        **Descrição da métrica**: Proporção de pronomes indefinidos em relação a todos os pronomes do texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes indefinidos são pronomes genéricos
        (nada, ninguém, alguém, nenhum, algum, qualquer, etc.).

        **Forma de cálculo da métrica**: identificam-se todos os pronomes do texto (tags: 'PROPESS','PROSUB', 'PROADJ',
        'PRO-KS', 'PRO-KS-REL' do nlpnet); contam-se as ocorrências de pronomes indefinidos, usando uma lista de
        pronomes indefinidos para identificá-los; depois divide-se o resultado pela quantidade total de pronomes no
        texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger do nlpnet e lista de pronomes indefinidos.

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Minha primeira tentativa fracassou, mas agora eu atingi meu objetivo e obtive tudo o que eu queria.
        Ninguém, além de você, me ajudou. Sua colaboração foi muito importante para mim.

        **Contagens**: 12 pronomes (minha, eu, meu, tudo, o, que, eu, ninguém, você, me, sua, mim), 2 pronomes
        indefinidos (tudo, ninguém)

        **Resultado Esperado**: 2/12 = 0,167

        **Resultado Obtido**: 0,167

        **Status**: correto
    """

    name = 'Ratio of Indefinite Pronouns'
    column_name = 'indefinite_pronoun_ratio'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        nouns = filter(pos_tagger.tagset.is_pronoun, words)
        nouns = [n[0].lower() for n in nouns]
        indefinite_list = rp._pronomes_indefinidos()
        match = [n for n in nouns if n in indefinite_list]
        if nouns:
            return len(match) / len(nouns)
        else:
            return 0


class AbstractNouns(base.Metric):
    """
        **Nome da Métrica**: abstract_nouns_ratio

        **Interpretação**: substantivos abstratos são mais complexos que substantivos concretos, portanto, quanto maior
        a proporção desses substantivos, maior a complexidade.

        **Descrição da métrica**: Proporção de substantivos abstratos em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: para fins desta métrica, são considerados
        substantivos abstratos os substantivos terminados com os sufixos -mento, -ção, -são, -agem, -mento, -ura, -ncia,
        -dela, -ria.

        **Forma de cálculo da métrica**: filtram-se todos os substantivos e contam-se aqueles que possuem a terminação
        definida para a métrica. Depois divide-se o resultado pelo total de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:  a principal limitação é de ordem conceitual. Sem um stemmer (separador de radicais),
        não é possível saber se a terminação é sufixo ou não. Por exemplo, -ção é sufixo em “profissionalização”, mas
        não é sufixo em “ração”. Além disso, a métrica parte do pressuposto de que há sufixos exclusivos de palavras
        abstratas, o que não é verdadeiro. Por exemplo:  sangramento, folhagem, ranhura e padaria apresentam as
        terminações definidas para a métrica e são palavras com alto grau de concretude. Por outro lado, há palavras
        abstratas derivadas de verbo que não são capturadas, como “coordenadora”, como no exemplo-teste.

        **Crítica**: como se trata de um tipo de substantivo, o ideal seria calcular a proporção em relação ao total de
        substantivos

        **Projeto**: GUTEN

        **Teste**: A coordenadora de Memória da Secretaria de Cultura, Miriam Avruch, garante que metade do valor já
        foi paga.

        **Contagens**: 3 substantivos com as terminações definidas: memória, secretaria, cultura e 18 palavras

        **Resultado Esperado**: 0,167 (3/18)

        **Resultado Obtido**: 0,167

        **Status**: correto

    """

    name = 'Ratio of Abstract Nouns to Words'
    column_name = 'abstract_nouns_ratio'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        nouns = filter(pos_tagger.tagset.is_noun, words)
        sufixes = ['mento', 'ção', 'agem', 'ura', 'são', 'ncia', 'dela', 'ria']
        match = [n for n in nouns for s in sufixes if n[0].endswith(s)]
        return len(match) / len(words)


# class SimpleVerbs(base.Metric):
#     """
#         **Nome da Métrica**: simple_verb_ratio
#
#         **Interpretação**: quanto maior o resultado da métrica, menor a complexidade
#
#         **Descrição da métrica**: Proporção de verbos simples em relação a todos os verbos do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: verbos simples são os verbos constantes da lista
#         de palavras simples compilada a partir do dicionário de palavras simples de Maria Tereza Biderman.
#
#         **Forma de cálculo da métrica**: identificam-se todos os verbos do texto (etiquetas V, VAUX e PCP do nlpnet);
#         verifica-se quais deles estão na lista de verbos simples. Contam-se as ocorrências de verbos simples e divide-se
#         o resultado pela quantidade de verbos do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet para identificar verbos e lista de palavras
#         simples
#
#         **Limitações da métrica**: só reconhece verbos no infinitivo, pois o dicionário é formado por lemas.
#
#         **Críticas**: Esta métrica deve ser comentada porque já está contida na métrica de palavras simples, que foi
#         corrigida para incluir lematização.
#
#         Verbos auxiliares estão presentes em todos os níveis de complexidade textual, pois constituem palavras
#         funcionais, por isso não deveriam fazer parte do cálculo. Esta métrica está contida na métrica do AIC que
#         verifica as palavras simples, com base na mesma lista de palavras (dicionário Biderman);
#
#         **Projeto**: GUTEN
#
#         **Teste**: Caso houvesse um candidato honesto, estaríamos contentes.
#
#         **Contagens**: 2 verbos (houvesse, estaríamos), ambos formas de lemas simples (haver e ser)
#
#         **Resultado Esperado**: 1 (2/2)
#
#         **Resultado Obtido**: 0 (pois nenhuma das formas está no infinitivo)
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Simple Verbs'
#     column_name = 'simple_verb_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         sw = rp.simple_words()
#         verbs = [t for t in rp.tagged_words(t)
#                  if pos_tagger.tagset.is_verb(t) or
#                  pos_tagger.tagset.is_auxiliary_verb(t) or
#                  pos_tagger.tagset.is_participle(t)]
#         verbs = list(map(lambda t: t[0], verbs))
#         count = sum(1 for v in verbs if v in sw)
#         return count / len(verbs)


# class AdverbialsLevel3(base.Metric):
#     """
#         **Nome da Métrica**: adverbials_03_ratio
#
#         **Interpretação**: orações subordinadas adverbiais estão relacionadas a maior complexidade
#
#         **Descrição da métrica**: Proporção de orações subordinadas adverbiais de nível 3 em relação à quantidade de
#         orações do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: oração adverbial é um tipo de oração subordinada.
#         Ela se encaixa na oração principal, funcionando como adjunto adverbial. Há 9 tipos de orações adverbiais:
#         causais, comparativas, concessivas, condicionais, conformativas, consecutivas, finais, proporcionais e temporais. 
#         As orações subordinadas adverbiais podem ser introduzidas por conjunções subordinativas (KS), mas nem toda
#         oração subordinada introduzida por conjunção subordinativa é adverbial. Há orações subordinadas adverbiais
#         reduzidas de gerúndio, particípio e infinitivo, as quais não estão sendo capturadas pela métrica.
#
#         **Forma de cálculo da métrica**: identificam-se as sequências lexicais definidas na lista e contam-se as
#         ocorrências. Depois divide-se o resultado pela soma de ocorrências de KS, KC e <rel>.
#
#         **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet
#
#         **Limitações da métrica**:
#
#         **Crítica**: vários motivos justificam a recomendação de comentar esta métrica:
#
#             1) A forma de cálculo da quantidade de orações (denominador do cálculo) está errada
#
#             2) a lista de palavras que introduzem orações adverbiais precisa ser revista;
#
#             3) das 9 classes de orações adverbiais existentes, o léxico só apresenta 5
#
#             4) há uma classe definida que não existe: explicativas (que associa-se à etiqueta <rel>) Somente orações
#             subordinadas adjetivas têm uma subcategoria chamada “explicativas”;
#
#             5) as listas de nível 1, 2 e 3 não são mutuamente excludentes;
#
#             6) há palavras que possuem função ambígua e  não há pistas para desambiguização
#
#             7) é necessário associar etiquetas que identifiquem conjunções subordinativas (KS) às palavras do léxico,
#             para melhorar sua precisão;
#
#             8) a oração introduzida por uma conjunção subordinativa nem sempre é adverbial. Por exemplo: “Não sei se
#             vou viajar” (a oração introduzida por “se” é subordinada substantiva objetiva direta e não adverbial
#             condicional, como a métrica consideraria):
#
#                 não [não] ADV @ADVL>
#                 sei [saber] <fmc> <vt> V PR 1S IND VFIN @FMV
#                 se [se] KS @SUB @#FS-<ACC
#                 vou [ir] V PR 1S IND VFIN @FAUX
#                 viajar [viajar] <vi> V INF @IMV @#ICL-AUX<
#
#             9) A precisão aumentaria se a oração fosse capturada pela etiqueta do parser Palavras que identifica orações
#             adverbiais. Ex:
#
#                 se [se] KS @SUB @#FS-ADVL>
#                 você [você] PERS M/F 3S NOM @SUBJ>
#                 vier [vir] <vi> V FUT 3S SUBJ VFIN @FMV
#                 eu [eu] PERS M/F 1S NOM @SUBJ>
#                 prometo [prometer] <fmc> <vt> V PR 1S IND VFIN @FMV
#                 que [que] KS @SUB @#FS-<ACC
#                 lhe [ele] PERS M/F 3S DAT @DAT>
#                 darei [dar] <vdt> V FUT 1S IND VFIN @FMV
#                 atenção [atenção] <am> N F S @<ACC
#
#         **Projeto**: GUTEN
#
#     """
#
#     name = 'Ratio of Adverbials Level 3 to Coordinate and Subordinate Clauses'
#     column_name = 'adverbials_03_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         expression = re.compile('''
#                                 \[a=fim=de\]|                   # final
#                                 \[a=fim=de=que\]|               # final
#                                 \[porque\]|                     # final
#                                 \[já=que\]|        # causal
#                                 \[porquanto\]|                  # causal
#                                 \[uma=vez=que\]|                # causal
#                                 \[visto=que\]|                  # causal
#                                 \[como\]|                       # causal
#                                 \[que\].*<rel>|                 # explicativa
#                                 \[onde\]|                       # explicativa
#                                 \[quando\]|                     # explicativa
#                                 \[quem\]|                       # explicativa
#                                 \[quanto\]|                     # explicativa
#                                 \[assim=que\]|                  # temporal
#                                 \[logo=que\]|                   # temporal
#                                 \[contanto=que\]|               # condicional
#                                 \[se\].*KS|                     # condicional
#                                 \[caso\].*KS|                   # condicional
#                                 \[a=menos=que\]                 # condicional
#                                 \[a=não=ser=que]|  # condicional
#                                 \[exceto=se\]|                  # condicional
#                                 \[salvo=se\]|                   # condicional
#                                 \[desde=que\]|                  # condicional
#                                 \[apesar=de=que\]|              # concessiva
#                                 \[embora\]|                     # concessiva
#                                 \[mas\]|                        # concessiva
#                                 \[conquanto\]|                  # concessiva
#                                 \[ainda=que\]|                  # concessiva
#                                 \[mesmo=que\]|                  # concessiva
#                                 \[nem=que\]|                    # concessiva
#                                 \[por=mais=que\]|               # concessiva
#                                 \[posto=que\]|                  # concessiva
#                                 \[por=muito=que\]|              # concessiva
#                                 \[de=forma=que\]|               # consecutiva
#                                 \[de=modo=que\]|                # consecutiva
#                                 \[conforme\]|                   # consecutiva
#                                 \[consoante\]|                  # consecutiva
#                                 \[segundo\]|                    # consecutiva
#                                 \[como\]                        # consecutiva
#                                 ''',
#                                 re.VERBOSE)
#         ocorrencias1 = len(re.findall(expression, flat))
#         # casos não capturados por expressão regular
#         ocorrencias2 = sum(
#             [
#                 lower.count('para que'),      # final
#                 lower.count('depois de'),     # temporal
#                 lower.count('depois que'),    # temporal
#                 lower.count('antes que'),     # condicional
#                 lower.count('sem que'),       # condicional
#                 lower.count('apesar que'),    # concessiva
#                 lower.count('tamanho que'),   # consecutiva
#                 lower.count('tal que'),       # consecutiva
#                 lower.count('tanto que'),     # consecutiva
#
#             ]
#         )
#         try:
#             return (ocorrencias1 + ocorrencias2) / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class AdverbialsLevel2(base.Metric):
#     """
#         **Nome da Métrica**: adverbials_02_ratio
#
#         **Interpretação**: orações subordinadas adverbiais estão relacionadas a maior complexidade
#
#         **Descrição da métrica**: Proporção de orações subordinadas adverbiais de nível 2 em relação à quantidade de
#         orações do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: oração adverbial é um tipo de oração subordinada.
#         Ela se encaixa na oração principal, funcionando como adjunto adverbial. Há 9 tipos de orações adverbiais:
#         causais, comparativas, concessivas, condicionais, conformativas, consecutivas, finais, proporcionais e temporais. 
#         As orações subordinadas adverbiais podem ser introduzidas por conjunções subordinativas (KS), mas nem toda
#         oração subordinada introduzida por conjunção subordinativa é adverbial. Há orações subordinadas adverbiais
#         reduzidas de gerúndio, particípio e infinitivo, as quais não estão sendo capturadas pela métrica.
#
#         **Forma de cálculo da métrica**: identificam-se as sequências lexicais definidas na lista e contam-se as
#         ocorrências. Depois divide-se o resultado pela soma de ocorrências de KS, KC e <rel>.
#
#         **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet
#
#         **Limitações da métrica**:
#
#         **Crítica**: vários motivos justificam a recomendação de comentar esta métrica:
#
#             1) A forma de cálculo da quantidade de orações (denominador do cálculo) está errada
#
#             2) a lista de palavras que introduzem orações adverbiais precisa ser revista;
#
#             3) das 9 classes existentes, o léxico só apresenta 5
#
#             4) há uma classe definida que não existe: explicativas (que associa-se à etiqueta <rel>) Somente orações
#             subordinadas adjetivas têm uma subcategoria chamada “explicativas”;
#
#             5) as listas de nível 1, 2 e 3 não são mutuamente excludentes;
#
#             6) há palavras que possuem função ambígua e  não há pistas para desambiguização
#
#             7) é necessário associar etiquetas que identifiquem conjunções subordinativas (KS) às palavras do léxico,
#             para melhorar sua precisão;
#
#             8) a oração introduzida por uma conjunção subordinativa nem sempre é adverbial. Por exemplo: “Não sei se
#             vou viajar” (a oração introduzida por “se” é subordinada substantiva objetiva direta e não adverbial
#             condicional, como a métrica consideraria):
#
#                 não [não] ADV @ADVL>
#                 sei [saber] <fmc> <vt> V PR 1S IND VFIN @FMV
#                 se [se] KS @SUB @#FS-<ACC
#                 vou [ir] V PR 1S IND VFIN @FAUX
#                 viajar [viajar] <vi> V INF @IMV @#ICL-AUX<
#
#             9) A precisão aumentaria se a oração fosse capturada pela etiqueta do parser Palavras que identifica orações
#             adverbiais. Ex:
#
#                 se [se] KS @SUB @#FS-ADVL>
#                 você [você] PERS M/F 3S NOM @SUBJ>
#                 vier [vir] <vi> V FUT 3S SUBJ VFIN @FMV
#                 eu [eu] PERS M/F 1S NOM @SUBJ>
#                 prometo [prometer] <fmc> <vt> V PR 1S IND VFIN @FMV
#                 que [que] KS @SUB @#FS-<ACC
#                 lhe [ele] PERS M/F 3S DAT @DAT>
#                 darei [dar] <vdt> V FUT 1S IND VFIN @FMV
#                 atenção [atenção] <am> N F S @<ACC
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Ratio of Adverbials Level 2 to Coordinate and Subordinate Clauses'
#     column_name = 'adverbials_02_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         expression = re.compile('''
#                                 \[a=fim=de\]|                   # final
#                                 \[a=fim=de=que\]|               # final
#                                 \[porque\]|                     # final
#                                 \[já=que\]|                     # causal
#                                 \[porquanto\]|                  # causal
#                                 \[uma=vez=que\]|                # causal
#                                 \[visto=que\]|                  # causal
#                                 \[como\]|                       # causal
#                                 \[que\].*<rel>|                 # explicativa
#                                 \[onde\]|                       # explicativa
#                                 \[quando\]|                     # explicativa
#                                 \[quem\]|                       # explicativa
#                                 \[quanto\]|                     # explicativa
#                                 \[assim=que\]|                  # temporal
#                                 \[logo=que\]|                   # temporal
#                                 \[contanto=que\]|               # condicional
#                                 \[se\].*KS|                     # condicional
#                                 \[caso\].*KS|                   # condicional
#                                 \[a=menos=que\]                 # condicional
#                                 \[a=não=ser=que]|               # condicional
#                                 \[exceto=se\]|                  # condicional
#                                 \[salvo=se\]|                   # condicional
#                                 \[desde=que\]|                  # condicional
#                                 \[apesar=de=que\]|              # concessiva
#                                 \[embora\]|                     # concessiva
#                                 \[mas\]|                        # concessiva
#                                 \[conquanto\]|                  # concessiva
#                                 \[ainda=que\]|                  # concessiva
#                                 \[mesmo=que\]|                  # concessiva
#                                 \[nem=que\]|                    # concessiva
#                                 \[por=mais=que\]|               # concessiva
#                                 \[posto=que\]|                  # concessiva
#                                 \[por=muito=que\]               # concessiva
#                                 ''',
#                                 re.VERBOSE)
#         ocorrencias1 = len(re.findall(expression, flat))
#         # casos não capturados por expressão regular
#         ocorrencias2 = sum(
#             [
#                 lower.count('para que'),      # final
#                 lower.count('depois de'),     # temporal
#                 lower.count('depois que'),    # temporal
#                 lower.count('antes que'),     # condicional
#                 lower.count('sem que'),       # condicional
#                 lower.count('apesar que'),    # concessiva
#
#             ]
#         )
#         try:
#             return (ocorrencias1 + ocorrencias2) / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class AdverbialsLevel1(base.Metric):
#     """
#         **Nome da Métrica**: adverbials_01_ratio
#
#         **Interpretação**: orações subordinadas adverbiais estão relacionadas a maior complexidade
#
#         **Descrição da métrica**: Proporção de orações subordinadas adverbiais de nível 1 em relação à quantidade de
#         orações do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: oração adverbial é um tipo de oração subordinada.
#         Ela se encaixa na oração principal, funcionando como adjunto adverbial. Há 9 tipos de orações adverbiais:
#         causais, comparativas, concessivas, condicionais, conformativas, consecutivas, finais, proporcionais e temporais.
#         As orações subordinadas adverbiais podem ser introduzidas por conjunções subordinativas (KS), mas nem toda
#         oração subordinada introduzida por conjunção subordinativa é adverbial. Há orações subordinadas adverbiais
#         reduzidas de gerúndio, particípio e infinitivo, as quais não estão sendo capturadas pela métrica.
#
#         **Forma de cálculo da métrica**: identificam-se as sequências lexicais definidas na lista e contam-se as
#         ocorrências. Depois divide-se o resultado pela soma de ocorrências de KS, KC e <rel>.
#
#         **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet
#
#         **Limitações da métrica**:
#
#         **Crítica**: vários motivos justificam a recomendação de comentar esta métrica:
#
#             1) A forma de cálculo da quantidade de orações (denominador do cálculo) está errada
#
#             2) a lista de palavras que introduzem orações adverbiais precisa ser revista;
#
#             3) das 9 classes existentes, o léxico só apresenta 5
#
#             4) há uma classe definida que não existe: explicativas (que associa-se à etiqueta <rel>) Somente orações
#             subordinadas adjetivas têm uma subcategoria chamada “explicativas”;
#
#             5) as listas de nível 1, 2 e 3 não são mutuamente excludentes;
#
#             6) há palavras que possuem função ambígua e  não há pistas para desambiguização
#
#             7) é necessário associar etiquetas que identifiquem conjunções subordinativas (KS) às palavras do léxico,
#             para melhorar sua precisão;
#
#             8) a oração introduzida por uma conjunção subordinativa nem sempre é adverbial. Por exemplo: “Não sei se vou
#             viajar” (a oração introduzida por “se” é subordinada substantiva objetiva direta e não adverbial
#             condicional, como a métrica consideraria):
#
#                 não [não] ADV @ADVL>
#                 sei [saber] <fmc> <vt> V PR 1S IND VFIN @FMV
#                 se [se] KS @SUB @#FS-<ACC
#                 vou [ir] V PR 1S IND VFIN @FAUX
#                 viajar [viajar] <vi> V INF @IMV @#ICL-AUX<
#
#             9) A precisão aumentaria se a oração fosse capturada pela etiqueta do parser Palavras que identifica orações
#             adverbiais. Ex:
#
#         se [se] KS @SUB @#FS-ADVL>
#         você [você] PERS M/F 3S NOM @SUBJ>
#         vier [vir] <vi> V FUT 3S SUBJ VFIN @FMV
#         eu [eu] PERS M/F 1S NOM @SUBJ>
#         prometo [prometer] <fmc> <vt> V PR 1S IND VFIN @FMV
#         que [que] KS @SUB @#FS-<ACC
#         lhe [ele] PERS M/F 3S DAT @DAT>
#         darei [dar] <vdt> V FUT 1S IND VFIN @FMV
#         atenção [atenção] <am> N F S @<ACC
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Ratio of Adverbials Level 1 to All Clauses'
#     column_name = 'adverbials_01_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         lower = t.raw_content.lower()
#         expression = re.compile('''
#                                 \[a=fim=de\]|                   # final
#                                 \[a=fim=de=que\]|               # final
#                                 \[porque\]|                     # final
#                                 \[já=que\]|                     # causal
#                                 \[porquanto\]|                  # causal
#                                 \[uma=vez=que\]|                # causal
#                                 \[visto=que\]|                  # causal
#                                 \[como\]|                       # causal
#                                 \[que\].*<rel>|                 # explicativa
#                                 \[onde\]|                       # explicativa
#                                 \[quando\]|                     # explicativa
#                                 \[quem\]|                       # explicativa
#                                 \[quanto\]|                     # explicativa
#                                 \[assim=que\]|                  # temporal
#                                 \[logo=que\]|                   # temporal
#                                 \[contanto=que\]|               # condicional
#                                 \[se\].*KS|                     # condicional
#                                 \[caso\].*KS|                   # condicional
#                                 \[a=menos=que\]                 # condicional
#                                 \[a=não=ser=que]                # condicional
#                                 \[exceto=se\]                   # condicional
#                                 \[salvo=se\]                    # condicional
#                                 \[desde=que\]                   # condicional
#                                 \[se=bem=que\]                  # condicional
#                                 ''',
#                                 re.VERBOSE)
#         ocorrencias1 = len(re.findall(expression, flat))
#         # casos não capturados por expressão regular
#         ocorrencias2 = sum(
#             [
#                 lower.count('para que'),      # final
#                 lower.count('depois de'),     # temporal
#                 lower.count('depois que'),    # temporal
#                 lower.count('antes que'),     # condicional
#                 lower.count('sem que'),       # condicional
#             ]
#         )
#         try:
#             return (ocorrencias1 + ocorrencias2) / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class DiscourseMarkersEasy(base.Metric):
#     """
#         **Nome da Métrica**: discourse_markers_easy
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual. Se a proporção de marcadores
#         discursivos fáceis fosse calculada em relação a todos os marcadores discursivos do texto, esta métrica seria
#         inversamente proporcional à complexidade textual (quanto maior a métrica, menor a complexidade).
#
#         **Descrição da métrica**: Proporção de marcadores discursivos fáceis em relação à quantidade de orações do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: Quantidade de orações é um número obtido por meio
#         da contagem das etiquetas “V” menos as etiquetas <aux> do parser Palavras ou seja, cada verbo principal
#         representa uma oração. Marcadores discursivos fáceis são os seguintes (informados diretamente no código de
#         extração da métrica):  ainda, antes, como, e, mal, mas, nem, ora, ou, para, porque, primeiro, quando, que, se,
#         tal, também, tanto, tão
#
#         **Forma de cálculo da métrica**: contam-se os marcadores discursivos fáceis, usando a lista do próprio código
#         para identificá-los; divide-se o resultado pela quantidade de orações do texto. Recursos de PLN utilizados
#         durante o cálculo: parser Palavras para contar as orações
#
#         **Limitações da métrica**:  não prevê a ambiguidade funcional das palavras
#
#         **Crítica**: vários motivos tornam recomendável inibir (comentar) esta métrica
#
#             1) a origem da lista de marcadores discursivos não está descrita
#
#             2) a lista de marcadores discursivos contém palavras que não são marcadores discursivos ou que podem ter
#             outras funções além de marcador discursivo
#
#             3) marcas para desambiguização de marcadores discursivos, como a vírgula, não são usadas,
#
#             4) os critérios para dividir os marcadores discursivos em 4 níveis não estão explícitos;
#
#             5) palavras ambíguas funcionalmente deveriam ser suprimidas do léxico de marcadores;
#
#             6) a proporção deveria ser em relação ao total de marcadores discursivos.
#
#         **Projeto**: GUTEN
#
#         **Teste**: O médico ainda não chegou e o paciente está passando mal. Por isso, o primeiro que chegar será
#         chamado para dar assistência urgente.
#
#         **Contagens**: 2 sentenças: na primeira 1 marcador discursivo fácil (e) e 2 orações; na segunda sentença, 1
#         marcador discursivo não fácil (por isso) e 3 orações
#
#         **Resultado Esperado**: 1/5 = 0,20
#
#         **Resultado Obtido**: 1,20 (o programa identificou as palavras “ainda”, “mal” e “primeiro” “que” e “para” como
#         marcadores discursivos fáceis) e calculou 6/5.
#
#         **Status**: incorreto
#
#     """
#
#     name = '''Ratio of Easy Discourse Markers to All Clauses'''
#     column_name = 'discourse_markers_easy'
#
#     def value_for_text(self, t, rp=default_rp):
#         lower = rp.all_words(t)
#         ocorrencias = sum(
#             [
#                 lower.count('e'),
#                 lower.count('se'),
#                 lower.count('que'),
#                 lower.count('ou'),
#                 lower.count('para'),
#                 lower.count('como'),
#                 lower.count('ora'),
#                 lower.count('mas'),
#                 lower.count('tão'),
#                 lower.count('também'),
#                 lower.count('tal'),
#                 lower.count('antes'),
#                 lower.count('quando'),
#                 lower.count('ainda'),
#                 lower.count('mal'),
#                 lower.count('porque'),
#                 lower.count('nem'),
#                 lower.count('tanto'),
#                 lower.count('primeiro')
#             ]
#         )
#         ngram = list(ngrams(lower, 2))
#         ocorrencias += sum(
#             [
#                 ngram.count(('por', 'exemplo'))
#             ]
#         )
#         try:
#             return ocorrencias / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class DiscourseMarkersMedium(base.Metric):
#     """
#         **Nome da Métrica**: discourse_markers_medium
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual.
#
#         **Descrição da métrica**: Proporção de marcadores discursivos medianos em relação à quantidade de orações do
#         texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: Quantidade de orações é um número obtido por meio
#         da contagem das etiquetas “V” menos as etiquetas <aux> do parser Palavras ou seja, cada verbo principal
#         representa uma oração. Marcadores discursivos medianos são os seguintes (informados diretamente no código de
#         extração da métrica): logo, caso, assim, então, após, porém, enquanto, ou seja, por isso, para que, antes de,
#         já que, quer dizer;
#
#         **Forma de cálculo da métrica**: contam-se os marcadores discursivos medianos, usando a lista do próprio código
#         para identificá-los; divide-se o resultado pela quantidade de orações do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras para contar as orações
#
#         **Limitações da métrica**:  não prevê a ambiguidade funcional das palavras
#
#         **Crítica**: vários motivos tornam recomendável inibir (comentar) esta métrica:
#
#             1) a origem da lista de marcadores discursivos não está descrita;
#
#             2) a lista de marcadores discursivos contém palavras que não são marcadores discursivos ou que podem ter
#             outras funções além de marcador discursivo;
#
#             3) marcas para desambiguização de marcadores discursivos, como a vírgula, não são usadas;
#
#             4) os critérios para dividir os marcadores discursivos em 4 níveis não estão explícitos;
#
#             5) palavras ambíguas funcionalmente deveriam ser suprimidas do léxico de marcadores;
#
#             6) a proporção deveria ser em relação ao total de marcadores discursivos.
#
#         **Projeto**: GUTEN
#
#         **Teste**: O caso é sério e é preciso operar logo após o meio-dia, assim que o médico chegar.
#
#         **Contagens**: 4 orações, 1 marcador discursivo fácil (e), nenhum mediano
#
#         **Resultado Esperado**: zero
#
#         **Resultado Obtido**: 1 (o programa identificou “caso”, “logo”, “após”, “assim” como marcadores discursivos,
#         mas essas palavras não têm essa função nessa sentença)
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Medium Discourse Markers to All Clauses'
#     column_name = 'discourse_markers_medium'
#
#     def value_for_text(self, t, rp=default_rp):
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('logo'),
#                 lower.count('caso'),
#                 lower.count('assim'),
#                 lower.count('então'),
#                 lower.count('após'),
#                 lower.count('porém'),
#                 lower.count('enquanto')
#             ]
#         )
#         ngram = list(ngrams(lower, 2))
#         ocorrencias += sum(
#             [
#                 ngram.count(('ou', 'seja')),
#                 ngram.count(('por', 'isso')),
#                 ngram.count(('para', 'que')),
#                 ngram.count(('antes', 'de')),
#                 ngram.count(('já', 'que')),
#                 ngram.count(('quer', 'dizer'))
#             ]
#         )
#         try:
#             return ocorrencias / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class DiscourseMarkersHard(base.Metric):
#     """
#         **Nome da Métrica**: discourse_markers_hard
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual.
#
#         **Descrição da métrica**: Proporção de marcadores discursivos de difíceis em relação à quantidade de orações do
#         texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: quantidade de orações é um número obtido por meio
#         da contagem das etiquetas “V” menos as etiquetas <aux> do parser Palavras ou seja, cada verbo principal
#         representa uma oração. Marcadores discursivos difíceis são os seguintes (informados diretamente no código de
#         extração da métrica): primeiramente, a ilustrar, por esse motivo, como vimos, de tal forma, efetivamente, na
#         realidade, em consequência, tampouco, por um lado, em segundo lugar, a não ser que, por último, embora, mas
#         também, até que, na verdade, assim como, acima, daí, portanto, no entanto, não só, apesar de, mesmo que, em
#         seguida, ao mesmo tempo, isto é, de fato, a seguir, assim que, mais tarde, em relação ao, bem como, depois que,
#         naturalmente, ainda que, desde que, de modo, certamente, sobretudo, com isso, uma vez que, mesmo assim, ou
#         melhor, repare-se, a fim de, igualmente, menos do que, entretanto, para começar, de forma a, contudo, com o
#         objetivo de, ainda assim, por outro lado, dado que, mais ainda, além disso, tal como, para concluir, logo que,
#         pelo contrário, é o caso de, em primeiro lugar.
#
#         **Forma de cálculo da métrica**: contam-se os marcadores discursivos difíceis, usando a lista do próprio código
#         para identificá-los; divide-se o resultado pela quantidade de orações do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras para contar as orações
#
#         **Limitações da métrica**:  não prevê a ambiguidade funcional das palavras
#
#         **Crítica**: vários motivos tornam recomendável inibir (comentar) esta métrica
#
#             1) a origem da lista de marcadores discursivos não está descrita
#
#             2) a lista de marcadores discursivos contém palavras que não são marcadores discursivos ou que podem ter
#             outras funções além de marcador discursivo
#
#             3) marcas para desambiguização de marcadores discursivos, como a vírgula, não são usadas,
#
#             4) os critérios para dividir os marcadores discursivos em 4 níveis não estão explícitos
#
#             5) marcadores discursivos muito ambíguos e sem marcas de desambiguização deveriam ser suprimidos;
#
#             6) a proporção deveria ser em relação ao total de marcadores discursivos e não por número de orações.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Vamos embora tão logo tenhamos resolvido essas pendências, apesar de estarmos adorando a estadia no
#         hotel.
#
#         **Contagens**: 3 orações e 1 marcador discursivo (apesar de)
#
#         **Resultado Esperado**: 1/3 = 0,33
#
#         **Resultado Obtido**: 0,667 (a palavra “embora” foi indevidamente reconhecida como marcador discursivo)
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Hard Discourse Markers to All Clauses'
#     column_name = 'discourse_markers_hard'
#
#     def value_for_text(self, t, rp=default_rp):
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('embora'),
#                 lower.count('mas também'),
#                 lower.count('até que'),
#                 lower.count('na verdade'),
#                 lower.count('assim como'),
#                 lower.count('acima'),
#                 lower.count('daí'),
#                 lower.count('portanto'),
#                 lower.count('no entanto'),
#                 lower.count('não só'),
#                 lower.count('apesar de'),
#                 lower.count('mesmo que'),
#                 lower.count('em seguida'),
#                 lower.count('ao mesmo tempo'),
#                 lower.count('isto é'),
#                 lower.count('de fato'),
#                 lower.count('a seguir'),
#                 lower.count('assim que'),
#                 lower.count('mais tarde'),
#                 lower.count('em relação ao'),
#                 lower.count('bem como'),
#                 lower.count('depois que'),
#                 lower.count('naturalmente'),
#                 lower.count('ainda que'),
#                 lower.count('desde que'),
#                 lower.count('desde que'),
#                 lower.count('de modo'),
#                 lower.count('certamente'),
#                 lower.count('sobretudo'),
#                 lower.count('com isso'),
#                 lower.count('uma vez que'),
#                 lower.count('mesmo assim'),
#                 lower.count('ou melhor'),
#                 lower.count('repare-se'),
#                 lower.count('a fim de'),
#                 lower.count('igualmente'),
#                 lower.count('menos do que'),
#                 lower.count('entretanto'),
#                 lower.count('para começar'),
#                 lower.count('de forma a'),
#                 lower.count('contudo'),
#                 lower.count('com o objetivo de'),
#                 lower.count('ainda assim'),
#                 lower.count('por outro lado'),
#                 lower.count('dado que'),
#                 lower.count('mais ainda'),
#                 lower.count('além disso'),
#                 lower.count('tal como'),
#                 lower.count('para concluir'),
#                 lower.count('pelo contrário'),
#                 lower.count('logo que'),
#                 lower.count('é o caso de'),
#                 lower.count('em primeiro lugar'),
#                 lower.count('por último'),
#                 lower.count('a não ser que'),
#                 lower.count('em segundo lugar'),
#                 lower.count('por um lado'),
#                 lower.count('tampouco'),
#                 lower.count('em consequência'),
#                 lower.count('na realidade'),
#                 lower.count('efetivamente'),
#                 lower.count('de tal forma'),
#                 lower.count('como vimos'),
#                 lower.count('por esse motivo'),
#                 lower.count('a ilustrar'),
#                 lower.count('primeiramente')
#             ]
#         )
#         try:
#             return ocorrencias / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class DiscourseMarkersVeryHard(base.Metric):
#     """
#         **Nome da Métrica**: discourse_markers_veryhard
#
#         **Interpretação**: quanto maior a proporção, maior a complexidade
#
#         **Descrição da métrica**: Proporção de marcadores discursivos muito difíceis em relação à quantidade de orações
#         do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: quantidade de orações é um número obtido por meio
#         da contagem das etiquetas “V” menos as etiquetas <aux> do parser Palavras ou seja, cada verbo principal
#         representa uma oração. Marcadores discursivos muito difíceis são os seguintes (informados diretamente no código
#         de extração da métrica): com efeito, daí que, em terceiro lugar, concluindo, paralelamente, ou antes, nesse
#         contexto, em contrapartida, visto que, como se pode ver, seguidamente, em resumo, por ora, pretendemos,
#         evidentemente, é evidente que, contanto que, além de tudo, com o propósito de, por conseguinte, prosseguindo,
#         em alternativa, documentando, a fim de que, para encerrar, por este motivo, note-se que, com intuito de, nesse
#         cenário, todavia, mais concretamente, contrariamente, pelo que referi anteriormente, em nosso entender, dizendo
#         melhor, opcionalmente, concomitantemente, com toda a certeza, conquanto, significa isto que, quer isto dizer,
#         decerto, recapitulando, exemplificando, não se pense que, em vias de, por outras palavras, estou em crer que,
#         sintetizando, não obstante, em conclusão, a meu ver, com vistas a, alternativamente, deste modo, malgrado, com
#         isto, veja-se, em suma.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras para contar as orações
#
#         **Limitações da métrica**:  não prevê a ambiguidade funcional das palavras
#
#         **Crítica**: é recomendável comentar esta métrica por uma série de motivos:
#
#             1) a origem da lista de marcadores discursivos não está descrita
#
#             2) a lista de marcadores discursivos contém palavras e sequências de palavras que não são marcadores
#             discursivos ou que podem ter outras funções além de marcador discursivo
#
#             3) marcas para desambiguização de marcadores discursivos, como a vírgula, não são usadas,
#
#             4) os critérios para dividir os marcadores discursivos em 4 níveis não estão explícitos;
#
#             5) palavras ambíguas funcionalmente deveriam ser suprimidas do léxico de marcadores.
#
#         **Projeto**: GUTEN
#
#         **Teste**: É importante esclarecer o assunto para que não se pense que somos contrários à greve.
#
#         **Contagens**: nenhum marcador discursivo, 4 orações
#
#         **Resultado Esperado**: 0
#
#         **Resultado Obtido**: 0,25 (o extrator localizou “não se pense que” e contou como marcador)
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Very Hard Discourse Markers to All Clauses'
#     column_name = 'discourse_markers_veryhard'
#
#     def value_for_text(self, t, rp=default_rp):
#         lower = t.raw_content.lower()
#         ocorrencias = sum(
#             [
#                 lower.count('com efeito'),
#                 lower.count('daí que'),
#                 lower.count('em terceiro lugar'),
#                 lower.count('concluindo'),
#                 lower.count('paralelamente'),
#                 lower.count('ou antes'),
#                 lower.count('nesse contexto'),
#                 lower.count('em contrapartida'),
#                 lower.count('visto que'),
#                 lower.count('como se pode ver'),
#                 lower.count('seguidamente'),
#                 lower.count('em resumo'),
#                 lower.count('por ora'),
#                 lower.count('pretendemos'),
#                 lower.count('evidentemente'),
#                 lower.count('é evidente que'),
#                 lower.count('contanto que'),
#                 lower.count('além de tudo'),
#                 lower.count('com o propósito de'),
#                 lower.count('por conseguinte'),
#                 lower.count('prosseguindo'),
#                 lower.count('em alternativa'),
#                 lower.count('documentando'),
#                 lower.count('a fim de que'),
#                 lower.count('para encerrar'),
#                 lower.count('por este motivo'),
#                 lower.count('note-se que'),
#                 lower.count('com intuito de'),
#                 lower.count('nesse cenário'),
#                 lower.count('todavia'),
#                 lower.count('mais concretamente'),
#                 lower.count('contrariamente'),
#                 lower.count('pelo que referi anteriormente'),
#                 lower.count('em nosso entender'),
#                 lower.count('dizendo melhor'),
#                 lower.count('opcionalmente'),
#                 lower.count('concomitantemente'),
#                 lower.count('com toda a certeza'),
#                 lower.count('conquanto'),
#                 lower.count('significa isto que'),
#                 lower.count('quer isto dizer'),
#                 lower.count('decerto'),
#                 lower.count('recapitulando'),
#                 lower.count('exemplificando'),
#                 lower.count('não se pense que'),
#                 lower.count('em vias de'),
#                 lower.count('por outras palavras'),
#                 lower.count('estou em crer que'),
#                 lower.count('sintetizando'),
#                 lower.count('não obstante'),
#                 lower.count('em conclusão'),
#                 lower.count('a meu ver'),
#                 lower.count('com vistas a'),
#                 lower.count('alternativamente'),
#                 lower.count('deste modo'),
#                 lower.count('malgrado'),
#                 lower.count('com isto'),
#                 lower.count('veja-se'),
#                 lower.count('em suma')
#             ]
#         )
#         try:
#             return ocorrencias / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


class TalkToReader(base.Metric):
    """
        **Nome da Métrica**: dialog_pronoun_ratio

        **Interpretação**: textos que estabelecem diálogo com o leitor têm menor complexidade, portanto, quanto maior o
        resultado, menor a complexidade.

        **Descrição da métrica**: proporção de pronomes pessoais que indicam uma conversa com o leitor em relação ao
        total de pronomes pessoais presentes no texto.

        **Definição dos termos que aparecem na descrição da métrica**: pronomes pessoais que indicam uma conversa com o
        leitor são: "eu", "tu", "você" e "vocês".

        **Forma de cálculo da métrica**: contam-se as ocorrências de "eu", "tu", "você" e "vocês" e divide-se o
        resultado pelo total de pronomes pessoais do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger do nlpnet

        **Limitações da métrica**:

        **Crítica**: a rigor, a métrica deveria computar primeiras e segundas pessoas: eu, tu, você, a gente, vocês,
        nós e vós. Está faltando computar “a gente” e “vós”.

        **Projeto**: GUTEN

        **Teste**: Você acredita que já chegou o final do ano? O tempo voou e a gente já começa a ver o Papai Noel nos
        outdoors e nas vitrines. Mas eu acho que o comércio está se antecipando demais e deveria esperar dezembro para
        começar as propagandas de Natal.

        **Contagens**: 3 pronomes pessoais que indicam diálogo com o leitor (você, a gente, eu)

        **Resultado Esperado**: 3/3 = 1,00

        **Resultado Obtido**: 1,00 (2/2) (como não reconhece “a gente”, não computa no numerador nem no denominador

        **Status**: correto
    """

    name = 'Pronouns that Delimits a Talk to Reader'
    column_name = 'dialog_pronoun_ratio'

    def value_for_text(self, t, rp=default_rp):
        words = rp.lower_words(t)
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


class NotSVO(base.Metric):
    """
        **Nome da Métrica**: non_svo_ratio

        **Interpretação**: quanto maior o resultado da métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de orações que não estão no formato SVO (sujeito-verbo-objeto) em relação a
        todas orações do texto

        **Definição dos termos que aparecem na descrição da métrica**: a ordem SVO é a ordem canônica ou “natural” dos
        constituintes na língua portuguesa (ex: Ela adotou um menino). Ordens não SVO são: OSV (ex: Greve eu não farei),
        OVS (ex: dinheiro só ganharão os bons profissionais), VS (ex: Acabou o prazo), VSO (ex: Ouviram do Ipiranga as
        margens plácidas, de um povo heroico o brado retumbante), VOS (ex: Fez vinte e oito pontos a melhor aluna).

        **Forma de cálculo da métrica**:

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Ouviram as margens plácidas o brado retumbante. Acabou o prazo de análise, mas nós ainda podemos
        pedir prorrogação.

        **Contagens**: 3 orações (ouviram..., acabou..., podemos pedir...), a primeira na ordem VSO, a segunda na ordem
        VS e a terceira na ordem SVO, portanto, 2 orações em ordens não SVO.

        **Resultado Esperado**: 2/3 = 0,667

        **Resultado Obtido**: 0,667

        **Status**: correto
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
            return count / nverbs
        except ZeroDivisionError:
            return 0


# class DiscourseVoices(base.Metric):
#     """
#         **Nome da Métrica**: discourse_voices_ratio
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de palavras que introduzem vozes no discurso em relação à quantidade de
#         palavras do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: de acordo com a concepção da métrica, palavras
#         que introduzem vozes no discurso são: “de=acordo”, “segundo”, “diz que”, “disse que”, “disseram”, “afirma”,
#         “afirmam”
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das sequências lexicais definidas como introdutoras
#         de vozes no discurso e divide-se pelo total de palavras do texto
#
#         **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet
#
#         **Limitações da métrica**: por ser baseada em léxico, tem muita ambiguidade e pode ser falsamente inflada
#
#         **Crítica**: o que é definido como “vozes do discurso” são formas de introduzir discurso indireto. A lista de
#         verbos de elocução é muito limitada. É preciso estudo para aumentar o léxico e para diminuir os riscos de
#         capturar as mesmas palavras com outras funções além dessa.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Foi segundo colocado na competição e afirma nunca ter usado esteroides.
#
#         **Contagens**: 11 palavras, 1 voz no discurso
#
#         **Resultado Esperado**: 1/11 = 0,09
#
#         **Resultado Obtido**: 0,25
#
#         **Status**: incorreto
#
#     """
#
#     name = 'Ratio of Discourse Voices to all Words'
#     column_name = 'discourse_voices_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         lower = t.raw_content.lower()
#         flat = rp.palavras_flat(t)
#         lines = flat.split('\n')
#         ocorrencias = 0
#         words = 0
#         expression = re.compile('''
#                                 de=acordo|
#                                 afirma|
#                                 \[segundo\]\ <com>
#                                 ''',
#                                 re.VERBOSE)
#         for line in lines:
#             if len(line) > 10:
#                 words += 1
#                 ocorrencias += len(re.findall(expression, line))
#         ocorrencias2 = sum(
#             [
#                 lower.count('diz que'),
#                 lower.count('disse que'),
#                 lower.count('disseram'),
#                 lower.count('afirma'),
#                 lower.count('afirmam'),
#
#             ]
#         )
#         try:
#             return (ocorrencias + ocorrencias2) / words
#         except ZeroDivisionError:
#             return 0


class TopicalizedClausesRatio(base.Metric):
    """
        **Nome da Métrica**: adverbs_before_main_verb_ratio

        **Interpretação**: quanto maior o resultado da métrica (o máximo é 1), maior a complexidade textual, pois
        representa carga de trabalho de leitura, ou seja, aquilo que se acumula na memória antes da chegada do verbo
        principal.

        **Descrição da métrica**: Proporção de orações com advérbio antes do verbo principal em relação à quantidade de
        orações do texto

        **Definição dos termos que aparecem na descrição da métrica**: advérbios antes de verbos principais são
        ocorrências que rompem a ordem canônica dos constituintes das sentenças (Sujeito, Verbo, Objeto, Advérbio).

        **Forma de cálculo da métrica**: verificam-se quantas orações possuem ocorrências de adjuntos adverbiais
        antepostos aos verbos (@ADVL>), não importando a quantidade de advérbios antepostos. Divide-se o resultado do
        contador pela quantidade de orações do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Gradativamente, ele foi se acostumando às novas condições de trabalho, porém, praticamente não se
        conformou até hoje com a perda de status. Hoje é fácil perceber isso, no entanto, naquela época, dificilmente
        alguém poderia saber que ele estava sofrendo profundamente.

        **Contagens**: 6 orações, 4 com advérbios antes dos verbos principais

        **Resultado Esperado**: 4/6 = 0,667

        **Resultado Obtido**: 0,667

        **Status**: correto

    """

    name = 'Ratio of Adverbs Before Main Verb'
    column_name = 'adverbs_before_main_verb_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        lines = flat.split('\n')
        count = 0
        advl = False
        for line in lines:
            if '@ADVL>' in line and not advl:
                advl = True
                count += 1
            if ' V ' in line and '<aux>' not in line:
                advl = False
        nverbs = flat.count(' V ') - flat.count('<aux>')
        try:
            return count / nverbs
        except ZeroDivisionError:
            return 0


# class AdverbsBeforeMainVerb(base.Metric):
#     """
#         **Nome da Métrica**: adverbs_before_main_verb
#
#         **Interpretação**: quanto maior o resultado da métrica, maior a complexidade textual
#
#         **Descrição da métrica**: Proporção entre a quantidade de advérbios antes de verbos principais e a quantidade
#         de verbos do texto.
#
#         **Definição dos termos que aparecem na descrição da métrica**: advérbios antes de verbos principais são
#         ocorrências que rompem a ordem canônica dos constituintes das sentenças (Sujeito, Verbo, Objeto, Advérbio).
#
#         **Forma de cálculo da métrica**: verificam-se as ocorrências de adjuntos adverbiais antepostos ao verbo (@ADVL>).
#          Somam-se todas as ocorrências e divide-se o resultado pela quantidade de orações do texto (V – aux).
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**: o parser Palavras anota conjunções adversativas como advérbios antepostos ao verbo, o
#         que pode levar a uma superestimativa da métrica.
#
#         **Crítica**: Esta métrica é muito semelhante à adverbs_before_main_verb_ratio e pode ser comentada para não
#         gerar redundância.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Gradativamente, ele foi se acostumando às novas condições de trabalho, porém, praticamente não se
#         conformou até hoje com a perda de status. Hoje é fácil perceber isso, no entanto, naquela época, dificilmente
#         alguém poderia saber que ele estava sofrendo profundamente.
#
#         **Contagens**: 6 orações, 6 advérbios antes dos verbos principais (gradativamente, praticamente, não, hoje,
#         naquela época, dificilmente)
#
#         **Resultado Esperado**: 6/6 = 0,667
#
#         **Resultado Obtido**: 0,1,333 (8/6, pois o parser anotou as conjunções adversativas “porém” e “no entanto”
#         com a etiqueta @ADVL)
#
#         **Status**: correto, considerando a limitação do parser
#     """
#
#     name = 'Adverbs Before Main Verb'
#     column_name = 'adverbs_before_main_verb'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         adverbs = re.findall('@ADVL>', flat)    # advérbios antes do verbo
#         nverbs = flat.count(' V ') - flat.count('<aux>')
#         try:
#             return len(adverbs) / nverbs
#         except ZeroDivisionError:
#             return 0
#

class PostponedSubject(base.Metric):
    """
        **Nome da Métrica**: postponed_subject_ratio

        **Interpretação**: sujeito posposto (VS) é uma ordem de constituintes mais complexa que sujeito anteposto (SV)

        **Descrição da métrica**: Proporção de sujeitos pospostos em relação a todos os sujeitos do texto

        **Definição dos termos que aparecem na descrição da métrica**: sujeito posposto é o sujeito que ocorre após o
        verbo.

        **Forma de cálculo da métrica**: contam-se todas as etiquetas <SUBJ (sujeito após verbo principal) do texto e
        divide-se o resultado pela soma de todas as etiquetas SUBJ (sujeitos) do texto

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: São tomadas muitas iniciativas a fim de melhorar a situação da educação no Brasil, porém são poucas
        as que dão resultado.

        **Contagens**: 4 orações (são tomadas, melhorar, são, dão), 3 sujeitos (muitas iniciativas, as que dão
        resultado, que) 2 sujeitos pospostos

        **Resultado Esperado**: 2/3 = 0,667

        **Resultado Obtido**: 0,667

        **Status**: correto
    """

    name = 'Postponed Subject Ratio'
    column_name = 'postponed_subject_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        pospostos = re.findall('<SUBJ', flat)
        sujeitos = re.findall('SUBJ', flat)
        try:
            return len(pospostos) / len(sujeitos)
        except ZeroDivisionError:
            return 0


class ObliquePronounsRatio(base.Metric):
    """
        **Nome da Métrica**: oblique_pronouns_ratio

        **Interpretação**: pronomes oblíquos estão associados a uma maior complexidade textual

        **Descrição da métrica**: Proporção de pronomes oblíquos em relação a todos os pronomes do texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes oblíquos são aqueles usados
        prioritariamente como objetos diretos ou indiretos (o, a, os, as, lo, la, los, las, no, na, nos, nas, lhe,
        lhes, me, mim, te, ti, se, si, ele, ela, eles, elas, nós, vós, conosco, convosco, comigo, contigo, consigo).
        Os pronomes oblíquos precedidos da preposição “com”, contraídos (comigo, contigo, etc.) ou não contraídos (com
        ele, com eles, etc.) podem ser também adjuntos adverbiais de companhia (ex: viajar conosco, viajar com eles).
        Os pronomes oblíquos precedidos de preposição podem ser complemento nominal (ex: saudade de mim). A ambiguidade
        funcional das formas: ele, ela, eles, elas, nós e vós é resolvida pela etiqueta PROPESS, pois os pronomes
        pessoais do caso reto têm etiqueta específica (PROSUB). A ambiguidade funcional das formas o, a, os, as também
        é tratada (elas podem ser artigos – ART e, no caso de “a”, até preposição – PREP). O “se” (que pode ser
        conjunção – KC ou KS) também é desambiguizado, porém as funções do “se” pronome (índice de apassivação, de
        indeterminação do sujeito, recíproco, reflexivo) não são discriminadas.

        **Forma de cálculo da métrica**: contam-se todas as ocorrências de pronomes que estejam na lista de pronomes
        oblíquos e tenham a etiqueta “PROPESS”.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: A etiqueta “PROPESS” não pega as formas contraídas dos pronomes oblíquos, mesmo que
        essas formas estejam no léxico da métrica. As formas contraídas dos pronomes oblíquos são: dele, dela, deles,
        delas, nele, nela, neles, nelas, comigo, contigo, consigo, conosco, convosco. Para capturar as formas contraídas
        seria necessário usar o léxico e a etiqueta PREP+PROPESS.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Ele não queria os créditos só para si: queria nos reconhecer como colaboradores valiosos. Nós ficamos
        motivados com a atitude que ele teve conosco. Ao que tudo indica, ele se preocupa conosco.

        **Contagens**: 10 pronomes (ele, si, nos, nós, ele, conosco, tudo, ele, se, conosco), 1 do caso oblíquo (nos),
        sem considerar o “conosco”, que tagger não reconhece.

        **Resultado Esperado**: 1/10 = 0,10

        **Resultado Obtido**: 0,10

        **Status**: correto
    """

    name = 'Ratio of Oblique Pronouns to All Pronouns'
    column_name = 'oblique_pronouns_ratio'

    def value_for_text(self, t, rp=default_rp):

        ends = ['-me', '-te', '-o', '-no', '-lo', '-a', '-na', '-la', '-nos',
                '-vos', '-os', '-nos', '-los', '-as', '-nas', '-las', '-lhe',
                '-lhes']
        atonos = ['me', 'te', 'o', 'a', 'nos', 'vos',
                        'os', 'as', 'lhe', 'lhes']
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        tagged = rp.tagged_words(t)
        occurances = 0
        for i in range(len(tagged) - 1):
            # VERBO + "-me, -te, -o, -a, -na, -no, -la, -lo, -nos, -vos, -os, -nas, -nos, -las, -los, -as, -lhe, -lhes"
            if True in [tagged[i][0].endswith(e) for e in ends]:
                occurances += 1
            # "me, te, o, a, nos, vos, os, as, lhe, lhes" + VERBO FLEXIONADO
            elif tagged[i][0] in atonos:
                if tagged[i+1][1] == 'V' and not tagged[i+1][0].endswith('r'):
                    occurances += 1
            # PREP + "ela, ele, nós, vós, eles, elas"
            elif tagged[i][1] == 'PREP' and tagged[i+1][1] == 'PROPESS':
                occurances += 1
        try:
            return occurances / ilen(pronouns)
        except ZeroDivisionError:
            return 0


class TemporalAdjunctRatio(base.Metric):
    """
        **Nome da Métrica**: temporal_adjunct_ratio

        **Interpretação**: não está clara a relação entre a métrica e a complexidade

        **Descrição da métrica**: Proporção de adjuntos adverbiais de tempo em relação a todos os adjuntos adverbiais
        do texto

        **Definição dos termos que aparecem na descrição da métrica**: adjuntos adverbiais de tempo são palavras ou
        expressões que informam quando a ação do verbo aconteceu (ex: ontem, de vez em quando, frequentemente, no dia
        18 de novembro, etc.). Para identificá-las, utilizam-se as expressões regulares criadas por Baptista
        et. Al. (2008).

        **Forma de cálculo da métrica**: identificam-se todos os adjuntos adverbiais (etiqueta ADVL do nlpnet).
        Filtram-se os adjuntos adverbiais de tempo, utilizando o léxico e as expressões regulares do
        rp.temporal_expressions. Divide-se a quantidade de adjuntos adverbiais de tempo pela quantidade total de
        adjuntos adverbiais.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger nlpnet.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Foi durante meus experimentos que eu me machuquei. Certamente cometi um erro.

        **Contagens**: 2 adjuntos adverbiais, um dos quais é de tempo (durante meus experimentos)

        **Resultado Esperado**: 1/2 = 0,50

        **Resultado Obtido**: 0,50

        **Status**: correto
    """

    name = 'Ratio of Temporal Adjuncts to All Adjuncts'
    column_name = 'temporal_adjunct_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        adjuncts = re.findall('ADVL', flat)
        temporals = rp.temporal_expressions(t)
        try:
            return len(temporals) / len(adjuncts)
        except ZeroDivisionError:
            return 0


class AdjacentDemonstrativePronounAnaphoricReferences(AnaphoricReferencesBase):
    """
        **Nome da Métrica**: demonstrative_pronoun_ratio

        **Interpretação**: quanto mais candidatos a referentes houver para resolver a referência anafórica, maior é a
        complexidade textual

        **Descrição da métrica**: Média de candidatos a referente, na sentença anterior, por pronome demonstrativo
        anafórico

        **Definição dos termos que aparecem na descrição da métrica**: referência anafórica é a relação entre um pronome
        e o termo anterior que ele substitui. O pronome é a anáfora e o nome que ele substitui é o referente. Por
        exemplo, quando digo “Gosto desse livro”, podem me perguntar: “Desse qual?” A resposta é o referente do pronome
        anafórico “desse”: “Comprei a obra “Sapiens”, que é um best seller desde que foi lançado. Gosto desse livro.”
        Leitores proficientes sabem que “desse” = “a obra ‘Sapiens’”. Na sentença anterior, contudo, há três
        substantivos candidatos a referente do pronome “desse”: “obra”, “Sapiens’” e “best seller”. Decidir entre os
        candidatos pode ser uma tarefa difícil para um leitor menos proficiente e por isso a quantidade de candidatos
        por pronome anafórico é uma medida de complexidade textual.

        **Forma de cálculo da métrica**: localizam-se todos os pronomes demonstrativos nas sentenças, usando uma lista
        desses pronomes com seus respectivos número (singular ou plural) e gênero (feminino ou masculino). Na sentença
        anterior a cada pronome demonstrativo, procuram-se substantivos que tenham, no léxico DELAF, o mesmo número e
        gênero do pronome demonstrativo, ou seja, que sejam candidatos a referência anafórica desses pronomes. Contam-se
        os candidatos por pronome demonstrativo e depois calcula-se a média de candidatos por pronome demonstrativo.

        **Recursos de PLN utilizados durante o cálculo**: DELAF

        **Limitações da métrica**: se os candidatos a referente não estiverem no léxico DELAF ou se não tiverem o mesmo
        número e grau do pronome demonstrativo, eles não serão reconhecidos, como é visto no primeiro teste.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste 1**: Comprei a obra “Sapiens”, que é um best-seller desde que foi lançado. Gosto desse livro.

        **Contagens**: 1 pronome demonstrativo (desse) e 3 candidatos a referentes na sentença anterior (obra, Sapiens,
         best-seller)

        **Resultado Esperado**: 3/1 = 3

        **Resultado Obtido**: 0 (“desse” é masculino singular e “obra” é feminino singular; “Sapiens” e “best seller”
        não estão no léxico do DELAF)

        **Status**: correto, dentro das limitações da métrica

        **Teste 2**: Ouvi dizer que estão tentando incluir orientação nutricional no currículo escolar. Sou totalmente
        defensor dessa proposta.

        **Contagens**: 1 pronome demonstrativo (dessa) e 1 candidato a referentes na sentença anterior (orientação)

        **Resultado Esperado**: 1/1 = 1

        **Resultado Obtido**: 1

        **Status**: correto
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


class RelativePronouns(base.Metric):
    """
        **Nome da Métrica**: relative_pronouns_ratio

        **Interpretação**: pronomes relativos introduzem orações subordinadas adjetivas, substantivas e adverbiais, que
        expandem o conteúdo de um sintagma nominal e aumentam a complexidade textual

        **Descrição da métrica**: Proporção de Pronomes Relativos em relação à quantidade de pronomes do texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes relativos retomam e qualificam um nome
        que os antecedem. Suas formas são: que, o que, o qual, os quais, a qual, as quais, cujo, cujos, cuja, cujas,
        quem, quando, onde, como, quanto, quantos, quanta, quantas. Muitos deles são ambíguos funcionalmente (podem
        atuar como outro tipo de pronome), por isso a etiqueta <rel> é importante para capturar apenas aqueles com
        função relativa.

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta <rel> e divide-se o resultado pela
        soma de todas as ocorrências de pronomes do texto.

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        embora a classe de pronomes seja imediatamente superior à  de pronomes relativos, a métrica poderia ser um
        índice melhor se fosse calculada por sintagma nominal.

        O POS tagger usado não reconhece multipalavras, como “o=que”, por exemplo. Isso faz com que a métrica possa ser
        superestimada em alguns casos, mas não é um problema grave.

        **Projeto**: GUTEN

        **Teste**: Regressando de São Paulo, visitei o sítio de minha tia, o qual me deixou encantado. Era exatamente o
        que eu esperava, apesar de nunca ter imaginado que eu estaria ali.

        **Contagens**: 7 pronomes (minha, o qual, me, o que, eu, que, eu), 9 contados pelo POS tagger nlpnet, dos quais
        2 são pronomes relativos (o qual, o que)

        **Resultado Esperado**: 2/7 = 0,285 ou 2/9 (o sistema identifica dois pronomes em “o que” e em “o qual”

        **Resultado Obtido**: 0,222

        **Status**: correto

    """

    name = 'Ratio of Relative Pronouns to all Pronouns'
    column_name = 'relative_pronouns_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        casos = re.findall('\[.*\].*<rel>', flat)
        if casos:
            relativos = [re.search('\[(.*)\].*<rel>', i).group(1) for i in casos]
            pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
            try:
                return len(relativos) / len(list(pronouns))
            except ZeroDivisionError:
                return 0
        else:
            return 0


class RelativePronounsDiversity(base.Metric):
    """
        **Nome da Métrica**: relative_pronouns_diversity_ratio

        **Interpretação**: pronomes relativos introduzem orações subordinadas adjetivas, substantivas e adverbiais, que
        expandem o conteúdo de um sintagma nominal e aumentam a complexidade textual. Sua forma mais simples é o “que”.
        Se houver uso de outros pronomes relativos, a complexidade textual aumenta.

        **Descrição da métrica**: Proporção de types de pronomes relativos  em relação à quantidade de tokens de
        pronomes relativos no texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes relativos retomam e qualificam um nome
        que os antecedem. Suas formas são: que, o que, o qual, os quais, a qual, as quais, cujo, cujos, cuja, cujas,
        quem, quando, onde, como, quanto, quantos, quanta, quantas. Muitos deles são ambíguos funcionalmente (podem
        atuar como outro tipo de pronome), por isso a etiqueta <rel> é importante para capturar apenas aqueles com
        função relativa.

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta <rel>, sem considerar repetições;
        divide-se o resultado pela soma de todas as ocorrências da etiqueta <rel> do texto, considerando as repetições.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: A escola na qual estudo é muito rigorosa, mas os professores que dão aula para mim são muito bons. A
        professora de gramática, a qual dá aula para mim desde o sexto ano, tem uma didática fantástica.

        **Contagens**: 3 pronomes relativos ((em) a qual, que, a qual ), dos quais 2 sem considerar repetições.

        **Resultado Esperado**: 2/3 = 0,667

        **Resultado Obtido**: 0,667

        **Status**: correto
    """

    name = 'Relative Pronouns Diversity'
    column_name = 'relative_pronouns_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        casos = re.findall('\[.*\].*<rel>', flat)
        if casos:
            relativos = [re.search('\[(.*)\].*<rel>', i).group(1) for i in casos]
            # unique = len(set(relativos))
            try:
                return rp.mattr(relativos)
                # return unique / len(relativos)
            except ZeroDivisionError:
                return 0
        else:
            return 0


class ShortSentencesRate(base.Metric):
    """
        **Nome da Métrica**: short_sentence_ratio

        **Interpretação**: quanto maior a proporção de sentenças curtas, menos complexo é o texto

        **Descrição da métrica**: Proporção de Sentenças Curtas em relação a todas as sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: há 4 tamanhos de sentença: curto, médio, longo e
        muito longo. Os números de quantidade de palavras que separam os quatro tipos de sentenças são 11, 763 - 13,027
        e 15,908. Na prática, isso significa que sentenças curtas têm 11 palavras ou menos; sentenças médias têm 12 ou
        13 palavras; sentenças longas têm 14 ou 15 palavras e sentenças muito longas têm mais de 15 palavras.

        **Forma de cálculo da métrica**: Calcula-se a quantidade de palavras por sentença. Contam-se as sentenças 11
        palavras ou menos e divide-se o resultado pelo total de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador

        **Limitações da métrica**:

        **Crítica**: Não há como uma sentença ter número quebrado de palavras, então uma sentença curta é aquela que
        tem 11 palavras ou menos (ao invés de 11,763). O artifício de usar os números quebrados 11, 763 - 13,027 e
        15,908 para separar os quatro intervalos só se justifica como forma de evitar ter que lidar com operações
        lógicas de “maior que” e “menor ou igual a”. Mas para isso as quantidades de palavras que delimitam os quatro
        intervalos de sentenças poderiam ser 11,001 - 13,001 e 15,001.

        Os intervalos entre as sentenças curtas, médias, longas e muito longas é muito curto (duas palavras)

        **Projeto**: GUTEN

        **Teste**: Todo mundo usa software livre, mas não sabe disso, como expliquei anteriormente. E mais pessoas
        usariam software livre se não houvesse tanta pirataria de software no mundo. No Brasil, 84% dos softwares de
        desktops são piratas.

        **Contagens**: 3 sentenças, uma das quais é curta (9 palavras).

        **Resultado Esperado**: 1/3 = 0,333

        **Resultado Obtido**: 0,333

        **Status**: correto
    """

    name = 'Short Sentences Rate'
    column_name = 'short_sentence_ratio'

    def value_for_text(self, t, rp=default_rp):
        CURTA = 11.763
        MEDIA = 13.027
        LONGA = 15.908
        sentences = rp.tagged_words_in_sents(t)
        tamanhos = [len(sentence) for sentence in sentences]
        intervalos = []
        for i in tamanhos:
            if i < CURTA:
                intervalos.append(0)
            elif CURTA <= i < MEDIA:
                intervalos.append(1)
            elif MEDIA <= i < LONGA:
                intervalos.append(2)
            else:
                intervalos.append(3)
        result = [
            intervalos.count(0),
            intervalos.count(1),
            intervalos.count(2),
            intervalos.count(3)
        ]
        try:
            return result[0] / sum(result)
        except:
            return 0


class MediumSentencesRate(base.Metric):
    """
        **Nome da Métrica**: medium_short_sentence_ratio

        **Interpretação**: não é clara a relação da métrica com o nível de complexidade textual. Em relação às sentenças
        curtas, as médias são mais complexas, já em relação às sentenças longas ou muito longas, as médias são menos
        complexas.

        **Descrição da métrica**: Proporção de Sentenças Médias  em relação a todas as sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: há 4 tamanhos de sentença: curto, médio, longo e
        muito longo. Os números de quantidade de palavras que separam os quatro tipos de sentenças são 11, 763 - 13,027
        e 15,908. Na prática, isso significa que sentenças curtas têm 11 palavras ou menos; sentenças médias têm 12 ou
        13 palavras; sentenças longas têm 14 ou 15 palavras e sentenças muito longas têm mais de 15 palavras.

        **Forma de cálculo da métrica**: Calcula-se a quantidade de palavras por sentença. Contam-se as sentenças com
        12 ou 13 palavras e divide-se o resultado pelo total de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador

        **Limitações da métrica**:

        **Crítica**: Não há como uma sentença ter número quebrado de palavras, então uma sentença média é aquela que
        tem 12 ou 13 palavras. O artifício de usar os números quebrados 11, 763 - 13,027 e 15,908 para separar os quatro
        intervalos só se justifica como forma de evitar ter que lidar com operações lógicas de “maior que” e “menor ou
        igual a”. Mas para isso as quantidades de palavras que delimitam os quatro intervalos de sentenças poderiam ser
        11,001 - 13,001 e 15,001.

        Os intervalos entre as sentenças curtas, médias, longas e muito longas é curto (duas palavras)

        **Projeto**: GUTEN

        **Teste**: Todo mundo usa software livre, mas não sabe disso, como expliquei anteriormente. E mais pessoas
        usariam software livre se não houvesse tanta pirataria de software no mundo. No Brasil, 84% dos softwares de
        desktops são piratas.

        **Contagens**: 3 sentenças, uma das quais é média (12 palavras).

        **Resultado Esperado**: 1/3 = 0,333

        **Resultado Obtido**: 0,333

        **Status**: correto
    """

    name = 'Medium Sentences Rate'
    column_name = 'medium_short_sentence_ratio'

    def value_for_text(self, t, rp=default_rp):
        CURTA = 11.763
        MEDIA = 13.027
        LONGA = 15.908
        sentences = rp.tagged_words_in_sents(t)
        tamanhos = [len(sentence) for sentence in sentences]
        intervalos = []
        for i in tamanhos:
            if i < CURTA:
                intervalos.append(0)
            elif CURTA <= i < MEDIA:
                intervalos.append(1)
            elif MEDIA <= i < LONGA:
                intervalos.append(2)
            else:
                intervalos.append(3)
        result = [
            intervalos.count(0),
            intervalos.count(1),
            intervalos.count(2),
            intervalos.count(3)
        ]
        try:
            return result[1] / sum(result)
        except:
            return 0


class LongSentencesRate(base.Metric):
    """
        **Nome da Métrica**: medium_long_sentence_ratio

        **Interpretação**: não é clara a relação da métrica com o nível de complexidade textual. Em relação às sentenças
        curtas e médias, as longas são mais complexas, já em relação às sentenças muito longas, as longas são menos
        complexas.

        **Descrição da métrica**: Proporção de Sentenças longas em relação a todas as sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: há 4 tamanhos de sentença: curto, médio, longo e
        muito longo. Os números de quantidade de palavras que separam os quatro tipos de sentenças são 11, 763 - 13,027
        e 15,908. Na prática, isso significa que sentenças curtas têm 11 palavras ou menos; sentenças médias têm 12 ou
        13 palavras; sentenças longas têm 14 ou 15 palavras e sentenças muito longas têm mais de 15 palavras.

        **Forma de cálculo da métrica**: Calcula-se a quantidade de palavras por sentença. Contam-se as sentenças que
        tenham 14 ou 15 palavras e divide-se o resultado pelo total de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador

        **Limitações da métrica**:

        **Crítica**: Não há como uma sentença ter número quebrado de palavras, então uma sentença longa é aquela que
        tem 14 ou 15 palavras. O artifício de usar os números quebrados 11, 763 - 13,027 e 15,908 para separar os
        quatro intervalos só se justifica como forma de evitar ter que lidar com operações lógicas de “maior que” e
        “menor ou igual a”. Mas para isso as quantidades de palavras que delimitam os quatro intervalos de sentenças
        poderiam ser 11,001 - 13,001 e 15,001.

        Os intervalos entre as sentenças curtas, médias, longas e muito longas é curto (duas palavras)

        **Projeto**: GUTEN

        **Teste**: O papel do código aberto é permitir a inovação localmente. A inovação é dificultada quando se demanda
        muito capital (seja dinheiro ou “alicerce”) para começar. As restrições insensatas que nos são impostas,
        chamadas “patentes” e “direitos autorais”, impedem as pessoas de construir sobre ideias geradas, e algumas
        grandes ideias são perdidas por nunca poderem superar a “inércia” gerada por essas restrições.

        **Contagens**: 3 sentenças (de 10, 15 e 36 palavras, portanto, 1 pequena, 1 longa e uma muito longa)

        **Resultado Esperado**: 1/3 = 0,333

        **Resultado Obtido**: 0,333

        **Status**: correto
    """

    name = 'Long Sentences Rate'
    column_name = 'medium_long_sentence_ratio'

    def value_for_text(self, t, rp=default_rp):
        CURTA = 11.763
        MEDIA = 13.027
        LONGA = 15.908
        sentences = rp.tagged_words_in_sents(t)
        tamanhos = [len(sentence) for sentence in sentences]
        intervalos = []
        for i in tamanhos:
            if i < CURTA:
                intervalos.append(0)
            elif CURTA <= i < MEDIA:
                intervalos.append(1)
            elif MEDIA <= i < LONGA:
                intervalos.append(2)
            else:
                intervalos.append(3)
        result = [
            intervalos.count(0),
            intervalos.count(1),
            intervalos.count(2),
            intervalos.count(3)
        ]
        try:
            return result[2] / sum(result)
        except:
            return 0


class VeryLongSentencesRate(base.Metric):
    """
        **Nome da Métrica**: long_sentence_ratio

        **Interpretação**: quanto maior a proporção de sentenças muito longas, maior a complexidade do texto

        **Descrição da métrica**: Proporção de Sentenças muito longas em relação a todas as sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: há 4 tamanhos de sentença: curto, médio, longo e
        muito longo. Os números de quantidade de palavras que separam os quatro tipos de sentenças são 11, 763 - 13,027
        e 15,908. Na prática, isso significa que sentenças curtas têm 11 palavras ou menos; sentenças médias têm 12 ou
        13 palavras; sentenças longas têm 14 ou 15 palavras e sentenças muito longas têm mais de 15 palavras.

        **Forma de cálculo da métrica**: Calcula-se a quantidade de palavras por sentença. Contam-se as sentenças que
        tenham mais de 15 palavras e divide-se o resultado pelo total de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador

        **Limitações da métrica**:

        **Crítica**: O artifício de usar os números quebrados 11, 763 - 13,027 e 15,908 para separar os quatro
        intervalos de tamanho de sentenças só se justifica como forma de evitar ter que lidar com operações lógicas de
        “maior que” e “menor ou igual a”. Mas para isso as quantidades de palavras que delimitam os quatro intervalos
        de sentenças poderiam ser 11,001 - 13,001 e 15,001.

        Os intervalos entre as sentenças curtas, médias, longas e muito longas é curto (duas palavras)

        **Projeto**: GUTEN

        **Teste**: O papel do código aberto é permitir a inovação localmente. A inovação é dificultada quando se demanda
        muito capital (seja dinheiro ou “alicerce”) para começar. As restrições insensatas que nos são impostas,
        chamadas “patentes” e “direitos autorais”, impedem as pessoas de construir sobre ideias geradas, e algumas
        grandes ideias são perdidas por nunca poderem superar a “inércia” gerada por essas restrições.

        **Contagens**: 3 sentenças (de 10, 15 e 36 palavras, portanto, 1 pequena, 1 longa e uma muito longa)

        **Resultado Esperado**: 1/3 = 0,333

        **Resultado Obtido**: 0,333

        **Status**: correto
    """

    name = 'Very Long Sentences Rate'
    column_name = 'long_sentence_ratio'

    def value_for_text(self, t, rp=default_rp):
        CURTA = 11.763
        MEDIA = 13.027
        LONGA = 15.908
        sentences = rp.tagged_words_in_sents(t)
        tamanhos = [len(sentence) for sentence in sentences]
        intervalos = []
        for i in tamanhos:
            if i < CURTA:
                intervalos.append(0)
            elif CURTA <= i < MEDIA:
                intervalos.append(1)
            elif MEDIA <= i < LONGA:
                intervalos.append(2)
            else:
                intervalos.append(3)
        result = [
            intervalos.count(0),
            intervalos.count(1),
            intervalos.count(2),
            intervalos.count(3)
        ]
        try:
            return result[3] / sum(result)
        except:
            return 0


class SentenceLengthMin(base.Metric):
    """
        **Nome da Métrica**: sentence_length_min

        **Interpretação**: não há relação direta entre a métrica e a complexidade textual

        **Descrição da métrica**: Quantidade mínima de palavras por sentença

        **Definição dos termos que aparecem na descrição da métrica**: a quantidade mínima de palavras por sentença é o
        tamanho da menor sentença do texto

        **Forma de cálculo da métrica**: Calculam-se as quantidades de palavras de todas as sentenças do texto.
        Classificam-se resultados e identifica-se a menor quantidade

        **Recursos de PLN utilizados durante o cálculo**: tokenizador nltk

        **Limitações da métrica**:

        **Crítica**: é preciso conferir a forma de tokenização utilizada, pois a quantidade mínima de palavras foi de
        11, ao invés de 10. É possível que as pontuações estejam sendo consideradas ou que as contrações estejam sendo
        desfeitas (ex: do = de + o)

        **Projeto**: GUTEN

        **Teste**: O papel do código aberto é permitir a inovação localmente. A inovação é dificultada quando se demanda
        muito capital (seja dinheiro ou “alicerce”) para começar. As restrições insensatas que nos são impostas,
        chamadas “patentes” e “direitos autorais”, impedem as pessoas de construir sobre ideias geradas, e algumas
        grandes ideias são perdidas por nunca poderem superar a “inércia” gerada por essas restrições.

        **Contagens**: 3 orações, com 10, 15 e 36 palavras

        **Resultado Esperado**: 10

        **Resultado Obtido**: 10

        **Status**: correto
    """

    name = 'Sentence Length Min'
    column_name = 'sentence_length_min'

    def value_for_text(self, t, rp=default_rp):
        return min(rp.sentence_lengths(t))


class SentenceLengthMax(base.Metric):
    """
        **Nome da Métrica**: sentence_length_max

        **Interpretação**: não há relação direta entre a métrica e a complexidade textual

        **Descrição da métrica**: Quantidade máxima de palavras por sentença

        **Definição dos termos que aparecem na descrição da métrica**: a quantidade máxima de palavras por sentença é o
        tamanho da maior sentença do texto

        **Forma de cálculo da métrica**: Calculam-se as quantidades de palavras de todas as sentenças do texto.
        Classificam-se resultados e identifica-se a maior quantidade

        **Recursos de PLN utilizados durante o cálculo**: tokenizador nltk

        **Limitações da métrica**:

        **Crítica**: é preciso conferir a forma de tokenização utilizada; como o resultado da maior sentença deu 43 ao
        invés de 36, é possível que as pontuações estejam sendo consideradas.

        **Projeto**: GUTEN

        **Teste**: O papel do código aberto é permitir a inovação localmente. A inovação é dificultada quando se demanda
        muito capital (seja dinheiro ou “alicerce”) para começar. As restrições insensatas que nos são impostas,
        chamadas “patentes” e “direitos autorais”, impedem as pessoas de construir sobre ideias geradas, e algumas
        grandes ideias são perdidas por nunca poderem superar a “inércia” gerada por essas restrições.

        **Contagens**: 3 orações, com 11, 15 e 36 palavras

        **Resultado Esperado**: 36

        **Resultado Obtido**: 37 (o tokenizador anotou como NUM (numeral) as aspas abertas antes de “direitos autorais”

        **Status**: correto, considerando a limitação do tokenizador
    """

    name = 'Sentence Length Max'
    column_name = 'sentence_length_max'

    def value_for_text(self, t, rp=default_rp):
        return max(rp.sentence_lengths(t))


class SentenceLengthStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: sentence_length_standard_deviation

        **Interpretação**: não há relação direta da métrica com a complexidade textual

        **Descrição da métrica**: Desvio Padrão da quantidade de palavras por sentença

        **Definição dos termos que aparecem na descrição da métrica**: desvio-padrão é o quanto as medidas variam em
        relação à média

        **Forma de cálculo da métrica**: Calculam-se as quantidades de palavras de cada sentença e depois calcula-se o
        desvio-padrão entre os resultados.

        **Recursos de PLN utilizados durante o cálculo**: tokenizador

        **Limitações da métrica**:

        **Crítica**: Verificamos que o “abre aspas” pode ser eventualmente etiquetado como uma categoria gramatical e
        por isso é contado como token.

        **Projeto**: GUTEN

        **Teste**: O papel do código aberto é permitir a inovação localmente. A inovação é dificultada quando se demanda
        muito capital (seja dinheiro ou “alicerce”) para começar. As restrições insensatas que nos são impostas,
        chamadas “patentes” e “direitos autorais”, impedem as pessoas de construir sobre ideias geradas, e algumas
        grandes ideias são perdidas por nunca poderem superar a “inércia” gerada por essas restrições.

        **Contagens**: 3 sentenças, com 10, 15 e 36 palavras

        **Resultado Esperado**: 13,796

        **Resultado Obtido**: 13,597 (na última sentença o nlpnet reconheceu 37 palavras)

        **Status**: correto

    """

    name = 'Sentence Length Standard Deviation'
    column_name = 'sentence_length_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        lengths = rp.sentence_lengths(t)
        return np.std(lengths)


class ContentWordsAmbiguity(base.Metric):
    """
        **Nome da Métrica**: content_words_ambiguity

        **Interpretação**: não está clara a relação da métrica com a complexidade.

        **Descrição da métrica**: Média de sentidos por palavra de conteúdo do texto

        **Definição dos termos que aparecem na descrição da métrica**: a quantidade de sentidos é o número de sentidos
        que uma palavra tem no dicionário TEP (Thesaurus Eletrônico do Português.

        **Forma de cálculo da métrica**: Para cada palavra de conteúdo do texto (substantivos, verbos, adjetivos e
        advérbios), soma-se o número de sentidos que ela apresenta no TEP (http://www.nilc.icmc.usp.br/tep2/); depois
        divide-se o resultado pelo número de palavras de conteúdo do texto que foram encontradas no TEP.

        **Recursos de PLN utilizados durante o cálculo**: tagger nlpnet e TEP Thesaurus Eletrônico do Português

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger e da estratégia de lematização
        utilizada, pois se as categorias de palavras de conteúdo não forem devidamente identificadas e lematizadas, as
        palavras não poderão ser procuradas no TEP.

        **Crítica**:

        Teoricamente, a ambiguidade é um fator que aumenta a complexidade. Utilizar a quantidade de sentidos da palavra
        para medir ambiguidade, porém, pode não resultar em uma boa métrica, pois as palavras mais raras (e mais
        complexas) são as que possuem menos sentidos e as palavras mais frequentes são as que possuem mais sentidos.
        As palavras mais frequentes são, também, as primeiras a serem adquiridas e, portanto, as mais simples. Por
        exemplo, o verbo “ser” tem 12 sentidos no TEP e, por isso, contribui para a obtenção de um resultado alto nesta
        métrica. Não se pode inferir, contudo, que a ocorrência do verbo “ser” aumente a complexidade do texto. É
        possível que essa métrica tenha se originado no tratamento automático da ambiguidade. Por isso, é preciso
        atentar para o fato de que o que é ambíguo para a máquina não é necessariamente ambíguo para o ser humano.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino colou na prova, embora soubesse que poderia ser pego.

        **Contagens**: 7 palavras de conteúdo, com um total de 52 sentidos
            2 substantivos (menino, prova), com 1 e 9 sentidos no TEP
            5 verbos (colou, soubesse, poderia, ser, pego) com  4, 7, 2, 12 e 17 sentidos no TEP
            Nenhum adjetivo e nenhum advérbio.
            A lematização não identificou o verbo “pegar”, por isso o cálculo foi feito com 6 palavras e u

        **Resultado Esperado**: 7,43 (52/7)

        **Resultado Obtido**:  5,83 (35/6, pois não foi identificado o verbo “pegar” a partir da forma “pego”)

        **Status**:  correto, considerando o erro do tagger na identificação da classe de “pego” (verbo “pegar”)
    """

    name = 'Content Words Ambiguity'
    column_name = 'content_words_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        adjectives = get_meanings_count(rp, t, 'A', 'Adjetivo',
                                         rp.pos_tagger().tagset.is_adjective)
        adverbs = get_meanings_count(rp, t, 'ADV', 'Advérbio',
                                      rp.pos_tagger().tagset.is_adverb)
        nouns = get_meanings_count(rp, t, 'N', 'Substantivo',
                                    rp.pos_tagger().tagset.is_noun)
        verbs = get_meanings_count(rp, t, 'V', 'Verbo',
                                    rp.pos_tagger().tagset.is_verb)
        total_words = len(adjectives) + len (adverbs) + len(nouns) + len(verbs)
        try:
            return (sum(adjectives) + sum(adverbs) + sum(nouns) + sum(verbs)) / total_words
        except:
            return 0


class AdjacentPersonalPronounAnaphoricReferences(AnaphoricReferencesBase):
    """
        **Nome da Métrica**: coreference_pronoun_ratio

        **Interpretação**: quanto maior a métrica, maior a complexidade textual

        **Descrição da métrica**: Média de candidatos a referente, na sentença anterior, por pronome anafórico do caso
        reto.

        **Definição dos termos que aparecem na descrição da métrica**: pronomes anafóricos são aqueles que retomam um
        referente que ocorreu antes no texto. No caso desta métrica, são considerados apenas os pronomes anafóricos do
        caso reto: ele, ela, eles, elas. O referente do pronome anafórico é procurado na sentença adjacente anterior.

        **Forma de cálculo da métrica**: Identificam-se os pronomes de caso reto. Para cada pronome, procuram-se, na
        sentença anterior, substantivos candidatos a referente que tenham o mesmo gênero (masculino ou feminino) e o
        mesmo número (singular ou plural) do pronome. Somam-se os candidatos e divide-se o resultado pelo número de
        pronomes anafóricos de caso reto, a fim de obter a média de candidatos por pronome. Apenas os substantivos
        constantes do léxico DELAF são considerados.

        **Recursos de PLN utilizados durante o cálculo**: DELAF – léxico de formas do português

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: As principais propostas apresentadas na última convenção do partido foram feitas pelas mulheres.
        Elas estão engajadas na missão de reformar o estatuto até o final do ano. Mas muitos integrantes do partido não
        querem que ele seja reformado.

        **Contagens**: 2 pronomes anafóricos do caso reto: “elas” tem 2 candidatos a referente na sentença anterior
        (propostas, mulheres) e “ele” tem 3 candidatos a referente na sentença anterior (estatuto, final, ano).

        **Resultado Esperado**: 5/2 = 2,5

        **Resultado Obtido**: 2,5

        **Status**: correto
    """
    referents = {r'^elas$': 'fp',
                 r'^eles$': 'mp',
                 r'^ela$': 'fs',
                 r'^ele$': 'ms',
                 }
    name = '''Ratio of candidates of personal pronouns to anaphoric reference
            in adjacente sentences'''
    column_name = 'coreference_pronoun_ratio'

    def __init__(self):
        super(AdjacentPersonalPronounAnaphoricReferences, self).__init__(nsentences=1)


# class RelativeSubordinateClauses(base.Metric):
#     """
#         **Nome da Métrica**: relative_subordinate_clauses
#
#         **Interpretação**: quanto maior a proporção, maior a complexidade
#
#         **Descrição da métrica**: Proporção de orações relativas em relação a todas as orações do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: orações relativas são orações subordinadas
#         adjetivas introduzidas por pronomes relativos: que, o qual, a qual, os quais, as quais, cujo, cuja, cujos,
#         cujas.
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências da etiqueta <rel> e divide-se o resultado pela
#         quantidade de orações do texto (V – aux)
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras.
#
#         **Limitações da métrica**: a precisão dos valores depende diretamente do desempenho do parser Palavras
#
#         **Crítica**: Esta métrica foi corrigida, pois anteriormente o divisor era a quantidade de conjunções
#         coordenativas e subordinativas, tomadas como índices de orações coordenadas e subordinadas, o que foi
#         constatado ser um erro. Com a correção, a métrica passou a usar a quantidade de orações como divisor, mas isso
#         a tornou idêntica a outra métrica, relative_clauses, do AIC, motivo pelo qual deve ser comentada.
#
#         **Projeto**: GUTEN
#
#         **Teste**: A mulher que eu contratei, cujo pai eu já conhecia, é aquela que você viu no dia em que chegou aqui.
#          Não sei qual é seu interesse nela, mas afirmo que, seja ele qual for, não me interessa. Os assuntos nos quais
#          estou interessado não são de ordem pessoal.
#
#         **Contagens**: 13 orações e 6 pronomes relativos: que, cujo, que, que, qual, quais (qual=for é anotado como
#         expressão)
#
#         **Resultado Esperado**: 0,462
#
#         **Resultado Obtido**: 0,462
#
#         **Status**: correto
#     """
#
#     name = '''Ratio of Relative Subordinate Clauses per number of Clauses'''
#     column_name = 'relative_subordinate_clauses'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         adjectives = len(re.findall('<rel>', flat))
#         try:
#             return adjectives / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class CoordinateClausesPredominance(base.Metric):
#     """
#         **Nome da Métrica**: coordinate_clauses_predominance
#
#         **Interpretação**: as orações coordenadas são mais simples que as subordinadas; portanto, se houver
#         predominância de coordenadas a complexidade textual é menor do que se não houver
#
#         **Descrição da métrica**: proporção de orações coordenadas em relação a todas as orações coordenadas,
#         subordinadas e relativas.
#
#         **Definição dos termos que aparecem na descrição da métrica**: orações coordenadas são orações independentes;
#         orações subordinadas são dependentes.
#
#         **Forma de cálculo da métrica**: somam-se as ocorrências de conjunções coordenativas (tag ‘KC’) e divide-se o
#         resultado pela soma de conjunções coordenativas (tag: ‘KC’), conjunções subordinativas (tag ‘KS’) e orações
#         relativas (tag <rel>)
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**: após extenso estudo, inclusive envolvendo o criador do parser, Eckhard Bick,
#         descobriu-se que não há algoritmo conhecido para capturar as orações coordenadas, portanto esta métrica não é
#         possível de ser calculada com os recursos disponíveis atualmente.
#
#         **Crítica**: a métrica deve ser comentada devido aos seguintes motivos:
#
#             1) A forma de calcular orações deveria ser como nas outras métricas (V – <aux>)
#
#             2) As etiquetas utilizadas para o cálculo são inapropriadas. As conjunções coordenativas (KC) coordenam
#             tanto sintagmas nominais quanto orações, portanto, utilizar sua quantidade como reflexo da quantidade de
#             orações coordenadas é errado. Já as conjunções subordinativas (KS) introduzem orações subordinadas, mas
#             apenas um conjunto delas. As subordinadas relativas estão sendo citadas como se não fossem um tipo de
#             subordinadas e as subordinadas reduzidas de gerúndio, particípio e infinitivo não estão sendo computadas.
#
#             3) A captura das coordenadas via conjunção coordenativa deveria multiplicar o resultado por dois, pois cada
#             conjunção coordena 2 orações. Isso não ocorre nas orações subordinadas, pois apenas uma das orações é
#             subordinada e a outra, a subordinadora, é chamada de oração principal.
#
#             4) As orações coordenadas assindéticas (separadas por vírgulas) não estão sendo computadas
#
#             5) A métrica não está retornando 0 ou 1 dependendo de haver ou não predominância.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Aldo e José estudaram para a prova, assistindo vídeo-aulas.
#
#         **Contagens**: 2 orações, 1 subordinada reduzida de gerúndio, nenhuma coordenada.
#
#         **Resultado Esperado**: 0
#
#         **Resultado Obtido**: 0,50 (o classificador contou o “e” como evidência de oração coordenada e não identificou a
#         oração subordinada porque ela não é introduzida por conjunção subordinativa)
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Coordinate Clauses to Coordinate and Subordinate Ones'
#     column_name = 'coordinate_clauses_predominance'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         coord_clauses = re.findall(r"<co-(vfin|ger|inf|pcv)>.*KC", flat)
#         try:
#             return len(coord_clauses) / rp.num_clauses(t)
#         except ZeroDivisionError:
#             return 0


# class Verbs3DegreeRatio(base.Metric):
#     """
#         **Nome da Métrica**: most_frequent_verbs_of_3-degree
#
#         **Interpretação**: em sua concepção, quanto maior a proporção, menor a complexidade
#
#         **Descrição da métrica**: Proporção de verbos simples em relação a todos os verbos do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: verbos simples ou verbos mais frequentes do nível
#         1 ou verbos mais frequentes do 3º ano são: ser, ir, ter, poder, estar, ficar, dever, precisar, haver, viver,
#         passar. Não há comentário sobre como essa lista de verbos foi levantada.
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências dos verbos da lista e divide-se o resultado pela
#         quantidade de verbos do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**:
#
#         **Limitações da métrica**:
#
#         **Crítica**:
#
#         A métrica só reconhece formas no infinitivo e não usa lematizador.
#
#         Verbos não podem ser classificados em “simples” ou “complexos” pelos seus lemas. Há formas verbais simples e
#         formas verbais complexas que possuem um mesmo lema. Por exemplo, a forma “há” do verbo haver é altamente
#         frequente, mas a forma “houvéssemos”, do mesmo verbo, é mais rara e complexa.
#
#         A métrica não distingue verbos principais de verbos auxiliares. Verbos auxiliares ocorrem mais, devido a sua
#         função gramatical de atribuir tempo, modo, aspecto e voz passiva. Portanto, verbos com função de auxiliares
#         deveriam ser desprezados.
#
#         **Projeto**: GUTEN
#
#         **Teste**: O reaproveitamento das águas residuais está apenas no início e tem todas as condições para ser uma
#         importante fonte não apenas de água doce, mas também de itens como fósforo, nitratos e biogás
#
#         **Contagens**: 3 verbos (está, tem, ser), todos da lista de verbos simples
#
#         **Resultado Esperado**: 3/3 = 1
#
#         **Resultado Obtido**: 0,333
#
#         **Status**: incorreto
#
#     """
#
#     name = 'Most Frequent Verbs of 3-degree'
#     column_name = 'most_frequent_verbs_of_3-degree'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         expression = re.compile('''
#                                 \[ser\]|
#                                 \[ir\]|
#                                 \[ter\]|
#                                 \[poder\]|
#                                 \[estar\]|
#                                 \[ficar\]|
#                                 \[dever\]|
#                                 \[precisar\]|
#                                 \[haver\]|
#                                 \[viver\]|
#                                 \[passar\]
#                                 ''',
#                                 re.VERBOSE)
#         try:
#             return len(re.findall(expression, flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             return 0


class Subtitles(base.Metric):
    """
        **Nome da Métrica**: subtitles

        **Interpretação**: não é clara a relação da métrica com a complexidade textual, mas supõe-se que os subtítulos
        contribuam para a clareza pelo fato de delimitarem assuntos no texto.

        **Descrição da métrica**: Proporção de Subtítulos em relação à quantidade de sentenças do texto

        **Definição dos termos que aparecem na descrição da métrica**: subtítulos são títulos intermediários ao longo
        do texto

        **Forma de cálculo da métrica**: contam-se os subtítulos etiquetados com <subtitle>   </subtitle> e divide-se
        pela quantidade de sentenças do texto.

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**: é preciso usar diversas heurísticas que capturem os subtítulos e não apenas a que encontra o
        formato dos subtítulos no corpus de treinamento do classificador. Deveria ser expandida para uso correto no
        futuro.

        **Projeto**: GUTEN

        **Teste 1**:

        A Mudança de Consciência

        Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado no
        tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais de
        6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
        frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
        Estados Unidos.

        A Mudança na Saúde

        É possível que esse vídeo faça uma enorme diferença na mudança dos hábitos alimentares dos americanos e provoque
        um decréscimo dos índices de colesterol da população.

        **Teste 2**:

        <subtitle> A Mudança de Consciência </subtitle>

        Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado no
        tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais de
        6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
        frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
        Estados Unidos.

        <subtitle> A Mudança na Saúde </subtitle>

        É possível que esse vídeo faça uma enorme diferença na mudança dos hábitos alimentares dos americanos e provoque
        um decréscimo dos índices de colesterol da população.

        **Contagens**: 2 subtítulos, 4 sentenças

        **Resultado Esperado**: 2/4

        **Resultado Obtido**: 0,5

        **Status**: correto
    """

    name = 'Number of Subtitles'
    column_name = 'subtitles'

    def value_for_text(self, t, rp=default_rp):
        try:
            return t.subtitles / len(rp.sentences(t))
        except AttributeError:
            return 0


class FunctionWordDiversity(base.Metric):
    """
        **Nome da Métrica**: function_word diversity

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de palavras funcionais em relação à quantidade de tokens de
        palavras funcionais no texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras funcionais as palavras
        de 6 classes gramaticais: artigos (tag: ‘ART’), conjunções (tags ‘KS’ e ‘KC’), interjeições (tag: ‘IN’),
        numerais (tag: ‘NUM’), pronomes (tags: 'PROPESS',

        'PROSUB', 'PROADJ', 'PRO-KS', 'PRO-KS-REL'), preposições (tags: 'PREP', 'PREP+PROPESS', 'PREP+ART',
        'PREP+PRO-KS', 'PREP+PRO-KS-REL', 'PREP+PROADJ', 'PREP+ADV', 'PREP+PROSUB'). Incluem-se nas palavras funcionais
        os advérbios com função coordenativa e subordinativa (tags: 'ADV-KS', 'ADV-KS-REL).

        **Forma de cálculo da métrica**: divide-se a quantidade de palavras funcionais diferentes (sem repetição) pela
        quantidade total de palavras funcionais.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado
        no tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais
        de 6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
        frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
        Estados Unidos.

        **Contagens**: 27 palavras funcionais, 18 sem repetições (o tagger reconhece meia, milhões e 2009 como
        substantivos)

        **Resultado Esperado**: 18/27 = 0,667

        **Resultado Obtido**: 0,667

        **Status**: correto
    """

    name = 'Function Word Diversity Ratio'
    column_name = 'function_word_diversity'

    def value_for_text(self, t, rp=default_rp):
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        function_words = [i[0].lower() for i in function_words]
        # unique = len(set(function_words))
        try:
            return rp.mattr(function_words)
            # return unique / len(function_words)
        except ZeroDivisionError:
            return 0


class ContentWordsMin(base.Metric):
    """
        **Nome da Métrica**: content_word min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção Mínima de palavras de conteúdo por quantidade de palavras nas sentenças

        **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
        adjetivos e advérbios.

        **Forma de cálculo da métrica**: Calcula-se a proporção de palavras de conteúdo por quantidade de palavras para
        cada sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger e do sentenciador.

        **Crítica**: as proporções de palavras de conteúdo pela quantidade de palavras nas sentenças são muito próximas
        umas das outras e por isso têm baixo poder discriminativo.

        **Projeto**: GUTEN

        **Teste**: Como marcar pessoas em fotos no Facebook. 1) Clique na foto para expandi-la. 2) Passe o cursor sobre
        a foto e clique em “marcar foto” na parte inferior. 3) Clique na pessoa na foto e comece a digitar o nome dela.
        4) Escolha o nome completo da pessoa que você desejar marcar, quando for exibido. 5) Clique em “finalizar
        marcação”.

        **Contagens**: 6 sentenças
            Palavras de conteúdo por sentença [4, 3, 8, 6, 8, 3]
            Palavras por sentença [7, 7, 16, 14, 16, 6]
            Proporções de palavras de conteúdo por sentença [0,57, 0,43, 0,5, 0,42, 0,5, 0,5]

        **O programa identificou**:
            Palavras de conteúdo por sentença [4, 4, 9, 7, 9, 5]
            Palavras por sentença [8, 8, 19, 15, 17, 9]
            Proporções de palavras de conteúdo por sentença [0.5, 0.5, 0.47, 0.47, 0.53, 0.56]

        **Resultado Esperado**: 0,42

        **Resultado Obtido**: 0,47 (o tokenizador está contando pontuações como palavras e isso aumenta o divisor do
        cálculo)

        **Status**: correto, considerando as limitações do tokenizador

    """

    name = 'Content Word Min'
    column_name = 'content_word_min'

    def value_for_text(self, t, rp=default_rp):
        cw = [len(i) for i in rp.content_words(t)]
        words = [len(i) for i in rp.tagged_sentences(t)]
        result = [cw[i] / words[i] for i in range(len(cw))]
        return np.array(result).min()


class ContentWordsMax(base.Metric):
    """
        **Nome da Métrica**: content_word max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção Máxima de palavras de conteúdo por quantidade de palavras nas sentenças

        **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
        adjetivos e advérbios.

        **Forma de cálculo da métrica**: Calcula-se a proporção de palavras de conteúdo por quantidade de palavras para
        cada sentença. Classificam-se os resultados e identifica-se a maior proporção.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet e nltk toolkit

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger e do sentenciador.

        **Crítica**: as proporções de palavras de conteúdo pela quantidade de palavras nas sentenças são muito próximas
        umas das outras e por isso têm baixo poder discriminativo.

        **Projeto**: GUTEN

        **Teste**: Como marcar pessoas em fotos no Facebook. 1) Clique na foto para expandi-la. 2) Passe o cursor sobre
        a foto e clique em “marcar foto” na parte inferior. 3) Clique na pessoa na foto e comece a digitar o nome dela.
        4) Escolha o nome completo da pessoa que você desejar marcar, quando for exibido. 5) Clique em “finalizar
        marcação”.

        **Contagens**: 6 sentenças
            Palavras de conteúdo por sentença [4, 3, 8, 6, 8, 3]
            Palavras por sentença [7, 7, 16, 14, 16, 6]
            Proporções de palavras de conteúdo por sentença [0,57, 0,43, 0,5, 0,42, 0,5, 0,5]

        **O programa identificou**:
            Palavras de conteúdo por sentença [4, 4, 9, 7, 9, 5]
            Palavras por sentença [8, 8, 19, 15, 17, 9]
            Proporções de palavras de conteúdo por sentença [0.5, 0.5, 0.47, 0.47, 0.53, 0.56]

        **Resultado Esperado**: 0,57

        **Resultado Obtido**: 0,53 (o tokenizador está contando pontuações como palavras e isso aumenta o divisor do
        cálculo)

        **Status**: correto, considerando as limitações do tokenizador
    """

    name = 'Content Word Max'
    column_name = 'content_word_max'

    def value_for_text(self, t, rp=default_rp):
        cw = [len(i) for i in rp.content_words(t)]
        words = [len(i) for i in rp.tagged_sentences(t)]
        result = [cw[i] / words[i] for i in range(len(cw))]
        return np.array(result).max()


class ContentWordsStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: content_word standard_deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre as palavras de conteúdo e a quantidade de palavras
        das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: palavras de conteúdo são substantivos, verbos,
        adjetivos e advérbios.

        **Forma de cálculo da métrica**: Calcula-se a proporção de palavras de conteúdo por quantidade de palavras para
        cada sentença. Calcula-se o desvio padrão .

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet e nltk toolkit

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger e do sentenciador.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Como marcar pessoas em fotos no Facebook. 1) Clique na foto para expandi-la. 2) Passe o cursor sobre
        a foto e clique em “marcar foto” na parte inferior. 3) Clique na pessoa na foto e comece a digitar o nome dela.
        4) Escolha o nome completo da pessoa que você desejar marcar, quando for exibido. 5) Clique em “finalizar
        marcação”.

        **Contagens**:
            6 sentenças,
            Palavras de conteúdo por sentença [4, 3, 8, 6, 8, 3]
            Palavras por sentença [7, 7, 16, 14, 16, 6]
            Proporções de palavras de conteúdo por sentença [0,57, 0,43, 0,5, 0,42, 0,5, 0,5]

        **O programa identificou**:
            Palavras de conteúdo por sentença [4, 4, 9, 7, 9, 5]
            Palavras por sentença [8, 8, 19, 15, 17, 9]
            Proporções de palavras de conteúdo por sentença [0.5, 0.5, 0.47, 0.47, 0.53, 0.56]

        **Resultado Esperado**: 0,055

        **Resultado Obtido**: 0,031 (o tokenizador está contando pontuações como palavras e isso aumenta o divisor do
        cálculo)

        **Status**: correto, considerando as limitações do tokenizador
    """

    name = 'Content Word Standard Deviation'
    column_name = 'content_word_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        cw = [len(i) for i in rp.content_words(t)]
        words = [len(i) for i in rp.tagged_sentences(t)]
        result = [cw[i] / words[i] for i in range(len(cw))]
        return np.array(result).std()


class ContentWordDiversity(base.Metric):
    """
        **Nome da Métrica**: content_word diversity

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de palavras de conteúdo em relação à quantidade de tokens de
        palavras de conteúdo no texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo:
        substantivos, verbos, adjetivos e advérbios.

        **Forma de cálculo da métrica**: divide-se a quantidade de palavras de conteúdo diferentes (sem repetição) pela
        quantidade total de palavras de conteúdo

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado
        no tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais
        de 6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
        frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
        Estados Unidos.

        **Contagens**: 41 palavras de conteúdo, 38 sem repetições. A contagem manual deu 40 e 37, mas descobrimos que o
        tagger contou um abre aspas como substantivo. Consideramos correta, pois o erro é devido à limitação da
        ferramenta utilizada.

        **Resultado Esperado**: 38/41 = 0,927

        **Resultado Obtido**: 0,927

        **Status**: correto

    """

    name = 'Content Word Diversity Ratio'
    column_name = 'content_word_diversity'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        content_words = [i[0].lower() for i in content_words]
        # unique = len(set(content_words))
        try:
            return rp.mattr(content_words)
            # return unique / len(content_words)
        except ZeroDivisionError:
            return 0


class PronounsMin(base.Metric):
    """
        **Nome da Métrica**: pronouns min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção mínima de pronomes em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados pronomes as palavras anotadas
        com as etiquetas PROPESS, PROSUB, PROADJ, PRO-KS, PRO-KS-REL pelo POS tagger nlpnet. Há também as etiquetas de
        contrações de preposições com pronomes: PREP+PROPESS,PREP+PRO-KS, PREP+PRO-KS-REL,PREP+PROADJ, PREP+PROSUB.

        **Forma de cálculo da métrica**: Calcula-se a proporção de pronomes por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os pronomes

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 3, 0, 2, 1 e 0 pronomes,
        respectivamente. Proporções: 3/15 = 0,2; 0/12 = 0; 2/12 = 0,167; 1/15 = 0,067; 0/15 = 0

        **Resultado Esperado**: 0

        **Resultado Obtido**: 0

        **Status**: correto
    """

    name = 'Pronouns Min'
    column_name = 'pronouns_min'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        pronouns = [filter(pos_tagger.tagset.is_pronoun, i) for i in sents]
        pronouns = [len(list(i)) for i in pronouns]

        result = [pronouns[i] / sents_count[i] for i in range(len(pronouns))]
        return np.array(result).min()


class PronounsMax(base.Metric):
    """
        **Nome da Métrica**: pronouns max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção máxima de pronomes em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados pronomes as palavras anotadas
        com as etiquetas PROPESS, PROSUB, PROADJ, PRO-KS, PRO-KS-REL pelo POS tagger nlpnet. Há também as etiquetas de
        contrações de preposições com pronomes: PREP+PROPESS,PREP+PRO-KS, PREP+PRO-KS-REL,PREP+PROADJ, PREP+PROSUB.

        **Forma de cálculo da métrica**: Calcula-se a proporção de pronomes por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a maior proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os pronomes

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 3, 0, 2, 1 e 0 pronomes,
        respectivamente. Proporções: 3/15 = 0,2; 0/12 = 0; 2/12 = 0,167; 1/15 = 0,067; 0/15 = 0

        **Resultado Esperado**: 0,2

        **Resultado Obtido**: 0,2

        **Status**: correto
    """

    name = 'Pronouns Max'
    column_name = 'pronouns_max'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        pronouns = [filter(pos_tagger.tagset.is_pronoun, i) for i in sents]
        pronouns = [len(list(i)) for i in pronouns]

        result = [pronouns[i] / sents_count[i] for i in range(len(pronouns))]
        return np.array(result).max()


class PronounsStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: pronouns standard deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre pronomes e a quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados pronomes as palavras anotadas
        com as etiquetas PROPESS, PROSUB, PROADJ, PRO-KS, PRO-KS-REL pelo POS tagger nlpnet. Há também as etiquetas de
        contrações de preposições com pronomes: PREP+PROPESS,PREP+PRO-KS, PREP+PRO-KS-REL,PREP+PROADJ, PREP+PROSUB.

        **Forma de cálculo da métrica**: Calcula-se a proporção de pronomes por quantidade de palavras para cada
        sentença. Calcula-se o desvio padrão das proporções obtidas.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os pronomes

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 3, 0, 2, 1 e 0 pronomes,
        respectivamente. Proporções: 3/15 = 0,2; 0/12 = 0; 2/12 = 0,167; 1/15 = 0,067; 0/15 = 0

        **Resultado Esperado**: 0,083

        **Resultado Obtido**: 0,083

        **Status**: correto
    """

    name = 'Pronouns Standard Deviation'
    column_name = 'pronouns_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        pronouns = [filter(pos_tagger.tagset.is_pronoun, i) for i in sents]
        pronouns = [len(list(i)) for i in pronouns]

        result = [pronouns[i] / sents_count[i] for i in range(len(pronouns))]
        return np.array(result).std()


class PronounDiversity(base.Metric):
    """
        **Nome da Métrica**: pronoun diversity

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de pronomes em relação à quantidade de tokens de pronomes no texto

        **Definição dos termos que aparecem na descrição da métrica**: pronomes são palavras que substituem ou
        qualificam os substantivos. No POS tagger nlpnet, os pronomes são representados pelas etiquetas: PROPESS,
        PROSUB, PROADJ, PRO-KS, PRO-KS-REL. Há também as etiquetas de contrações de preposições com pronomes:
        PREP+PROPESS,PREP+PRO-KS, PREP+PRO-KS-REL,PREP+PROADJ, PREP+PROSUB.

        **Forma de cálculo da métrica**: divide-se a quantidade de pronomes diferentes (sem repetição) pela quantidade
        total de pronomes no texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: o POS tagger nlpnet não faz descontração, por isso é preciso usar as etiquetas de
        contrações de preposição com pronomes para capturar todos os pronomes (PREP+PROPESS,PREP+PRO-KS,
        PREP+PRO-KS-REL,PREP+PROADJ, PREP+PROSUB).

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O principal defeito dele é não prestar atenção aos detalhes de sua escrita. Ela é muito rica
        conceitualmente, porém contém aqueles tipos de erro de ortografia que ninguém mais comete. Desde que trabalha
        conosco, ele se nega a utilizar um editor eletrônico. Se ele o fizesse, grande parte de seus erros
        desapareceriam.

        **Contagens**: 10 pronomes, 9 sem considerar repetições

        **Resultado Esperado**: 9/10 = 0,90

        **Resultado Obtido**: 0,90

        **Status**: correto
    """

    name = 'Pronoun Diversity Ratio'
    column_name = 'pronoun_diversity'

    def value_for_text(self, t, rp=default_rp):
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        pronouns = [i[0].lower() for i in pronouns]
        # unique = len(set(pronouns))
        try:
            return rp.mattr(pronouns)
            # return unique / len(pronouns)
        except ZeroDivisionError:
            return 0


class AdverbsMin(base.Metric):
    """
        **Nome da Métrica**: adverbs min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção mínima de advérbios em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados advérbios as palavras anotadas
        com as etiquetas ADV e PDEN pelo POS tagger nlpnet. Há também a etiqueta de contrações de preposições com
        advérbios: PREP+ADV.

        **Forma de cálculo da métrica**: Calcula-se a proporção de advérbios por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os advérbios

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, com 0, 1, 0, 1 e 0 advérbios (o nlpnet não reconheceu
        “só” como advérbio). Proporções: 0/15 = 0; 1/12 = 0,083; 0/12 = 0; 1/15 = 0,067; 0/8 = 0

        **Resultado Esperado**: 0

        **Resultado Obtido**: 0

        **Status**: correto
    """

    name = 'Adverbs Min'
    column_name = 'adverbs_min'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adverbs = [filter(pos_tagger.tagset.is_adverb, i) for i in sents]
        adverbs = [len(list(i)) for i in adverbs]

        result = [adverbs[i] / sents_count[i] for i in range(len(adverbs))]
        return np.array(result).min()


class AdverbsMax(base.Metric):
    """
        **Nome da Métrica**: adverbs max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção máxima de advérbios em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados advérbios as palavras anotadas
        com as etiquetas ADV e PDEN pelo POS tagger nlpnet. Há também a etiqueta de contrações de preposições com
        advérbios: PREP+ADV.

        **Forma de cálculo da métrica**: Calcula-se a proporção de advérbios por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a maior proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os advérbios

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, com 0, 1, 0, 1 e 0 advérbios (o nlpnet não reconheceu
        “só” como advérbio). Proporções: 0/15 = 0; 1/12 = 0,083; 0/12 = 0; 1/15 = 0,067; 0/8 = 0

        **Resultado Esperado**: 0,083

        **Resultado Obtido**: 0,083

        **Status**: correto
    """

    name = 'Adverbs Max'
    column_name = 'adverbs_max'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adverbs = [filter(pos_tagger.tagset.is_adverb, i) for i in sents]
        adverbs = [len(list(i)) for i in adverbs]

        result = [adverbs[i] / sents_count[i] for i in range(len(adverbs))]
        return np.array(result).max()


class AdverbsStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: adverbs standard deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre advérbios e a quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados advérbios as palavras anotadas
        com as etiquetas ADV e PDEN pelo POS tagger nlpnet. Há também a etiqueta de contrações de preposições com
        advérbios: PREP+ADV.

        **Forma de cálculo da métrica**: Calcula-se a proporção de advérbios por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os advérbios

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, com 0, 1, 0, 1 e 0 advérbios (o nlpnet não reconheceu
        “só” como advérbio). Proporções: 0/15 = 0; 1/12 = 0,083; 0/12 = 0; 1/15 = 0,067; 0/8 = 0

        **Resultado Esperado**: 0,037

        **Resultado Obtido**: 0,037

        **Status**: correto
    """

    name = 'Adverbs Standard Deviation'
    column_name = 'adverbs_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adverbs = [filter(pos_tagger.tagset.is_adverb, i) for i in sents]
        adverbs = [len(list(i)) for i in adverbs]

        result = [adverbs[i] / sents_count[i] for i in range(len(adverbs))]
        return np.array(result).std()


class AdverbDiversity(base.Metric):
    """
        **Nome da Métrica**: adverbs_diversity_ratio

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de advérbios em relação à quantidade de tokens de advérbios no
        texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados advérbios as palavras anotadas
        com as etiquetas ADV e PREP+ADV ou PDEN pelo POS tagger nlpnet

        **Forma de cálculo da métrica**: divide-se a quantidade de advérbios diferentes (sem repetição) pela quantidade
        total de advérbios no texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Os direitos existem para que cada um de nós tenha uma vida digna e decente, ainda que nem sempre eles
        sejam respeitados. Como cidadão, todo ser humano já nasce com uma série de direitos: direito à vida, ao
        trabalho, à liberdade. Também as crianças têm direitos só para elas, assim como os consumidores, e até mesmo os
        animais. Ser cidadão também é bater o pé para que os direitos não sejam só leis no papel.

        **Contagens**: 10 advérbios (nem, sempre, já, também, só, até, mesmo, também, não, só) 8 sem repetições

        **Resultado Esperado**: 8/10 = 0,80

        **Resultado Obtido**: 0,80

        **Status**: correto
    """

    name = 'Adverbs Diversity'
    column_name = 'adverbs_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        adverbs = [i[0].lower() for i in rp.tagged_words(t)
                   if pos_tagger.tagset.is_adverb(i)
                   or pos_tagger.tagset.is_denotative_word(i)]
        # unique = len(set(adverbs))
        try:
            return rp.mattr(adverbs)
            # return unique / len(adverbs)
        except ZeroDivisionError:
            return 0


class AdjectivesMin(base.Metric):
    """
        **Nome da Métrica**: adjectives min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção mínima de adjetivos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados adjetivos as palavras anotadas
        com as etiquetas ADJ pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de adjetivos por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
         identificar os adjetivos

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 5, 1 e 1 adjetivos, respectivamente. O nlpnet
        não reconheceu “Fundamental” e “Médio” como adjetivos, porque estão grafados com inicial maiúscula, por isso a
        primeira sentença ficou com 3 adjetivos. Proporções: 3/30 = 0,1, 1/21 = 0,048, 1/18 = 0,056.

        **Resultado Esperado**: 1/21 = 0,048

        **Resultado Obtido**: 0,048

        **Status**: correto
    """

    name = 'Adjectives Min'
    column_name = 'adjectives_min'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adjectives = [filter(pos_tagger.tagset.is_adjective, i) for i in sents]
        adjectives = [len(list(i)) for i in adjectives]

        result = [adjectives[i] / sents_count[i] for i in range(len(adjectives))]
        return np.array(result).min()


class AdjectivesMax(base.Metric):
    """
        **Nome da Métrica**: adjectives max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção máxima de adjetivos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados adjetivos as palavras anotadas
        com as etiquetas ADJ pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de adjetivos por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a maior proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os adjetivos

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 5, 1 e 1 adjetivos, respectivamente. O nlpnet
         não reconheceu “Fundamental” e “Médio” como adjetivos, porque estão grafados com inicial maiúscula, por isso a
          primeira sentença ficou com 3 adjetivos. Proporções: 3/30 = 0,1, 1/21 = 0,048, 1/18 = 0,056.

        **Resultado Esperado**: 0,1

        **Resultado Obtido**: 0,1

        **Status**: correto
    """

    name = 'Adjectives Max'
    column_name = 'adjectives_max'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adjectives = [filter(pos_tagger.tagset.is_adjective, i) for i in sents]
        adjectives = [len(list(i)) for i in adjectives]

        result = [adjectives[i] / sents_count[i] for i in range(len(adjectives))]
        return np.array(result).max()


class AdjectivesStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: adjectives standard deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre adjetivos e a quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados adjetivos as palavras anotadas
        com as etiquetas ADJ pelo POS tagger nlpnet. Desvio-padrão é o quanto as medidas variam em relação à média.

        **Forma de cálculo da métrica**: Calcula-se a proporção de adjetivos por quantidade de palavras para cada
        sentença. Em seguida, calcula-se o desvio-padrão das proporções obtidas.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os adjetivos

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 5, 1 e 1 adjetivos, respectivamente. O nlpnet
        não reconheceu “Fundamental” e “Médio” como adjetivos, porque estão grafados com inicial maiúscula, por isso a
        primeira sentença ficou com 3 adjetivos. Proporções: 3/30 = 0,1, 1/21 = 0,048, 1/18 = 0,056.

        **Resultado Esperado**: 0,023

        **Resultado Obtido**: 0,023

        **Status**: correto
    """

    name = 'Adjectives Standard Deviation'
    column_name = 'adjectives_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        adjectives = [filter(pos_tagger.tagset.is_adjective, i) for i in sents]
        adjectives = [len(list(i)) for i in adjectives]

        result = [adjectives[i] / sents_count[i] for i in range(len(adjectives))]
        return np.array(result).std()


class AdjectiveDiversity(base.Metric):
    """
        **Nome da Métrica**: adjective_diversity_ratio

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de adjetivos em relação à quantidade de tokens de adjetivos no
        texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados adjetivos as palavras anotadas
        com as etiquetas ADJ pelo POS tagger nlpnet

        **Forma de cálculo da métrica**: divide-se a quantidade de adjetivos diferentes (sem repetição) pela quantidade
        total de adjetivos no texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Os direitos existem para que cada um de nós tenha uma vida digna e decente, ainda que nem sempre eles
        sejam respeitados. Como cidadão, todo ser humano já nasce com uma série de direitos: direito à vida, ao trabalho,
        à liberdade. Também as crianças têm direitos só para elas, assim como os consumidores, e até mesmo os animais.
        Ser cidadão também é bater o pé para que os direitos não sejam só leis no papel.

        **Contagens**: 2 adjetivos (digna, decente) 2 sem repetições

        **Resultado Esperado**: 2/2 = 1

        **Resultado Obtido**: 1

        **Status**: correto
    """

    name = 'Adjective Diversity'
    column_name = 'adjective_diversity_ratio'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        adjectives = [i[0].lower() for i in adjectives]
        # unique = len(set(adjectives))
        try:
            return rp.mattr(adjectives)
            # return unique / len(adjectives)
        except ZeroDivisionError:
            return 0


class NounsMin(base.Metric):
    """
        **Nome da Métrica**: nouns min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção mínima de substantivos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas substantivos as palavras
        anotadas com as etiquetas N e NPROP pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de substantivos por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os substantivos.

        **Limitações da métrica**:

        **Crítica**: ao analisarmos o resultado desta métrica nos três níveis de complexidade do corpus PorSimples, não
        foi identificada uma tendência que correlacione a quantidade de substantivos à complexidade textual

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 11, 8 e 7 substantivos respectivamente. O
        nlpnet reconheceu os adjetivos “Fundamental” e “Médio” como nomes próprios, por estarem grafados com inicial
        maiúscula, por isso a primeira sentença ficou com 13 substantivos.
        Proporções: 13/30 = 0,433; 8/21 = 0,381; 7/18 = 0,388

        **Resultado Esperado**: 0,023

        **Resultado Obtido**: 0,023

        **Status**: correto

    """

    name = 'Nouns Min'
    column_name = 'nouns_min'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        nouns = [filter(pos_tagger.tagset.is_noun, i) for i in sents]
        nouns = [len(list(i)) for i in nouns]

        result = [nouns[i] / sents_count[i] for i in range(len(nouns))]
        return np.array(result).min()


class NounsMax(base.Metric):
    """
        **Nome da Métrica**: nouns max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção máxima de substantivos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas substantivos as palavras
        anotadas com as etiquetas N e NPROP pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de substantivos por quantidade de palavras para cada
        sentença. Classificam-se os resultados e identifica-se a maior proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os substantivos.

        **Limitações da métrica**:

        **Crítica**: ao analisarmos o resultado desta métrica nos três níveis de complexidade do corpus PorSimples, não
        foi identificada uma tendência que correlacione a quantidade de substantivos à complexidade textual

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 12, 8 e 7 substantivos respectivamente. O
        nlpnet reconheceu os adjetivos “Fundamental” e “Médio” como nomes próprios, por estarem grafados com inicial
        maiúscula, por isso a primeira sentença ficou com 13 substantivos.
        Proporções: 13/30 = 0,433; 8/21 = 0,381; 7/18 = 0,388

        **Resultado Esperado**: 0,381

        **Resultado Obtido**: 0,381

        **Status**: correto

    """

    name = 'Nouns Max'
    column_name = 'nouns_max'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        nouns = [filter(pos_tagger.tagset.is_noun, i) for i in sents]
        nouns = [len(list(i)) for i in nouns]

        result = [nouns[i] / sents_count[i] for i in range(len(nouns))]
        return np.array(result).max()


class NounsStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: nouns standard deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre substantivos e a quantidade de palavras das
        sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas substantivos as palavras
        anotadas com as etiquetas N e NPROP pelo POS tagger nlpnet. Desvio-padrão é o quanto as medidas variam em
        relação à média.

        **Forma de cálculo da métrica**: Calcula-se a proporção de substantivos por quantidade de palavras para cada
        sentença. Em seguida, calcula-se o desvio-padrão das proporções obtidas.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os substantivos.

        **Limitações da métrica**:

        **Crítica**: ao analisarmos o resultado desta métrica nos três níveis de complexidade do corpus PorSimples, não
        foi identificada uma tendência que correlacione a quantidade de substantivos à complexidade textual

        **Projeto**: GUTEN

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças de 30, 21 e 18 palavras, e um total de 13, 8 e 7 substantivos respectivamente. O
        nlpnet reconheceu os adjetivos “Fundamental” e “Médio” como nomes próprios, por estarem grafados com inicial
        maiúscula. Proporções; 13/30 = 0,433, 8/21 = 0,381, 7/18 = 0,388.

        **Resultado Esperado**: 0,023

        **Resultado Obtido**: 0,023

        **Status**: correto
    """

    name = 'Nouns Standard Deviation'
    column_name = 'nouns_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        nouns = [filter(pos_tagger.tagset.is_noun, i) for i in sents]
        nouns = [len(list(i)) for i in nouns]

        result = [nouns[i] / sents_count[i] for i in range(len(nouns))]
        return np.array(result).std()


class NounDiversity(base.Metric):
    """
        **Nome da Métrica**: noun diversity

        **Interpretação**: quanto maior métrica, maior a complexidade, pois a repetição de substantivos é uma das
        formas mais simples de construir cadeias de correferência.

        **Descrição da métrica**: Proporção de types de substantivos em relação à quantidade de tokens de substantivos
        no texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados substantivos as palavras
        anotadas com as etiquetas N e NPROP pelo POS tagger nlpnet

        **Forma de cálculo da métrica**: divide-se a quantidade de substantivos diferentes (sem repetição) pela
        quantidade total de substantivos no texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Os direitos existem para que cada um de nós tenha uma vida digna e decente, ainda que nem sempre eles
        sejam respeitados. Como cidadão, todo ser humano já nasce com uma série de direitos: direito à vida, ao
        trabalho, à liberdade. Também as crianças têm direitos só para elas, assim como os consumidores, e até mesmo os
        animais. Ser cidadão também é bater o pé para que os direitos não sejam só leis no papel.

        **Contagens**: 20 substantivos (direitos, vida, cidadão, ser, humano, série, direitos, direito, vida, trabalho,
        liberdade, crianças, direitos, consumidores, animais, cidadão, pé, direitos, leis, papel) 15 sem repetições

        **Resultado Esperado**: 15/20 = 0,75

        **Resultado Obtido**: 0,737 (o nlpnet não reconheceu “ser”, de “ser humano”, como substantivo)

        **Status**: correto
    """

    name = 'Noun Diversity Ratio'
    column_name = 'noun_diversity'

    def value_for_text(self, t, rp=default_rp):
        nouns = filter(pos_tagger.tagset.is_noun, rp.tagged_words(t))
        nouns = [i[0].lower() for i in nouns]
        # unique = len(set(nouns))
        try:
            return rp.mattr(nouns)
            # return unique / len(nouns)
        except ZeroDivisionError:
            return 0


class VerbsMin(base.Metric):
    """
        **Nome da Métrica**: verbs min

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção mínima de verbos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados verbos as palavras anotadas com
        a etiqueta V pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de verbos por quantidade de palavras para cada sentença.
        Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os verbos

        **Limitações da métrica**:

        **Crítica**: não há razão para os verbos auxiliares e no particípio (VAUX e PCP) não serem computados na métrica

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
         amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 2, 2, 2, 2 e 1 verbos, respectivamente.
        Proporções: 0,133, 0,167, 0,167, 0,133 e 0,125

        **Resultado Esperado**: 0,125

        **Resultado Obtido**: 0,125

        **Status**: correto

    """

    name = 'Verbs Min'
    column_name = 'verbs_min'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        verbs = [filter(pos_tagger.tagset.is_verb, i) for i in sents]
        verbs = [len(list(i)) for i in verbs]

        result = [verbs[i] / sents_count[i] for i in range(len(verbs))]
        return np.array(result).min()


class VerbsMax(base.Metric):
    """
        **Nome da Métrica**: verbs max

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção máxima de verbos em relação à quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados verbos as palavras anotadas com
        a etiqueta V pelo POS tagger nlpnet. Não são considerados os auxiliares e os verbos em forma de particípio
        (VAUX e PCP).

        **Forma de cálculo da métrica**: Calcula-se a proporção de verbos por quantidade de palavras para cada sentença.
        Classificam-se os resultados e identifica-se a menor proporção.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os verbos

        **Limitações da métrica**:

        **Crítica**: não há razão para os verbos auxiliares e no particípio não serem computados na métrica

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 2, 2, 2, 2 e 1 verbos, respectivamente.
        Proporções: 0,133, 0,167, 0,167, 0,133 e 0,125

        **Resultado Esperado**: 0,167

        **Resultado Obtido**: 0,167

        **Status**: correto
    """

    name = 'Verbs Max'
    column_name = 'verbs_max'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        verbs = [filter(pos_tagger.tagset.is_verb, i) for i in sents]
        verbs = [len(list(i)) for i in verbs]

        result = [verbs[i] / sents_count[i] for i in range(len(verbs))]
        return np.array(result).max()


class VerbsStandardDeviation(base.Metric):
    """
        **Nome da Métrica**: verbs standard deviation

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Desvio padrão das proporções entre verbos e a quantidade de palavras das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: são considerados verbos as palavras anotadas com
        a etiqueta V pelo POS tagger nlpnet.

        **Forma de cálculo da métrica**: Calcula-se a proporção de verbos por quantidade de palavras para cada sentença.
        Depois, calcula-se o desvio-padrão das proporções obtidas.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os verbos

        **Limitações da métrica**:

        **Crítica**: não há razão para os verbos auxiliares e no particípio (VAUX e PCP) não serem computados na métrica

        **Projeto**: GUTEN

        **Teste**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme vive
        no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes humanas.
        Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também conhecida como
        amarelão.

        **Contagens**: 5 sentenças de 15, 12, 12, 15 e 8 palavras, e um total de 2, 2, 2, 2 e 1 verbos, respectivamente.
        Proporções: 0,133, 0,167, 0,167, 0,133 e 0,125

        **Resultado Esperado**: 0,018

        **Resultado Obtido**: 0,018

        **Status**: correto
    """

    name = 'Verbs Standard Deviation'
    column_name = 'verbs_standard_deviation'

    def value_for_text(self, t, rp=default_rp):
        sents = [list(filterfalse(pos_tagger.tagset.is_punctuation,
                                  i)) for i in rp.tagged_sentences(t)]
        sents_count = [len(i) for i in sents]
        verbs = [filter(pos_tagger.tagset.is_verb, i) for i in sents]
        verbs = [len(list(i)) for i in verbs]

        result = [verbs[i] / sents_count[i] for i in range(len(verbs))]
        return np.array(result).std()


class VerbDiversity(base.Metric):
    """
        **Nome da Métrica**: verb diversity

        **Interpretação**: não está clara a relação da métrica com a complexidade textual, mas supõe-se que, quanto
        maior métrica, maior a complexidade.

        **Descrição da métrica**: Proporção de types de verbos em relação à quantidade de tokens de verbos no texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados verbos as palavras anotadas com
        as etiquetas V, VAUX e PCP pelo POS tagger nlpnet

        **Forma de cálculo da métrica**: divide-se a quantidade de verbos diferentes (sem repetição) pela quantidade
        total de verbos no texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Tem gente que tem fome o tempo todo. Fome de brincar, fome de jogar, e até fome de conhecer as
        coisas! Para quem tem fome de saber, preparamos esse teste rápido para deixar você com água na boca.

        **Contagens**: 9 verbos, 7 sem repetições

        **Resultado Esperado**: 7/9 =0,778

        **Resultado Obtido**: 0,778

        **Status**: correto
    """

    name = 'Verb Diversity Ratio'
    column_name = 'verb_diversity'

    def value_for_text(self, t, rp=default_rp):
        verbs = [i[0].lower() for i in rp.tagged_words(t)
                 if pos_tagger.tagset.is_verb(i) or
                 pos_tagger.tagset.is_auxiliary_verb(i) or
                 pos_tagger.tagset.is_participle(i)]
        # unique = len(set(verbs))
        try:
            return rp.mattr(verbs)
            # return unique / len(verbs)
        except ZeroDivisionError:
            return 0


class DaleChall(base.Metric):
    """
        **Nome da Métrica**: dalechall adapted

        **Interpretação**: quanto maior o valor da métrica, maior a complexidade textual

        **Descrição da métrica**: a fórmula de leiturabilidade de Dalechall adaptada combina a quantidade de palavras
        não familiares com a quantidade média de palavras por sentença. A métrica tem uma equivalência com os níveis
        escolares, conforme segue (Chall, Jeanne Sternlicht; Dale, Edgar (May 1, 1995). Readability revisited. ISBN 
        1571290087):

        4,9 ou menos => nível 4 ou abaixo
        5,0 a 5,9 => níveis 5 – 6
        6,0 a 6,9 => níveis 7 – 8
        7,0 a 7,9 => níveis 9 – 10
        8,0 a 8,9 => níveis 11 – 12
        9,0 a 9,9 => níveis 13 – 15 (universitários)
        10 ou mais => nível 16 ou acima (graduados)

        **Definição dos termos que aparecem na descrição da métrica**: palavras não familiares são aquelas que não
        constam do vocabulário básico conhecido por alunos do quarto ano. Para fins desta métrica, foram utilizadas as
        entradas do dicionário Biderman de palavras simples.

        **Forma de cálculo da métrica**: primeiro conta-se a quantidade de palavras de cada sentença, somam se as
        quantidades e divide-se o resultado pela quantidade de sentenças do texto, para encontrar a média de palavras
        por sentença; depois buscam-se todas as palavras do texto na lista de palavras simples e conta-se 1 a cada
        palavra não encontrada na lista (o contador representa as palavras não familiares). Finalmente, usa-se a fórmula
        a seguir para calcular a métrica:

        (0.1579 * percentual de palavras não familiares) + (0.0496 * quantidade média de palavras por sentença) + 3.6365

        **Projeto**: GUTEN

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora do
        Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 38 palavras, 2 sentenças, média de 19 palavras por sentença, 19 palavras não contidas na lista de
        palavras simples.

        Temos 50% de palavras fora da lista de palavras simples

        **Resultado Esperado**: (0.1579 * 0,5) + (0.0496 * 19) + 3.6365 = 4,658 (0,079+0,94+3,6365)

        **Resultado Obtido**: 4,658

        **Status**: correto

    """

    name = 'DaleChall'
    column_name = 'dalechall_adapted'

    def value_for_text(self, t, rp=default_rp):
        sw = rp.simple_words()
        words = rp.lower_words(t)
        word_lemmas = [rp.stemmer().get_lemma(word) for word in words]
        count = sum(1 for word in word_lemmas if word not in sw)
        unfamiliar_words = count / len(words) * 100
        sentences = rp.sentences(t)
        words_sentence = len(words) / len(sentences)

        ret = (0.1579 * unfamiliar_words) + (0.0496 * words_sentence)
        if unfamiliar_words > 5:
            ret += 3.6365

        return ret


class GunningFog(base.Metric):
    """
        **Nome da Métrica**: gunning fox

        **Interpretação**: quanto maior a métrica, maior a complexidade

        **Descrição da métrica**: Índice Gunning Fox de leiturabilidade

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: O índice Gunning Fox de leiturabilidade calcula a média de palavras por
        sentença do texto, soma o percentual de palavras com 3 ou mais sílabas no texto e multiplica o resultado por
        0,4.

        **Recursos de PLN utilizados durante o cálculo**: sentenciador, tokenizador e separador de sílabas

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério – justifica a diretora
        do Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 19 palavras com 3 ou mais sílabas em 38 palavras e 2 sentenças

        **Resultado Esperado**: (38/2 + 19/38) x 0,4 => 19,5 x 0,4 = 7,8

        **Resultado Obtido**: 7,8

        **Status**: correto
    """

    name = 'Gunning Fox'
    column_name = 'gunning_fox'

    def value_for_text(self, t, rp=default_rp):
        words = rp.tagged_words(t)
        sentences = rp.sentences(t)
        syllables = list(map(syllable_separator.separate, rp.all_words(t)))
        complex_words = [i for i in syllables if len(i) >= 3]
        average_words = len(words) / ilen(sentences)
        percentage_complex = len(complex_words) / len(words)
        return 0.4 * (average_words + percentage_complex)


class ContentDensity(base.Metric):
    """
        **Nome da Métrica**: content density

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção média de palavras de conteúdo em relação à quantidade de palavras funcionais
        das sentenças

        **Definição dos termos que aparecem na descrição da métrica**: Palavras de conteúdo são palavras de classe
        aberta (substantivos, adjetivos, verbos e advérbios). Palavras funcionais são palavras das classes fechadas
        (numerais, artigos, pronomes, interjeições, preposições, conjunções)

        **Forma de cálculo da métrica**: somam-se as ocorrências de palavras de conteúdo de cada sentença e divide-se o
        resultado pela quantidade de palavras funcionais da respectiva sentença. Depois somam-se as proporções de todas
        as sentenças e divide-se pela quantidade de sentenças.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: a rigor, somente os advérbios terminados em –mente são palavras de conteúdo. Mas como
        as etiquetas não fazem essa diferença, estão sendo computados todos os advérbios. O resultado da métrica é
        dependente da forma de tokenização adotada (com ou sem descontração, com ou sem junção de partes de nomes
        próprios e multipalavras).

        **Crítica**:

        A métrica faz a tokenização sem considerar descontrações. A descontração é importante para o cômputo de palavras
        funcionais. Se houver descontração, cada parte da contração é contada em uma categoria; porém, se não houver,
        uma das categorias gramaticais envolvidas ficará prejudicada.

        **Projeto**: GUTEN

        **Teste**: Atenção! Nós não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos
        suficientes para a manutenção das quatro escolas, por exemplo, e também precisamos valorizar o magistério -
        justifica a diretora do Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**:

        28 Palavras de conteúdo: [('Atenção', 'N'), ('não', 'ADV'), ('podemos', 'V'), ('acrescentar', 'V'),
        ('despesa', 'N'), ('a', 'ADV'), ('mais', 'ADV'), ('orçamento', 'N'), ('Já', 'ADV'), ('não', 'ADV'),
        ('temos', 'V'), ('recursos', 'N'), ('suficientes', 'ADJ'), ('manutenção', 'N'), ('escolas', 'N'),
        ('por', 'PDEN'), ('exemplo', 'PDEN'), ('também', 'PDEN'), ('precisamos', 'V'), ('valorizar', 'V'),
        ('magistério', 'N'), ('justifica', 'V'), ('diretora', 'N'), ('Departamento', 'N'), ('Pedagógico', 'ADJ'),
        ('SEC', 'NPROP'), ('Sonia', 'NPROP'), ('Balzano', 'NPROP')]

        13 Palavras funcionais: [('Nós', 'PROPESS'), ('nenhuma', 'PROADJ'), ('no', 'PREP+ART'), ('nosso', 'PROADJ'),
        ('para', 'PREP'), ('a', 'ART'), ('das', 'PREP+ART'), ('quatro', 'NUM'), ('e', 'KC'), ('o', 'ART'), ('a', 'ART'),
        ('do', 'PREP+ART'), ('da', 'PREP+ART')]

        **Resultado Esperado**: 28/13 = 2,15

        **Resultado Obtido**: 2,15

        **Status**: correto
    """

    name = 'Content Words per Funcional Words'
    column_name = 'content_density'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        return ilen(content_words) / ilen(function_words)


class NamedEntitiesRatioText(base.Metric):
    """
        **Nome da Métrica**: named_entity_ratio_text

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção de Nomes Próprios em relação à quantidade de palavras do Texto

        **Definição dos termos que aparecem na descrição da métrica**: nomes próprios são palavras escritas em letra
        maiúscula, compostos de um ou mais tokens, capturadas por meio da etiqueta morfossintática PROP do parser
        Palavras. A etiqueta PROP junta todos os tokens de um mesmo nome próprio em uma multipalavra.

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta PROP e divide-se o resultado pela
        quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: é importante para essa métrica usar a opção de junção de palavras que compõem os
        nomes próprios, disponível no parser Palavras; caso contrário, corre-se o risco de contar cada token do nome
        próprio como uma entidade nomeada diferente.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: O melhor amigo do João é o Jorge Campos, que trabalha na Siemens. Eles se conheceram no Palestra
        Itália, num dia de decisão entre Palmeiras e São Paulo.

        **Contagens**: 28 palavras, 6 nomes próprios: João, Jorge Campos, Siemens, Palestra Itália, Palmeiras, São Paulo

        **Resultado Esperado**: 6/29 = 0,207

        **Resultado Obtido**: 0,207

        **Status**: correto
    """

    name = 'Named Entity Ratio on Text'
    column_name = 'named_entity_ratio_text'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            occurances = re.findall(' PROP ', flat)
            repeated = re.findall(' PROP .* PROP ', flat)  # Palavras bug
            elements = [i for i in flat.split('\n') if len(i) > 10]
            return (len(occurances) - len(repeated)) / len(elements)
        except ZeroDivisionError:
            return 0


class NamedEntitiesRatioSentence(base.Metric):
    """
        **Nome da Métrica**: named_entity_ratio_sentence

        **Interpretação**: segundo hipotetizado por Feng et al., 2010* (A Comparison of Features for Automatic
        Readability Assessment), quanto maior a quantidade de entidades mencionadas, maior a carga de memória requerida
        e, portanto, maior a complexidade textual. 

        **Descrição da métrica**: Média das proporções de nomes próprios em relação à quantidade de palavras das
        Sentenças

        **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
        como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
        reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nessa métrica só
        estão sendo reconhecidas as entidades nomeadas que possuem nome próprio em letra maiúscula, capturadas por meio
        da etiqueta morfossintática PROP do parser Palavras.

        **Forma de cálculo da métrica**: contam-se as ocorrências da etiqueta PROP em cada sentença e divide-se o
        resultado pela quantidade de palavras da sentença (proporção de entidades nomeadas por quantidade de palavras
        das sentenças). Depois somam-se todas as proporções calculadas e divide-se o resultado pelo número de sentenças,
        para obter a média das proporções.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Romero Jucá já disse que presidente deve vetar trecho sobre PIS-Cofins.

        **Contagens**: 10 palavras, 2 PROP (Romero=Jucá  e PIS-Cofins)

        **Resultado Esperado**: 0,20

        **Resultado Obtido**: 0,20

        **Status**: correto
    """

    name = 'Named Entity Ratio on Sentences'
    column_name = 'named_entity_ratio_sentence'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        sentences = flat.split('</s>')[:-2]
        results = []
        for sentence in sentences:
            occurances = re.findall(' PROP ', sentence)
            repeated = re.findall(' PROP .* PROP ', sentence)   # Palavras bug
            elements = [i for i in sentence.split('\n') if len(i) > 10]
            try:
                results.append((len(occurances) - len(repeated)) / len(elements))
            except ZeroDivisionError:
                results.append(0)
        try:
            return sum(results) / len(results)
        except ZeroDivisionError:
            return 0


# class HumanNamedEntitiesRatioText(base.Metric):
#     """
#         **Nome da Métrica**: human_named_entity_ratio_text
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de Entidades Nomeadas Humanas em relação à quantidade de palavras do texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica só
#         estão sendo reconhecidas as entidades nomeadas que têm nome próprio em letra maiúscula (PROP) e que sejam
#         humanas, ou seja, que apresentem também a etiqueta semântica <hum> do parser Palavras.
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências conjuntas das etiquetas PROP e <hum> no texto e
#         divide-se o resultado pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: já existe uma métrica que engloba essa (named_entity_ratio_text), que tem mais correlação com
#         complexidade textual. Por esse motivo, esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Human Named Entity Ratio on Text'
#     column_name = 'human_named_entity_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             occurances = re.findall('<hum>.* PROP ', flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class HumanNamedEntitiesRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: human_named_entity_ratio_sentence
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: média das proporções de Entidades Nomeadas Humanas nas sentenças em relação à
#         quantidade de palavras das Sentenças
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica só
#         estão sendo reconhecidas as entidades nomeadas que têm nome próprio em letra maiúscula (PROP) e que sejam
#         humanas, ou seja, que apresentem também a etiqueta semântica <hum> do parser Palavras. A métrica de entidades
#         nomeadas geral faz mais sentido para aferir complexidade textual.
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências conjuntas das etiquetas PROP e <hum> em cada sentença
#         e divide-se o resultado pela quantidade de palavras da sentença (proporção de entidades nomeadas humanas por
#         quantidade de palavras nas sentenças). Depois somam-se todas as proporções calculadas e divide-se o resultado
#         pelo número de sentenças, para obter a média das proporções.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: já existe uma métrica que engloba essa (named_entity_ratio_sentence), que tem mais correlação com
#         complexidade textual. Por esse motivo, esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Human Named Entity Ratio on Sentences'
#     column_name = 'human_named_entity_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             occurances = re.findall('<hum>.* PROP ', sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


# class NonHumanAnimateMovingNamedEntitiesRatioText(base.Metric):
#     """
#         **Nome da Métrica**: non-human_animate_moving_named_entity_ratio_text
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de Entidades Nomeadas Não Humanas Animadas que se Movem em relação à
#         quantidade de palavras do Texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica estão
#         sendo reconhecidas como entidades nomeadas não humanas, animadas, que se movem, 7 etiquetas semânticas de
#         “animal prototypes” do parser Palavras ou seja, <Adom> (animal doméstico ou grande mamífero), <Amyth> (animal
#         mitológico), <Azo> (animal terrestre), <Aorn> (pássaro), <Acell> (animal celular ou célula do sangue), <Aich>
#         (animal aquático), <Aent> (inseto).
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas de animais no texto e divide-se o
#         resultado pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**:
#
#         As palavras buscadas não se enquadram na descrição de entidades nomeadas;
#
#         O parser Palavras tem uma categoria de etiquetas semânticas exclusiva para entidades nomeadas, mas as etiquetas
#         eleitas para esta métrica não fazem parte dessa categoria;
#
#         Se a categoria semântica de onde foram extraídas as etiquetas se chama “animal prototypes”, qual o sentido de
#         renomear o conceito para “entidades nomeadas não humanas animadas com movimento? REVER conceito da métrica.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Non-Human Animate Moving Named Entity Ratio on Text'
#     column_name = 'non-human_animate_moving_named_entity_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             expression = re.compile('''
#                                     <Amyth>|    # Mitológico
#                                     <Acell>|    # Bactéria
#                                     <Adom>|     # Mamíferos
#                                     <Azo>|      # Pássaros
#                                     <Aorn>|     # Pássaros
#                                     <Aent>|     # Insetos
#                                     <Aich>      # Peixes
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class NonHumanAnimateMovingNamedEntitiesRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: non-human_animate_moving_named_entity_ratio_sentence
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: média das proporções de Entidades Nomeadas Não Humanas Animadas que se Movem em
#         relação à quantidade de palavras nas sentenças
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica estão
#         sendo reconhecidas como entidades nomeadas não humanas, animadas, que se movem, 7 etiquetas semânticas de
#         “animal prototypes” do parser Palavras ou seja, <Adom> (animal doméstico ou grande mamífero), <Amyth> (animal
#         mitológico), <Azo> (animal terrestre), <Aorn> (pássaro), <Acell> (animal celular ou célula do sangue), <Aich>
#         (animal aquático), <Aent> (inseto).
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas de animais em cada sentença e divide-se
#         o resultado pela quantidade de palavras da sentença. Depois somam-se todas as proporções calculadas e divide-se
#         o resultado pelo número de sentenças, para obter a média das proporções.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**:
#
#         As palavras buscadas não se enquadram na descrição de entidades nomeadas.
#
#         O parser Palavras tem uma categoria de etiquetas semânticas exclusiva para entidades nomeadas, mas as etiquetas
#         eleitas para esta métrica não fazem parte dessa categoria.
#
#         Se a categoria semântica de onde foram extraídas as etiquetas se chama “animal prototypes”, qual o sentido de
#         renomear o conceito para “entidades nomeadas não humanas animadas com movimento?
#
#         Por esses motivos, esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Non-Human Animate Moving Named Entity Ratio on Sentences'
#     column_name = 'non-human_animate_moving_named_entity_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             expression = re.compile('''
#                                     <Amyth>|    # Mitológico
#                                     <Acell>|    # Bactéria
#                                     <Adom>|     # Mamíferos
#                                     <Azo>|      # Pássaros
#                                     <Aorn>|     # Pássaros
#                                     <Aent>|     # Insetos
#                                     <Aich>      # Peixes
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


# class NonHumanAnimateNonMovingNamedEntitiesRatioText(base.Metric):
#     """
#         **Nome da Métrica**: non-human_animate_non-moving_named_entity_ratio_text
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de Entidades Nomeadas Não Humanas Animadas que não se Movem em relação à
#         quantidade de palavras do Texto
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica estão
#         sendo reconhecidas como entidades nomeadas não humanas, animadas, que não se movem, apenas 1 das 5 etiquetas da
#         categoria semântica “plant prototypes” do parser Palavras ou seja, <Btree> (árvore)
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências da etiquetas <Btree> no texto e divide-se o resultado
#         pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: As palavras buscadas não se enquadram na descrição de entidades nomeadas.
#
#         O parser Palavras tem uma categoria de etiquetas semânticas exclusiva para entidades nomeadas, mas a etiqueta
#         eleita para esta métrica não faz parte dessa categoria.
#
#         Se a categoria semântica de onde foram extraídas as etiquetas se chama “plant prototypes”, qual o sentido de
#         renomear o conceito para “entidades nomeadas não humanas animadas sem movimento”?
#
#         O traço +animado é usado em semântica para descrever aquilo que tem movimento e, portanto, “animadas sem
#         movimento” é uma definição que traz o traço repetido com informações contrárias (que se move e que não se move),
#         o que é ilógico.
#
#         Por esses motivos, esta métrica deve ser comentada.
#     """
#
#     name = 'Non-Human Animate Non-Moving Named Entity Ratio on Text'
#     column_name = 'non-human_animate_non-moving_named_entity_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             expression = '<Btree>'
#             # 'Árvores'
#             occurances = re.findall(expression, flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class NonHumanAnimateNonMovingNamedEntitiesRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: non-human_animate_non-moving_named_entity_ratio_sentence
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: média das proporções de Entidades Nomeadas Não Humanas Animadas que não se Movem em
#         relação à quantidade de palavras nas sentenças
#
#         **Definição dos termos que aparecem na descrição da métrica**: entidade nomeada é uma entidade do mundo real,
#         como pessoas, lugares, datas, organizações, produtos, etc. que pode ser denotada por meio de um nome. O
#         reconhecimento de entidades nomeadas é uma subtarefa do processamento de línguas naturais. Nesta métrica estão
#         sendo reconhecidas como entidades nomeadas não humanas, animadas, que não se movem, apenas 1 das 5 etiquetas da
#         categoria semântica “plant prototypes” do parser Palavras ou seja, <Btree> (árvore)
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências da etiqueta <Btree> em cada sentença e divide-se o
#         resultado pela quantidade de palavras da sentença. Depois somam-se todas as proporções calculadas e divide-se
#         o resultado pelo número de sentenças, para obter a média das proporções.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: As palavras buscadas não se enquadram na descrição de entidades nomeadas. O parser Palavras tem
#         uma categoria de etiquetas semânticas exclusiva para entidades nomeadas, mas a etiqueta eleita para esta métrica
#         não faz parte dessa categoria. Se a categoria semântica de onde foram extraídas as etiquetas se chama “plant
#         prototypes”, qual o sentido de renomear o conceito para “entidades nomeadas não humanas animadas sem movimento”?
#
#         O traço +animado é usado em semântica para descrever aquilo que tem movimento e, portanto, “animadas sem
#         movimento” é uma definição que traz o traço repetido com informações contrárias (que se move e que não se move),
#         o que é ilógico.
#
#         Por esses motivos, esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Non-Human Animate Non-Moving Named Entity Ratio on Sentences'
#     column_name = 'non-human_animate_non-moving_named_entity_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             expression = '<Btree>'
#             # 'Árvores'
#             occurances = re.findall(expression, sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


# class TopologicalsRatioText(base.Metric):
#     """
#         **Nome da Métrica**: topological_ratio_text
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Proporção de Topônimos em relação à quantidade de palavras do texto Definição dos
#         termos que aparecem na descrição da métrica: topônimo é “nome de lugar”, como por exemplo: Morro de São Paulo.
#         Nesta métrica são usadas etiquetas semânticas para capturar os mais diversos tipos de lugares: <Lwater>(lugar de
#         água: rio, lago, mar, etc); <Ltop> (lugar natural: pântano, promontório, etc); <Lpath> (caminho: rodovia, rua,
#         pista, etc); <Lciv> (local: cidade, estado, país, etc); <Ltrap> (armadilha); <L[a-z]*> (todas as etiquetas de
#         locais); <L> (local, hiperônimo de todas as etiquetas iniciadas por L) <inst> (instituição: auto-escola, teatro,
#         escola, etc); <furn>(mobília: cadeira, cama, quadro, etc.); <BB> (grupo de plantas).
#
#         **Forma de cálculo da métrica**: Contam-se as ocorrências das etiquetas eleitas e divide-se o resultado pela
#         quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: Um tipo de lugar não é um topônimo. Topônimo é um lugar que tem um nome próprio.
#
#         Foram eleitas etiquetas de diferentes “prototypes” do Palavras, sem justificativa. Talvez combinando a etiqueta
#         PROP com as etiquetas de lugares seja possível capturar os lugares que têm nome. Por não ter fundamento lógico,
#         esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Ratio of Topologicals on Text'
#     column_name = 'topological_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             expression = re.compile('''
#                                     <BB>|       # Floresta
#                                     <Lwater>|   # Água
#                                     <Ltop>|     # Céu
#                                     <Lpath>|    # Caminho
#                                     <Lciv>|     # Local
#                                     <inst>|     # Instituição
#                                     <furn>|     # Mobília
#                                     <Ltrap>|    # Armadilhas
#                                     <L[a-z]*>|
#                                     <L>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class TopologicalsRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: topological_ratio_sentence
#
#         **Interpretação**: não está clara a relação da métrica com a complexidade textual
#
#         **Descrição da métrica**: Média das proporções de Topônimos em relação à quantidade de palavras nas Sentenças
#
#         **Definição dos termos que aparecem na descrição da métrica**: topônimo é “nome de lugar”, como por exemplo:
#         Morro de São Paulo. Nesta métrica são usadas etiquetas semânticas para capturar os mais diversos tipos de
#         lugares: <Lwater>(lugar de água: rio, lago, mar, etc); <Ltop> (lugar natural: pântano, promontório, etc);
#         <Lpath> (caminho: rodovia, rua, pista, etc); <Lciv> (local: cidade, estado, país, etc); <Ltrap> (armadilha);
#         <L[a-z]*> (todas as etiquetas de locais); <L> (local, hiperônimo de todas as etiquetas iniciadas por L) <inst>
#         (instituição: auto-escola, teatro, escola, etc); <furn>(mobília: cadeira, cama, quadro, etc.); <BB> (grupo de
#         plantas).
#
#         **Forma de cálculo da métrica**: Contam-se as ocorrências das etiquetas eleitas em cada sentença e divide-se o
#         resultado pela quantidade de palavras da respectiva sentença. Depois se faz uma média entre todas proporções
#         calculadas.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**:
#
#         **Crítica**: Um tipo de lugar não é um topônimo. Topônimo é um lugar que tem um nome próprio.
#
#         Foram eleitas etiquetas de diferentes “prototypes” do Palavras, sem justificativa. Talvez combinando a etiqueta
#         PROP com as etiquetas de lugares seja possível capturar os lugares que têm nome. Por não ter fundamento lógico,
#         esta métrica deve ser comentada.
#
#         **Projeto**: GUTEN
#     """
#
#     name = 'Ratio of Topologicals on Sentences'
#     column_name = 'topological_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             expression = re.compile('''
#                                     <BB>|       # Floresta
#                                     <Lwater>|   # Água
#                                     <Ltop>|     # Céu
#                                     <Lpath>|    # Caminho
#                                     <Lciv>|     # Local
#                                     <inst>|     # Instituição
#                                     <furn>|     # Mobília
#                                     <Ltrap>|    # Armadilhas
#                                     <L[a-z]*>|
#                                     <L>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


# class ConcreteMovingRatioText(base.Metric):
#     """
#         **Nome da Métrica**: concrete_moving_ratio_text
#
#         **Interpretação**: não está clara a relação entre esta métrica e a complexidade textual
#
#         **Descrição da métrica**: média das proporções de palavras concretas com movimento em relação ao número total de
#         palavras em cada sentença.
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras concretas com movimento correspondem à
#         categoria “Veículos” do parser Palavras, cujas etiquetas são são <Vwater>, <Vair>, <V[a-z]*>
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas <Vwater>, <Vair>, <V[a-z]*> e divide-se
#         o resultado pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras na função de anotação semântica
#
#         **Limitações da métrica**: o parser Palavras tem anotação semântica, mas ela não dá conta de todo o léxico
#
#         **Crítica**:
#
#             1) não está clara a motivação para distinguir objetos concretos moventes de concretos não moventes nas
#             métricas.
#
#             2) As etiquetas que representam a categoria criada com o nome de “objetos concretos com movimento” são
#             categorizadas como Veículos no parser Palavras.
#
#         **Projeto**: GUTEN
#
#         **Teste**: Ele foi de avião, porém sua mãe, que tem medo de voar, preferiu ir de trem. Além disso, as poltronas
#         do trem são bem mais espaçosas que as do avião.
#
#         **Contagens**: dois objetos concretos com movimento e 16 palavras na primeira sentença; 2 objetos concretos com
#         movimento e 17 palavras na segunda sentença, contando descontrações ou 14, sem contá-las. Total: 4 objetos,
#         30 palavras, 2 sentenças.
#
#         **Resultado Esperado**: (4/30) = 0,133 (a métrica está utilizando tokenização sem descontração)
#
#         **Resultado Obtido**: 0,10
#
#         **Status**: incorreto
#
#     """
#
#     name = 'Ratio of Concrete Moving Entitites on Text'
#     column_name = 'concrete_moving_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             expression = re.compile('''
#                                     <Vwater>|   # Navios
#                                     <Vair>|     # Aviões
#                                     <V[a-z]*>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class ConcreteMovingRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: concrete_moving_ratio_sentence
#
#         **Interpretação**: não está clara a relação entre esta métrica e a complexidade textual
#
#         **Descrição da métrica**: média por sentença da proporção de palavras concretas com movimento em relação ao
#         total de palavras
#
#         **Definição dos termos que aparecem na descrição da métrica**: palavras concretas com movimento correspondem à
#         categoria “Veículos” do parser Palavras, cujas etiquetas são são <Vwater>, <Vair>, <V[a-z]*>
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas <Vwater>, <Vair>, <V[a-z]*> e divide-se
#         o resultado pela quantidade de palavras da sentença. Depois somam-se as proporções obtidas em cada sentença e
#         divide-se o resultado pelo número de sentenças do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras na função de anotação semântica
#
#         **Limitações da métrica**: o parser Palavras tem anotação semântica, mas ela não dá conta de todo o léxico
#
#         **Crítica**:
#
#             1) não está clara a motivação para distinguir objetos concretos com movimento de concretos sem movimento nas
#             métricas.
#
#             2) As etiquetas que representam a categoria criada com o nome de “objetos concretos com movimento” são
#             categorizadas como Veículos no parser Palavras.
#
#             3) ERRO: aparentemente a métrica não está dividindo pelo número de sentenças
#
#         **Projeto**: GUTEN
#
#         **Teste**: Ele foi de avião, porém sua mãe, que tem medo de voar, preferiu ir de trem. Além disso, as poltronas
#         do trem são bem mais espaçosas que as do avião.
#
#         **Contagens**: dois objetos concretos com movimento e 16 palavras na primeira sentença; 2 objetos concretos com
#         movimento e 17 palavras na segunda sentença, contando descontrações ou 14, sem contá-las.
#
#         **Resultado Esperado**: (4/30)/2 = 0,05
#
#         **Resultado Obtido**: 0,10
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Concrete Moving Entitites on Sentences'
#     column_name = 'concrete_moving_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             expression = re.compile('''
#                                     <Vwater>|   # Navios
#                                     <Vair>|     # Aviões
#                                     <V[a-z]*>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


# class ConcreteNonMovingRatioText(base.Metric):
#     """
#         **Nome da Métrica**: concrete_non-moving_ratio_text
#
#         **Interpretação**: não está clara a relação entre esta métrica e a complexidade textual
#
#         **Descrição da métrica**: proporção de palavras concretas sem movimento em relação à quantidade de palavras do
#         texto.
#
#         **Definição dos termos que aparecem na descrição da métrica**: objetos concretos sem movimento correspondem à
#         categoria “substância” do parser Palavras, cujas etiquetas são <cm-liq>, <mat>,<cm-rem>, <cm-[a-z]*> e <cm>
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas <cm-liq>, <mat>, <cm-rem>, <cm-[a-z]*>
#         e <cm> no texto e divide-se o resultado pela quantidade de palavras do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras na função de anotação semântica
#
#         **Limitações da métrica**: o parser Palavras tem anotação semântica, mas ela não dá conta de todo o léxico
#
#         **Crítica**:
#
#             1) não está clara a motivação para distinguir concretos com movimento de concretos sem movimento nas
#             métricas.
#
#             2) As etiquetas que representam a categoria criada com o nome de “concretos sem movimento” são categorizadas
#             como “substâncias” no parser Palavras.
#
#             3) Proposta: EXCLUIR
#
#         **Projeto**: GUTEN
#
#         **Teste**: Ele foi de avião, porém sua mãe, que tem medo de voar, preferiu ir de trem. Além disso, as poltronas
#         do trem são bem mais espaçosas que as do avião.
#
#         **Contagens**: nenhum objeto concreto sem movimento e 16 palavras na primeira sentença; 1 objeto concreto sem
#         movimento e 17 palavras na segunda sentença, contando descontrações ou 14, sem contá-las. Total: 1 objeto e 30
#         palavras no texto.
#
#         **Resultado Esperado**: 1/30 = 0,033
#
#         **Resultado Obtido**: 0,033
#
#         **Status**: correto
#     """
#
#     name = 'Ratio of Concrete Non-Moving Entities on Text'
#     column_name = 'concrete_non-moving_ratio_text'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             expression = re.compile('''
#                                     <cm-liq>|       # Líquidos
#                                     <mat>|          # Materiais
#                                     <cm-rem>|       # Remédio
#                                     <cm-[a-z]*>|
#                                     <cm>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, flat)
#             elements = [i for i in flat.split('\n') if len(i) > 10]
#             return len(occurances) / len(elements)
#         except ZeroDivisionError:
#             return 0


# class ConcreteNonMovingRatioSentence(base.Metric):
#     """
#         **Nome da Métrica**: concrete_non-moving_ratio_sentence
#
#         **Interpretação**: não está clara a relação entre esta métrica e a complexidade textual
#
#         **Descrição da métrica**: média das proporções de palavras concretas sem movimento pela quantidade total de
#         palavras de cada sentença.
#
#         **Definição dos termos que aparecem na descrição da métrica**: objetos concretos sem movimento correspondem à
#         categoria “substância” do parser Palavras, cujas etiquetas são <cm-liq>, <mat>,<cm-rem>, <cm-[a-z]*> e <cm>
#
#         **Forma de cálculo da métrica**: contam-se as ocorrências das etiquetas <cm-liq>, <mat>,<cm-rem>, <cm-[a-z]*> e
#         <cm> em cada sentença e divide-se o resultado pela quantidade de palavras da sentença. Depois somam-se as
#         proporções obtidas e divide-se o resultado pelo número de sentenças do texto.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras na função de anotação semântica
#
#         **Limitações da métrica**: o parser Palavras tem anotação semântica, mas ela não dá conta de todo o léxico
#
#         **Crítica**:
#
#             1) não está clara a motivação para distinguir concretos moventes de concretos não moventes nas métricas.
#
#             2) As etiquetas que representam a categoria criada com o nome de “concretos sem movimento” são categorizadas
#             como “Substâncias” no parser Palavras.
#
#             3) ERRO: aparentemente a métrica não está dividindo pelo número de sentenças
#
#         **Projeto**: GUTEN
#
#         **Teste**: Ele foi de avião, porém sua mãe, que tem medo de voar, preferiu ir de trem. Além disso, as poltronas
#         do trem são bem mais espaçosas que as do avião.
#
#         **Contagens**: nenhum objeto concreto sem movimento e 16 palavras na primeira sentença; 1 objeto concreto sem
#         movimento e 17 palavras na segunda sentença, contando descontrações ou 14, sem contá-las.
#
#         **Resultado Esperado**: (1/30)/2 = 0,0165 (a métrica está utilizando tokenização sem descontração)
#
#         **Resultado Obtido**: 0,033
#
#         **Status**: incorreto
#     """
#
#     name = 'Ratio of Concrete Non-Moving Entities on Sentences'
#     column_name = 'concrete_non-moving_ratio_sentence'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         sentences = flat.split('</s>')[:-2]
#         results = []
#         for sentence in sentences:
#             expression = re.compile('''
#                                     <cm-liq>|       # Líquidos
#                                     <mat>|          # Materiais
#                                     <cm-rem>|       # Remédio
#                                     <cm-[a-z]*>|
#                                     <cm>
#                                     ''',
#                                     re.VERBOSE)
#             occurances = re.findall(expression, sentence)
#             elements = [i for i in sentence.split('\n') if len(i) > 10]
#             try:
#                 results.append(len(occurances) / len(elements))
#             except ZeroDivisionError:
#                 results.append(0)
#         try:
#             return sum(results) / len(results)
#         except ZeroDivisionError:
#             return 0


class PunctuationRatio(base.Metric):
    """
        **Nome da Métrica**: punctuation_ratio

        **Interpretação**: não é clara a relação entre a proporção de sinais de pontuação e complexidade textual.

        **Descrição da métrica**: proporção de sinais de pontuação em relação à quantidade de palavras.

        **Definição dos termos que aparecem na descrição da métrica**: por sinais de pontuação, entende-se: ponto final;
        vírgula, dois pontos, ponto-e-vírgula, ponto de exclamação, ponto de interrogação,  parênteses, reticências,
        travessão (. , : ; ! ? () ... _ )

        **Forma de cálculo da métrica**: Contam-se os sinais de pontuação e divide-se o resultado pela quantidade de
        palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras na função de tokenizador

        **Limitações da métrica**:

        **Crítica**: avaliar todos os sinais de pontuação conjuntamente não parece ser uma boa estratégia, pois eles
        têm diferentes impactos sobre a complexidade. Por exemplo: pontos de interrogação e exclamação estão associados
        a textos mais próximos do leitor e, portanto, mais fáceis de ler. Muitas vírgulas podem indicar textos mais
        complexos, ao passo que muitos pontos finais podem indicar textos mais simples.

        **Projeto**: GUTEN

        **Teste**:

        Trata-se de uma mudança radical: ao longo das três últimas décadas, no mínimo, o papel de arquivilão era
        atribuído à gordura saturada. No momento em que Yudkin fazia sua pesquisa, nos anos 60, uma nova ortodoxia
        nutricional se afirmava: a alimentação saudável deveria ser pobre em gordura. Yudkin liderava um grupo cada
        vez menor de dissidentes que creditava ao açúcar – e não à gordura – a causa mais provável de males como
        obesidade, doença cardíaca e diabetes.

        **Contagens**: 12 sinais de pontuação e 83 palavras (contando as 7 descontrações)

        **Resultado Esperado**: 12/83 = 0,14

        **Resultado obtido**: 0,14

        **Status**: correto
    """

    name = 'Punctuation Ratio'
    column_name = 'punctuation_ratio'

    def value_for_text(self, t, rp=default_rp):
        expression = re.compile('''
                                \\.\\.+|       # ponto final e reticências
                                [.!(),-:;?]    # Demais pontuações
                                ''',
                                re.VERBOSE)
        try:
            return len(re.findall(expression, t.raw_content)) /\
                len(rp._all_tokens(t))
        except ZeroDivisionError:
            return 0


class PunctuationDiversity(base.Metric):
    """
        **Nome da Métrica**: punctuation_diversity

        **Interpretação**: não é clara a relação entre diversidade de sinais de pontuação e complexidade textual.

        **Descrição da métrica**: Proporção de types de sinais de pontuação em relação aos tokens de sinais de pontuação
        do texto. Essa métrica presume que, dados dois textos que tenham a mesma quantidade de sinais de pontuação, o
        mais complexo é aquele que contém maior diversidade de sinais de pontuação. Instanciando: um texto com um
        parênteses, dois pontos de exclamação, 5 vírgulas e 12 pontos finais seria mais complexo que um texto com 12
        vírgulas e 8 pontos finais.

        **Definição dos termos que aparecem na descrição da métrica**: por sinais de pontuação, entende-se: ponto final;
        vírgula, dois pontos, ponto-e-vírgula, ponto de exclamação, ponto de interrogação,  parênteses, reticências,
        travessão (. , : ; ! ? () ... _ )

        **Forma de cálculo da métrica**: divide-se a quantidade de sinais de pontuação diferentes (sem repetição) pela
        quantidade total de sinais de pontuação.

        **Recursos de PLN utilizados durante o cálculo**: parser, na função de tokenizador

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste 1**:

        Trata-se de uma mudança radical: ao longo das três últimas décadas, no mínimo, o papel de arquivilão era
        atribuído à gordura saturada. No momento em que Yudkin fazia sua pesquisa, nos anos 60, uma nova ortodoxia
        nutricional se afirmava: a alimentação saudável deveria ser pobre em gordura. Yudkin liderava um grupo cada vez
        menor de dissidentes que creditava ao açúcar – e não à gordura – a causa mais provável de males como obesidade,
        doença cardíaca e diabetes.

        **Contagens**: 12 sinais de pontuação e 4 tipos de sinais de pontuação (ponto, dois pontos, vírgula, travessão)

        **Resultado Esperado**: 4/12 = 0,33

        **Resultado obtido**: 0,33

        **Status**: correto
    """

    name = 'Punctuation Diversity Ratio'
    column_name = 'punctuation_diversity'

    def value_for_text(self, t, rp=default_rp):
        expression = re.compile('''
                                \\.\\.+|         # ponto final e reticências
                                \\s+\\-|\\-\\s+| # hifens
                                [.!(),–:;?]      # Demais pontuações
                                ''',
                                re.VERBOSE)
        try:
            puncts = re.findall(expression, t.raw_content)
            return rp.mattr(puncts)
            # return len(set(puncts)) / len(puncts)
        except ZeroDivisionError:
            return 0


class IndicativePresentMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_present_ratio

        **Interpretação**: o presente do indicativo é o tempo verbal de mais frequente de todas as formas flexionadas.
        Pode ocorrer em textos de diferentes níveis de complexidade.

        **Descrição da métrica**: proporção de verbos no presente do modo indicativo, em relação ao total de verbos
        flexionados do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*PR.*IND e divide-se o resultado
        pelo total de verbos flexionados do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste 1**:

        O secretário da Segurança Pública, Enio Bacci, disse que o aumento está ligado à legislação branda contra
        desmanches, ao aumento da frota e ao chamado golpe do seguro -- quando o dono vende o carro a bandidos e recebe
        um novo da seguradora, mas reconheceu que precisa ajustar a repressão.

        **Contagens**:

        6 verbos, 4 no presente do indicativo (está, vende, recebe, precisa), 2 no pretérito perfeito (disse,
        reconheceu)

        O parser, contudo, reconheceu indevidamente o substantivo “desmanches” como mais um verbo (no presente do
        subjuntivo).

        **Resultado Esperado**: 0,667 (4/6) ou 0,571 (4/7) se considerarmos o erro do parser

        **Resultado Obtido**: 0,571

        **Status**: correto
    """

    name = 'Ratio of Indicative Present Mood'
    column_name = 'indicative_present_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[0] / sum(tenses)


class IndicativePerfectMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_preterite_perfect_ratio

        **Interpretação**: o pretérito perfeito simples do indicativo é um tempo frequente. Pode ocorrer em textos de
        diferentes níveis de complexidade. Não está claro qual sua relação com o nível de complexidade do texto.

        **Descrição da métrica**: proporção de verbos no pretérito perfeito simples do modo indicativo, em relação ao
        total de verbos do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*PS.*IND e divide-se o resultado
        pelo total de verbos do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste 1**:

        Robert Lustig trabalha como endocrinologista pediátrico na Universidade da Califórnia, especializado no
        tratamento da obesidade infantil. Em 2009, ele proferiu a palestra “Açúcar: a amarga verdade”, que teve mais
        de 6 milhões de visualizações no YouTube. No decorrer de uma hora e meia, Lustig defende com veemência que a
        frutose, um açúcar onipresente na alimentação moderna, é o “veneno” responsável pela epidemia de obesidade nos
        Estados Unidos.

        **Contagens**: 6 verbos, 3 no presente, 2 no pretérito perfeito

        **Resultado Esperado**: 2/5 = 0,40

        **Resultado Obtido**: 0,40

        **Status**: correto
    """

    name = 'Ratio of Indicative Preterite Perfect Mood'
    column_name = 'indicative_preterite_perfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[2] / sum(tenses)


class IndicativeImperfectMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_imperfect_ratio

        **Interpretação**: o pretérito imperfeito do indicativo é um tempo frequente. Pode ocorrer em textos de
        diferentes níveis de complexidade. Não está claro qual sua relação com o nível de complexidade do texto.

        **Descrição da métrica**: proporção de verbos no pretérito imperfeito do modo indicativo, em relação ao total
        de verbos do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*IMPF.*IND e divide-se o resultado
        pelo total de verbos flexionados do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: A conclusão da investigação do exército sobre o caso, que vazou para a imprensa, afirma que as
        acusações de homicídio doloso (com intenção) eram "infundadas".

        **Contagens**: 3 verbos flexionados (vazou, afirma, eram); 1 verbo no pretérito imperfeito do indicativo (eram)

        **Resultado Esperado**: 0,333 (1/3)

        **Resultado Obtido**: 0,333

        **Status**: correto
    """

    name = 'Ratio of Indicative Imperfect Mood'
    column_name = 'indicative_imperfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[1] / sum(tenses)


class IndicativePluperfectMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_pluperfect_ratio

        **Interpretação**: o pretérito mais que perfeito é um verbo pouco frequente e está associado a alta complexidade.
        Portanto, quanto maior a métrica, maior a complexidade.

        **Descrição da métrica**: proporção de verbos no pretérito mais que perfeito do modo indicativo, em relação ao
        total de verbos do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V MQP.*IND e divide-se o resultado
        pelo total de verbos flexionados do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras. A terceira pessoa do
        plural dos tempos pretérito perfeito e pretérito mais que perfeito são iguais, o que gera ambiguidade,
        aumentando indevidamente a estatística desta métrica.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Trechos do vídeo foram exibidos pela rede britânica BBC e mostram uma fileira de corpos com
        ferimentos claramente provocados por tiros.

        **Contagens**: 2 verbos, os dois flexionados (foram, mostram).

        A forma “foram” está usada no pretérito perfeito, mas como se trata de uma forma ambígua, o parser a reconheceu
        com 2 etiquetas: pretérito mais que perfeito e pretérito perfeito, fazendo o cálculo da métrica computar 3
        verbos flexionados

        **Resultado Esperado**: 0

        **Resultado Obtido**: 0,333 (1/3)

        **Status**: correto, considerando a limitação do parser
    """

    name = 'Ratio of Indicative Pluperfect Mood'
    column_name = 'indicative_pluperfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[3] / sum(tenses)


class IndicativeFutureMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_future_ratio

        **Interpretação**: o futuro do indicativo não está entre os tempos verbais mais frequentes e pode estar
        associado a complexidade mediana. Portanto, quanto maior a métrica, maior a complexidade.

        **Descrição da métrica**: proporção de verbos no futuro do indicativo em relação ao total de verbos flexionados
        do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta 'V.*FUT*IND e divide-se o resultado
        pelo total de verbos flexionados do texto (VFIN).

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Pescadores tentarão retirar o maior número de peixes da espécie, que pode atingir 20 centímetros de
        comprimento e um quilo.

        **Contagens**: 2 verbos flexionados (tentarão, pode), 1 no futuro do indicativo (tentarão)

        **Resultado Esperado**: 0,50 (1/2)

        **Resultado Obtido**: 0,50

        **Status**: correto
    """

    name = 'Ratio of Indicative Future mood'
    column_name = 'indicative_future_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[4] / sum(tenses)


class IndicativeConditionMoodRatio(base.Metric):
    """
        **Nome da Métrica**: indicative_condition_ratio

        **Interpretação**: o futuro do pretérito do indicativo não está entre os tempos verbais mais frequentes e pode
        estar associado a complexidade mediana. Portanto, quanto maior a métrica, maior a complexidade.

        **Descrição da métrica**: proporção de verbos no futuro do pretérito do indicativo em relação ao total de verbos
        flexionados do texto

        **Definição dos termos que aparecem na descrição da métrica**: o futuro do pretérito do indicativo chama-se
        “condicional” na gramática do português europeu e corresponde ao “conditional” do inglês.

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta 'V.*COND’ e divide-se o resultado
        pelo total de verbos flexionados do texto (VFIN).

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Com a oferta do uniforme, as escolas públicas poderão torná-lo obrigatório, o que eliminaria a roupa
        como um indicador de diferenças sociais nas escolas e não criaria constrangimento aos alunos mais pobres.

        **Contagens**: 3 verbos flexionados (poderão, eliminaria, criaria), dois dos quais no futuro do pretérito do
        indicativo (eliminaria e criaria)

        **Resultado Esperado**: 0,666 (2/3)

        **Resultado Obtido**: 0,666

        **Status**: correto
    """

    name = 'Ratio of Indicative Condition Mood'
    column_name = 'indicative_condition_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[5] / sum(tenses)


class SubjunctivePresentMoodRatio(base.Metric):
    """
        **Nome da Métrica**: subjunctive_present_ratio

        **Interpretação**: o presente do subjuntivo é um tempo usado com menor frequência e sua ocorrência pode estar
        associada a maior complexidade

        **Descrição da métrica**: Proporção de Verbos no Presente do Subjuntivo em relação ao total de verbos
        flexionados do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*PR.*SUBJ e divide-se o resultado
        pelo total de verbos flexionados (VFIN) do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:  a precisão da métrica depende do desempenho do parser Palavras. Como as terceiras
        pessoas do presente do subjuntivo são ambíguas com as terceiras pessoas do imperativo e o parser por default
        anota todas como subjuntivo, esta métrica pode ser superestimada.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: A regra obriga as legendas a fechar nos Estados apenas coligações que não colidam com as nacionais.

        **Contagens**: 2 verbos flexionados, 1 no presente do indicativo (obriga) e 1 no presente do subjuntivo
        (colidam)

        **Resultado Esperado**: 0,50 (1/2)

        **Resultado Obtido**: 0,50

        **Status**: correto
    """

    name = 'Ratio of Subjunctive Present mood'
    column_name = 'subjunctive_present_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[6] / sum(tenses)


class SubjunctiveImperfectMoodRatio(base.Metric):
    """
        **Nome da Métrica**: subjunctive_imperfect_ratio

        **Interpretação**: o imperfeito do subjuntivo é um tempo usado com menor frequência e sua ocorrência pode estar
        associada a maior complexidade

        **Descrição da métrica**: Proporção de Verbos no Pretérito Imperfeito do Subjuntivo em relação ao total de
        verbos flexionados

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta 'V.*IMPF.*SUBJ' e divide-se o
        resultado pelo total de verbos flexionados do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:  a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Não fosse o aspecto financeiro, o projeto teria o apoio incondicional de Balzano e do presidente da
        Famurs, Flávio Luiz Lammel.

        **Contagens**: 2 verbos flexionados, 1 no imperfeito do subjuntivo (fosse) e 1 no futuro do pretérito do
        indicativo (teria).

        **Resultado Esperado**: 0,50 (1/2)

        **Resultado Obtido**: 0,50

        **Status**: correto
    """

    name = 'Ratio of Subjunctive Imperfect mood'
    column_name = 'subjunctive_imperfect_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[7] / sum(tenses)


class SubjunctiveFutureMoodRatio(base.Metric):
    """
        **Nome da Métrica**: subjunctive_future_ratio

        **Interpretação**: o futuro do subjuntivo é um tempo usado com menor frequência e sua ocorrência pode estar
        associada a maior complexidade

        **Descrição da métrica**: Proporção de Verbos no Futuro do Subjuntivo em relação ao total de verbos flexionados

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências da etiqueta V.*FUT.*SUBJ e divide-se o resultado
        pelo total de verbos flexionados do texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:  a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Se a idéia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado,
        meias, calça e camiseta.

        **Contagens**: 2 verbos flexionados, 1 no futuro do subjuntivo (for) e 1 no futuro do indicativo (receberão)

        **Resultado Esperado**: 0,50 (1/2)

        **Resultado Obtido**: 0,50

        **Status**: correto
    """

    name = 'Ratio of Future Imperfect mood'
    column_name = 'subjunctive_future_ratio'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]
        return tenses[8] / sum(tenses)


# class ImperativeMoodRatio(base.Metric):
#     """
#         **Nome da Métrica**: imperative_ratio
#
#         **Interpretação**: verbos no modo imperativo sugerem diálogo com o leitor, o que pode estar associado à
#         facilitação da leitura. Portanto, quanto maior a proporção, menor a complexidade.
#
#         **Descrição da métrica**: Proporção de verbos no modo imperativo em relação ao total de verbos
#
#         **Definição dos termos que aparecem na descrição da métrica**:
#
#         **Forma de cálculo da métrica**: contam-se todas as ocorrências de V*IMP e divide-se o resultado pela quantidade
#         total de verbos.
#
#         **Recursos de PLN utilizados durante o cálculo**: parser Palavras
#
#         **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras. As formas mais usadas
#         do imperativo são as segundas pessoas. Como no português do Brasil as segundas pessoas mais usadas são “você” e
#         “vocês” (ao invés de “tu” e “vós”), que conjugam como terceiras pessoas, o imperativo acaba não sendo
#         reconhecido nessas pessoas, a forma verbal é ambígua com o presente do subjuntivo e, diante de dessas formas
#         ambíguas, o parser prioriza a forma do subjuntivo em detrimento da forma do imperativo (já que o imperativo na
#         terceira pessoa é raro em português europeu).
#
#         **Crítica**: Como o parser prioriza a forma do subjuntivo, esta métrica não consegue ser capturada e o resultado
#         sempre dará 0, motivo pelo qual é melhor comentá-la
#
#         **Projeto**: GUTEN
#
#         **Teste**: Não precisa viajar para comer: confira como fazer em casa uma torta de abóbora americana incrível!
#
#         **Contagens**:
#
#         2 verbos flexionados, 1 no presente do indicativo (precisa) e 1 no imperativo (confira).
#
#         O parser, contudo, anotou “confira” como terceira pessoa do presente do subjuntivo, quando na verdade se trata
#         da segunda pessoa do imperativo. Como as formas são ambíguas, o parser teria que usar pistas de contexto para
#         desambiguizar e anotar corretamente.
#
#         **Resultado Esperado**: 0,50 (1/2)
#
#         **Resultado Obtido**: 0
#
#         **Status**: correto, considerando limitação do parser
#     """
#
#     name = 'Ratio of Imperative mood'
#     column_name = 'imperative_ratio'
#
#     def value_for_text(self, t, rp=default_rp):
#         flat = rp.palavras_flat(t)
#         try:
#             present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             present_ind = 0
#         try:
#             imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             imperfect_ind = 0
#         try:
#             perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             perfect_ind = 0
#         try:
#             pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             pluperfect_ind = 0
#         try:
#             future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             future_ind = 0
#         try:
#             conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
#         except ZeroDivisionError:
#             conditional_ind = 0
#         try:
#             present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
#         except:
#             present_subj = 0
#         try:
#             imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
#         except:
#             imperfect_subj = 0
#         try:
#             future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
#         except:
#             future_subj = 0
#         try:
#             imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
#         except:
#             imperative = 0
#         tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
#                   future_ind, conditional_ind, present_subj, imperfect_subj,
#                   future_subj, imperative]
#         return tenses[9] / sum(tenses)


class VerbalMoodsTimeDiversity(base.Metric):
    """
        **Nome da Métrica**: verbal_time_moods_diversity

        **Interpretação**: quanto maior a diversidade de tempos e modos verbais, maior a complexidade

        **Descrição da métrica**: Quantidade de diferentes tempos e modos verbais no texto

        **Definição dos termos que aparecem na descrição da métrica**: há 10 tempos e modos verbais identificados pela
        métrica: indicativo: presente, pretérito imperfeito, pretérito perfeito, pretérito mais que perfeito, futuro,
        futuro do pretérito; subjuntivo: presente, pretérito imperfeito, futuro; imperativo. Portanto, o resultado pode
        variar de 0 a 10.

        **Forma de cálculo da métrica**: contam-se os diferentes tipos de tempo e modo verbal que ocorrem no texto.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser Palavras

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Ele fizera questão de enfatizar que, embora houvesse chegado tarde, havia telefonado antecipadamente
        para avisar do atraso. A empresa não quer ouvir os argumentos dele e afirmou que fará de tudo para demiti-lo
        dentro da lei.

        **Contagens**: 6 tempos/modo verbais (fizera, houvesse, havia, quer, afirmou, fará)

        **Resultado Esperado**: 6

        **Resultado Obtido**: 6

        **Status**: correto
    """

    name = 'Diversity of verbal time and mode inflections'
    column_name = 'verbal_time_moods_diversity'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        try:
            present_ind = len(re.findall('V.*PR.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            present_ind = 0
        try:
            imperfect_ind = len(re.findall('V.*IMPF.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            imperfect_ind = 0
        try:
            perfect_ind = len(re.findall('V.*PS.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            perfect_ind = 0
        try:
            pluperfect_ind = len(re.findall('V.*MQP.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            pluperfect_ind = 0
        try:
            future_ind = len(re.findall('V.*FUT.*IND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            future_ind = 0
        try:
            conditional_ind = len(re.findall('V.*COND', flat)) / flat.count(' V ')
        except ZeroDivisionError:
            conditional_ind = 0
        try:
            present_subj = len(re.findall('V.*PR.*SUBJ', flat)) / flat.count(' V ')
        except:
            present_subj = 0
        try:
            imperfect_subj = len(re.findall('V.*IMPF.*SUBJ', flat)) / flat.count(' V ')
        except:
            imperfect_subj = 0
        try:
            future_subj = len(re.findall('V.*FUT.*SUBJ', flat)) / flat.count(' V ')
        except:
            future_subj = 0
        try:
            imperative = len(re.findall('V.*IMP ', flat)) / flat.count(' V ')
        except:
            imperative = 0
        tenses = [present_ind, imperfect_ind, perfect_ind, pluperfect_ind,
                  future_ind, conditional_ind, present_subj, imperfect_subj,
                  future_subj, imperative]

        return sum([1 for i in tenses if i > 0])



class MeanNounPhrase(base.Metric):
    """
        **Nome da Métrica**: mean_noun_phrase

        **Interpretação**: quanto maior o resultado, maior a complexidade textual

        **Descrição da métrica**: Média dos tamanhos médios dos sintagmas nominais nas sentenças

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: a partir das árvores de dependência do LX-Parser, localizam-se os NPs de alto
        nível (que não são filhos de outros NPs). Conta-se a quantidade palavras de cada NP, calcula-se o tamanho médio
        de NP por sentença e, depois, somam-se as médias obtidas e divide-se o resultado pela quantidade sentenças.

        **Recursos de PLN utilizados durante o cálculo**: LX-Parser

        **Limitações da métrica**: a precisão da métrica depende do desempenho do LX-Parser.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Três geneticistas norte-americanos receberam o Nobel por desvendarem o mecanismo por trás do ciclo
        circadiano, o relógio biológico que regula em animais e plantas os padrões diários de comportamento e funções
        vitais, como o metabolismo, níveis de hormônio, sono e temperatura corporal. Jeffrey C. Hall, de 72 anos,
        Michael Rosbash, de 73, e Michael W. Young, de 68, compartilham o prêmio de Medicina ou Fisiologia. Ao isolar,
        a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER), eles foram
        pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Contagens**: 3 sentenças com 96 palavras e 9 NPs de alto nível:

            1. Três geneticistas norte-americanos
            2. o Nobel
            3. o mecanismo por trás do ciclo circadiano, o relógio biológico que regula em animais e plantas os padrões
            diários de comportamento e funções vitais, como o metabolismo, níveis de hormônio, sono e temperatura
            corporal
            4. Jeffrey C. Hall, de 72 anos, Michael Rosbash, de 73, e Michael W. Young, de 68,
            5. o prêmio de Medicina ou Fisiologia
            6. os anos 1970
            7. genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER),
            8. eles
            9. pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        O LX-Parser identificou 4 sentenças com 96 palavras e 11 NPs de alto nível, como segue:
            1. Três geneticistas norte-americanos
            2. o Nobel
            3. o mecanismo por trás do ciclo circadiano, o relógio biológico que regula em animais e plantas os padrões
            diários de comportamento e funções vitais, como o metabolismo, níveis de hormônio, sono e temperatura
            corporal
            4. Jeffrey C.
            5. Hall, de 72 anos, Michael Rosbash, de 73, e Michael W. Young, de
            6. 68,
            7. o prêmio de Medicina ou Fisiologia
            8. Ao
            9. a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER),
            10. eles
            11. pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Resultado Esperado**: 10.8 (13 + 11 + 6,25/3)

        **Resultado Obtido**: 7,39 (13 + 2 + 6.33 + 8.25 / 4)

        **Status**: correto, consideradas as limitações do parser
    """
    name = 'Mean Noun Phrase'
    column_name = 'mean_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        all_leaves = rp.leaves_in_toplevel_nps(t)
        mean_sizes = [np.mean([len(toplevel) for toplevel in sent] if sent else 0) for sent in all_leaves]
        return np.mean(mean_sizes)


class MaxNounPhrase(base.Metric):
    """
        **Nome da Métrica**: max_noun_phrase

        **Interpretação**: quanto maior o resultado, maior a complexidade textual

        **Descrição da métrica**: Máximo entre os sintagmas nominais do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: a partir das árvores de dependência do LX-Parser, localizam-se os NPs de alto
        nível (que não são filhos de outros NPs). Conta-se a quantidade palavras de cada NP, e localiza-se o maior
        tamanho entre todos.

        **Recursos de PLN utilizados durante o cálculo**: LX-Parser

        **Limitações da métrica**: a precisão da métrica depende do desempenho do LX-Parser.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Três geneticistas norte-americanos receberam o Nobel por desvendarem o mecanismo por trás do ciclo
        circadiano, o relógio biológico que regula em animais e plantas os padrões diários de comportamento e funções
        vitais, como o metabolismo, níveis de hormônio, sono e temperatura corporal. Jeffrey C. Hall, de 72 anos,
        Michael Rosbash, de 73, e Michael W. Young, de 68, compartilham o prêmio de Medicina ou Fisiologia. Ao isolar,
        a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER), eles foram
        pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Contagens**: 3 sentenças com 96 palavras e 9 NPs de alto nível. A primeira sentença com 3 NPs (3, 2, 34
        palavras). A segunda sentença com 2 NPs (16 e 6 palavras). A terceira com 4 NPs (3, 12, 1, 9 palavras). Tamanhos
        máximos dos NPs nas sentenças: 34, 16 e 12, respectivamente.

        **Resultado Esperado**: 34

        **Resultado Obtido**: 34

        **Status**: correto
    """
    name = 'Maximum Noun Phrase'
    column_name = 'max_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        ret = 0
        if len(np_sizes) > 0:
            ret = max(np_sizes)
        return ret


class MinNounPhrase(base.Metric):
    """
        **Nome da Métrica**: min_noun_phrase

        **Interpretação**: quanto maior o resultado, maior a complexidade textual

        **Descrição da métrica**: Mínimo entre os sintagmas nominais do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: a partir das árvores de dependência do LX-Parser, localizam-se os NPs de alto
        nível (que não são filhos de outros NPs). Conta-se a quantidade palavras de cada NP, e localiza-se o menor
        tamanho entre todos.

        **Recursos de PLN utilizados durante o cálculo**: LX-Parser

        **Limitações da métrica**: a precisão da métrica depende do desempenho do LX-Parser.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Três geneticistas norte-americanos receberam o Nobel por desvendarem o mecanismo por trás do ciclo
        circadiano, o relógio biológico que regula em animais e plantas os padrões diários de comportamento e funções
        vitais, como o metabolismo, níveis de hormônio, sono e temperatura corporal. Jeffrey C. Hall, de 72 anos,
        Michael Rosbash, de 73, e Michael W. Young, de 68, compartilham o prêmio de Medicina ou Fisiologia. Ao isolar,
        a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER), eles foram
        pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Contagens**: 3 sentenças com 96 palavras e 9 NPs de alto nível. A primeira sentença com 3 NPs (3, 2, 34
        palavras). A segunda sentença com 2 NPs (16 e 6 palavras). A terceira com 4 NPs (3, 12, 1, 9 palavras). Tamanhos
        mínimos dos NPs nas sentenças: 2, 6 e 1, respectivamente.

        **Resultado Esperado**: 1

        **Resultado Obtido**: 1

        **Status**: correto
    """
    name = 'Minimum Noun Phrase'
    column_name = 'min_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        ret = 0
        if len(np_sizes) > 0:
            ret = min(np_sizes)
        return ret


class StdNounPhrase(base.Metric):
    """
        **Nome da Métrica**: std_noun_phrase

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual. Ela ajuda a interpretar o
        resultado da média.

        **Descrição da métrica**: Desvio-padrão do tamanho dos sintagmas nominais do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: : a partir das árvores de dependência do LX-Parser, localizam-se os NPs de alto
        nível (que não são filhos de outros NPs). Conta-se a quantidade palavras de cada NP e calcula-se o desvio-padrão
        entre os tamanhos (quanto os tamanhos desviam da média)

        **Recursos de PLN utilizados durante o cálculo**: LX-Parser

        **Limitações da métrica**: a precisão da métrica depende do desempenho do LX-Parser

        **Projeto**: GUTEN

        **Teste**: Três geneticistas norte-americanos receberam o Nobel por desvendarem o mecanismo por trás do ciclo
        circadiano, o relógio biológico que regula em animais e plantas os padrões diários de comportamento e funções
        vitais, como o metabolismo, níveis de hormônio, sono e temperatura corporal. Jeffrey C. Hall, de 72 anos,
        Michael Rosbash, de 73, e Michael W. Young, de 68, compartilham o prêmio de Medicina ou Fisiologia. Ao isolar,
        a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER), eles foram
        pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Contagens**: 3 sentenças com 96 palavras e 9 NPs de alto nível. A primeira sentença com 3 NPs (3, 2, 34
        palavras). A segunda sentença com 2 NPs (16 e 6 palavras). A terceira com 4 NPs (3, 12, 1, 9 palavras).
            10. Três geneticistas norte-americanos
            11. o Nobel
            12. o mecanismo por trás do ciclo circadiano, o relógio biológico que regula em animais e plantas os padrões
            diários de comportamento e funções vitais, como o metabolismo, níveis de hormônio, sono e temperatura
            corporal
            13. Jeffrey C. Hall, de 72 anos, Michael Rosbash, de 73, e Michael W. Young, de 68,
            14. o prêmio de Medicina ou Fisiologia
            15. os anos 1970
            16. genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER),
            17. eles
            18. pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        O LX-Parser errou na identificação de 3 NPs: os de 16, 3 e 12 palavras, gerando 5 NPs com 2, 12, 1, 1 e 22
        palavras, conforme segue:
            12. Três geneticistas norte-americanos
            13. o Nobel
            14. o mecanismo por trás do ciclo circadiano, o relógio biológico que regula em animais e plantas os padrões
            diários de comportamento e funções vitais, como o metabolismo, níveis de hormônio, sono e temperatura
            corporal
            15. Jeffrey C.
            16. Hall, de 72 anos, Michael Rosbash, de 73, e Michael W. Young, de
            17. 68,
            18. o prêmio de Medicina ou Fisiologia
            19. Ao
            20. a partir dos anos 1970, genes ligados ao ritmo biológico, como o timeless (TIM) e o period (PER),
            21. eles
            22. pioneiros em estabelecer conexões diretas entre DNA e comportamento.

        **Resultado Esperado**: 10,157 (desvio entre 3, 2, 34, 16, 6, 3, 12, 1, 9)

        **Resultado Obtido**: 10,45 (desvio entre 3, 2, 34, 2, 12, 1, 6, 1, 22, 1, 9)

        **Status**: correto, considerando as limitações do parser
    """
    name = 'Std Noun Phrase'
    column_name = 'std_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        retorno = 0.0
        if len(np_sizes) > 0:
            retorno = np.std(np_sizes)
        return retorno


class InfiniteSubordinateClauses(base.Metric):
    """
        **Nome da Métrica**: infinite_subordinate_clauses

        **Interpretação**:.quanto maior o resultado da métrica, maior a complexidade

        **Descrição da métrica**: Proporção de orações subordinadas reduzidas em relação à quantidade de orações do
        texto

        **Definição dos termos que aparecem na descrição da métrica**: orações subordinadas reduzidas são aquelas
        formadas por verbos nas formas nominais (ou infinitas): infinitivo, gerúndio e particípio

        **Forma de cálculo da métrica**: contam-se as ocorrências de verbo principal nas formas infinitas
        (<mv>.*V (INF|PCP|GER)(?!.*ICL-AUX) e divide-se pelo total de orações (V – aux).

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Ele, determinado a entrar na universidade e sempre estudando horas a fio, foi o único a se lembrar
        do prazo final para inscrição no vestibular.

        **Contagens**: 5 verbos, 4 nas formas infinitas (determinado, entrar, estudando, lembrar)

        **Resultado Esperado**: 0,80

        **Resultado Obtido**: 0,80

        **Status**: correto
    """

    name = 'Ratio of Infinite Subordinate Clauses per Number of Clauses'
    column_name = 'infinite_subordinate_clauses'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        infinite_subordinate = re.findall(r"<mv>.*V (INF|PCP|GER)(?!.*ICL-AUX)", flat)
        return len(infinite_subordinate) / rp.num_clauses(t)


class SubordinateClauses(base.Metric):
    """
        **Nome da Métrica**: subordinate_clauses

        **Interpretação**: as orações subordinadas são estruturas mais complexas, que demandam mais esforço de
        processamento. Portanto, quanto maior o resultado, maior a complexidade.

        **Descrição da métrica**: proporção de orações subordinadas em relação a todas orações do texto.

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: computam-se as orações subordinadas reduzidas de infinitivo, gerúndio e
        particípio. Para isso, buscam-se verbos nas formas infinitivas, excluindo-se aqueles precedidos de verbos
        auxiliares (<mv>.*V (INF|PCP|GER) menos ICL-AUX); somam-se, a essas, as orações subordinadas introduzidas por
        conjunções subordinativas (KS) e orações subordinadas relativas (<rel>). Essa métrica tem origem no AIC, mas
        foi refeita durante do convênio ICMC-GUTEN.

        **Recursos de PLN utilizados durante o cálculo**: parser Palavras.

        **Limitações da métrica**: a precisão da métrica depende do desempenho do parser na atribuição das etiquetas
        utilizadas no cálculo.

        **Crítica**:

        **Projeto**: GUTEN

        **Teste**: Ele e amigos, como Giovane Silva Ferreira, 13 anos, passam as tardes pescando o peixe, depois levado
        para uma associação de artesãos que faz o curtimento da pele do animal.

        **Contagens**: 4 orações (passam, pescando, levado, faz), 1 subordinada reduzida de gerúndio (pescando), 1
        subordinada reduzida de particípio (levado), 1 subordinada relativa (que faz).

        **Resultado Esperado**: 0,75

        **Resultado Obtido**: 0,75

        **Status**: correto
    """

    name = 'Ratio of Subordinate Clauses per Number of Clauses'
    column_name = 'subordinate_clauses'

    def value_for_text(self, t, rp=default_rp):
        flat = rp.palavras_flat(t)
        num_subordinate = re.findall(r"<mv>.*V (INF|PCP|GER)(?!.*ICL-AUX)| KS |<rel>", flat)
        return len(num_subordinate) / rp.num_clauses(t)


class GUTEN(base.Category):
    name = 'GUTEN'
    table_name = 'guten'

    def __init__(self):
        super(GUTEN, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics = [m for m in self.metrics if m.name != 'AnaphoricReferencesBase']
        self.metrics.sort(key=lambda m: m.name)
