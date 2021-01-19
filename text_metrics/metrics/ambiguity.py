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


def calculate_ambiguity(rp, t, delaf_tag, tep_tag, checker):
    """Calculates the ambiguity metric for a word category, which is the average
    number of meanings of the words belonging to this category in the text.

    :rp: the resource pool to be used.
    :t: the text to be analyzed.
    :delaf_tag: the corresponding PoS tag used in the DELAF tables.
    :tep_tag: the corresponding PoS tag used in the Tep tables.
    :checker: a function that returns True iff a token is of the desired
    category

    :returns: the ratio between the total number of meanings and the total
    number of words for a given category.

    """

    words = [word.lower() for (word, tag) in rp.tagged_words(t)
             if checker((word, tag))]

    word_stems = [rp.stemmer().get_lemma(word, delaf_tag) for word in words]
    word_stems = [word for word in word_stems if word is not None]

    meanings_count = [rp.db_helper().get_tep_words_count(stem, tep_tag)
                      for stem in word_stems]
    meanings_count = [m for m in meanings_count if m is not None]

    return sum(meanings_count) / len(word_stems) if words else 0


def get_meanings_count(rp, t, delaf_tag, tep_tag, checker):
    """Get the number of meanings of the words belonging to this
    category in the text.

    :rp: the resource pool to be used.
    :t: the text to be analyzed.
    :delaf_tag: the corresponding PoS tag used in the DELAF tables.
    :tep_tag: the corresponding PoS tag used in the Tep tables.
    :checker: a function that returns True iff a token is of the desired
    category

    :returns: list with number of meanings for each word in a given category.

    """

    words = [word.lower() for (word, tag) in rp.tagged_words(t)
             if checker((word, tag))]

    word_stems = [rp.stemmer().get_lemma(word, delaf_tag) for word in words]
    word_stems = [word for word in word_stems if word is not None]

    meanings_count = [rp.db_helper().get_tep_words_count(stem, tep_tag)
                      for stem in word_stems]
    meanings_count = [m for m in meanings_count if m is not None]

    return meanings_count


class VerbAmbiguity(base.Metric):
    """
        **Nome da Métrica**: verbs_ambiguity

        **Interpretação**: não está clara a relação da métrica com a complexidade. Os verbos mais frequentes são os que
        possuem mais sentidos. Os verbos mais frequentes também são os primeiros a serem adquiridos e, portanto, os mais
        simples. Porém, nem todos os sentidos dos verbos polissêmicos são aprendidos de uma só vez.

        **Descrição da métrica**: proporção entre a quantidade de sentidos que os verbos do texto possuem no TEP e a
        quantidade de verbos do texto. Quanto mais sentidos tem um verbo, maior sua ambiguidade.

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: Identificam-se os verbos e usa-se um lematizador para descobri o lema deles.
        Busca-se a quantidade de sentidos que o lema de cada verbo apresenta no TEP, Thesaurus Eletrônico do Português
        (http://www.nilc.icmc.usp.br/tep2/). Somam-se as quantidades de sentidos de todos os verbos e divide-se o total
        pelo número de verbos do texto.

        **Recursos de PLN utilizados durante o cálculo**: nlpnet, TEP Thesaurus Eletrônico do Português

        **Limitações da métrica**: se o POS tagger ou o lematizador falharem em identificar o verbo, fica impossível
        buscar o número de sentidos no TEP.

        **Crítica**: teoricamente, a ambiguidade é um fator que aumenta a complexidade. Utilizar a quantidade de
        sentidos da palavra para medir ambiguidade, porém, pode não resultar em uma boa métrica, pois as palavras mais
        raras (e mais complexas) são as que possuem menos sentidos. Por exemplo, o verbo “ser” tem 12 sentidos no TEP e,
        por isso, contribui para a obtenção de uma alta proporção de ambiguidade. Não se pode inferir, contudo, que a
        ocorrência do verbo “ser” aumente a complexidade do texto.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino colou na prova, embora soubesse que poderia ser pego.

        **Contagens**: 5 verbos (colar, saber, poder, ser, pegar) com 4, 7, 2, 12, 17 sentidos, respectivamente, no TEP.

        **Resultado Esperado**: 8,4 (42/5)

        **Resultado Obtido**: 6,25 (o verbo “pegar” não foi identificado)

        **Status**:  correto, dependendo da corretude do PoS tagger e lematizador.
    """

    name = 'Mean number of TEP senses for verbs'
    column_name = 'verbs_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'V', 'Verbo',
                                   rp.pos_tagger().tagset.is_verb)


class NounAmbiguity(base.Metric):
    """
        **Nome da Métrica**: nouns_ambiguity

        **Interpretação**: não está clara a relação da métrica com a complexidade.

        **Descrição da métrica**: proporção de sentidos dos substantivos em relação à quantidade de substantivos

        **Definição dos termos que aparecem na descrição da métrica**: quantidade de sentidos é a soma de todos os
        sentidos de cada palavra no TEP Thesaurus Eletrônico do Português

        **Forma de cálculo da métrica**: Para cada substantivo do texto soma-se o número de sentidos que ele apresenta
        no TEP (Maziero et. al., 2008) e divide-se o total pelo número de substantivos do texto.

        **Recursos de PLN utilizados durante o cálculo**: TEP Thesaurus Eletrônico do Português

        **Limitações da métrica**:

        **Crítica**: teoricamente, a ambiguidade é um fator que aumenta a complexidade. Utilizar a quantidade de
        sentidos da palavra para medir ambiguidade, porém, pode não resultar em uma boa métrica, pois as palavras
        mais raras (e mais complexas) são as que possuem menos sentidos.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O menino colou na prova, embora soubesse que poderia ser pego.

        **Contagens**: 2 substantivos: menino e prova, com 1 e 9 sentidos no TEP, respectivamente.

        **Resultado Esperado**: 10/2 = 5

        **Resultado Obtido**: 5

        **Status**: correto
    """

    name = 'Mean number of TEP senses for nouns'
    column_name = 'nouns_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'N', 'Substantivo',
                                   rp.pos_tagger().tagset.is_noun)


class AdjectiveAmbiguity(base.Metric):
    """
        **Nome da Métrica**: adjectives_ambiguity

        **Interpretação**: não está clara a relação da métrica com a complexidade.

        **Descrição da métrica**: Ambiguidade de Adjetivos

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: Para cada adjetivo do texto soma-se o número de sentidos que ele apresenta no
        TEP (Maziero et. al., 2008) e divide-se o total pelo número de adjetivos do texto.

        **Recursos de PLN utilizados durante o cálculo**: TEP Thesaurus Eletrônico do Português

        **Limitações da métrica**: há palavras que não estão no TEP e isso compromete a confiabilidade da métrica

        **Crítica**: teoricamente, a ambiguidade é um fator que aumenta a complexidade. Utilizar a quantidade de
        sentidos da palavra para medir ambiguidade, porém, pode não resultar em uma boa métrica, pois as palavras mais
        raras (e mais complexas) são as que possuem menos sentidos.

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 6 adjetivos (polêmico, municipal, estadual, federal, solar, anual). Apenas o adjetivo “anual”
        consta do TEP, com 1 sentido

        **Resultado Esperado**: 1/6

        **Resultado Obtido**: 0,166

        **Status**: correto

    """

    name = 'Mean number of TEP senses for adjectives'
    column_name = 'adjectives_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'A', 'Adjetivo',
                                   rp.pos_tagger().tagset.is_adjective)


class AdverbAmbiguity(base.Metric):
    """
        **Nome da Métrica**: adverbs_ambiguity

        **Interpretação**: não está clara a relação da métrica com a complexidade.

        **Descrição da métrica**: Ambiguidade de Advérbios. Proporção entre a quantidade de sentidos dos advérbios do
        texto no TEP e a quantidade de advérbios do texto.

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: Para cada advérbio do texto (etiqueta ADV), soma-se o número de sentidos que
        ele apresenta no TEP (http://www.nilc.icmc.usp.br/tep2/) e divide-se o total pelo número de advérbios do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet e TEP Thesaurus Eletrônico do Português

        **Limitações da métrica**: há palavras que não estão no TEP e, quando isso ocorre, o número de sentidos é 0.
        Também pode ocorrer falha de POS tagging e de lematização, impedindo a identificação do lema a ser procurado no
        TEP.

        **Crítica**: teoricamente, a ambiguidade é um fator que aumenta a complexidade. Utilizar a quantidade de
        sentidos da palavra para medir ambiguidade, porém, pode não resultar em uma boa métrica, pois as palavras mais
        raras (e mais complexas) são as que possuem menos sentidos.

        O cálculo não está considerando a etiqueta PDEN (palavras denotativas) e as contrações de preposição com
        advérbios (ex: daqui, dali) PREP+ADV.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora do
        Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 5 advérbios (não, mais, já, não, também) com 1, 5, 4, 1 e 4 sentidos respectivamente.

        O tagger identificou 5 advérbios ['não', 'a', 'mais', 'já', 'não'] e 4 lemas ['não', 'mais', 'já', 'não'], os
        quais possuem 1, 5, 4, 1 sentidos respectivamente]

        **Resultado Esperado**: 15/5 = 3,0

        **Resultado Obtido**: 2,75 (11/4, porque o advérbio “também” está anotado como PDEN)

        **Status**: correto, considerando a limitação do tagger
    """

    name = 'Mean number of TEP senses for adverbs'
    column_name = 'adverbs_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'ADV', 'Advérbio',
                                   rp.pos_tagger().tagset.is_adverb)


class Ambiguity(base.Category):
    name = 'Ambiguity'
    table_name = 'ambiguity'

    def __init__(self):
        super(Ambiguity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
