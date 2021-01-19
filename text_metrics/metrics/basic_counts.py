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
from text_metrics.utils import ilen
from text_metrics.tools import syllable_separator, pos_tagger
from text_metrics.resource_pool import rp as default_rp
from itertools import chain


class Flesch(base.Metric):
    """
        **Nome da Métrica**: flesch

        **Interpretação**: Índice de leiturabilidade de Flesch

        **Descrição da métrica**: O Índice de Legibilidade de Flesch busca uma correlação entre tamanhos médios de
        palavras e sentenças

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: 248.835 - [1.015 x (média de palavras por sentença)] - [84.6 x (Número de
        sílabas do texto / Número de palavras do texto)]

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 3 sentenças, 69 palavras, 160 sílabas. Médias: 23 palavras por sentença; 2,31 sílabas por palavra.

        **Resultado Esperado**: 248,835 – [1,015 x (23)] – [84,6 x (2,31)] => 248,835 – [23,345 – 195,43] = 29,316

        **Resultado Obtido**: 29,316

        **Status**: correto
    """

    name = 'Flesch index'
    column_name = 'flesch'

    def value_for_text(self, t, rp=default_rp):
        mean_words_per_sentence = WordsPerSentence().value_for_text(t)

        syllables = chain.from_iterable(
            map(syllable_separator.separate, rp.all_words(t)))
        mean_syllables_per_word = ilen(syllables) / ilen(rp.all_words(t))

        flesch = 248.835 - 1.015 * mean_words_per_sentence\
            - 84.6 * mean_syllables_per_word

        return flesch


class Words(base.Metric):
    """
        **Nome da Métrica**: words

        **Interpretação**: quanto maior a quantidade de palavras, maior a complexidade textual

        **Descrição da métrica**: quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todos os tokens (descontando as pontuações)

        **Recursos de PLN utilizados durante o cálculo**: nltk toolkit

        **Limitações da métrica**: a contagem depende do critério de tokenização adotado (separação das contrações,
        união de multiwords, união de nomes próprios)

        **Crítica**: o ideal é que o classificador adote uma única forma de tokenização para contagem de palavras

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
        proposta.

        **Contagens**: 17 palavras

        **Resultado Esperado**: 17

        **Resultado Obtido**: 17

        **Status**: correto
    """

    name = 'Number of Words'
    column_name = 'words'

    def value_for_text(self, t, rp=default_rp):
        return len(rp.tagged_words(t))


class Sentences(base.Metric):
    """
        **Nome da Métrica**: sentences

        **Interpretação**: quanto maior o número de sentenças, maior a complexidade

        **Descrição da métrica**: quantidade de sentenças no texto

        **Definição dos termos que aparecem na descrição da métrica**: sentença é o segmento do texto iniciado por letra
        maiúscula e terminado por ponto final, ponto de interrogação, ponto de exclamação ou reticências.

        **Forma de cálculo da métrica**: contam-se as sentenças reconhecidas pelo sentenciador

        **Recursos de PLN utilizados durante o cálculo**: sentenciador

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 4 sentenças

        **Resultado Esperado**: 4

        **Resultado Obtido**: 4

        **Status**: correto
    """

    name = 'Number of Sentences'
    column_name = 'sentences'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.sentences(t))


class Paragraphs(base.Metric):
    """
        **Nome da Métrica**: paragraphs

        **Interpretação**: quanto maior o número de parágrafos, maior a complexidade textual

        **Descrição da métrica**: quantidade de parágrafos do texto.

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas marcas de parágrafos somente a
        quebra de linha e não identações.

        **Forma de cálculo da métrica**: contam-se os parágrafos do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**:  Coh-Metrix-Port

        **Teste**:

        Os vermes – também chamados de helmintos – são parasitos, animais que, em geral, dependem da relação com outros
        seres para viver.

        Eles podem se hospedar no organismo de diversos animais, como bois, aves e peixes. Por isso, podemos também
        contraí-los comendo carnes cruas ou mal cozidas.

        **Contagens**: 2 parágrafos

        **Resultado Esperado**: 2

        **Resultado Obtido**: 2

        **Status**: correto
    """

    name = 'Number of Paragraphs'
    column_name = 'paragraphs'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.paragraphs(t))


class WordsPerSentence(base.Metric):
    """
        **Nome da Métrica**: words_per_sentence

        **Interpretação**: quanto maior a métrica, maior a complexidade

        **Descrição da métrica**: Número de palavras dividido pelo número de sentenças

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: divide-se o total de palavras do texto pelo número de sentenças do texto

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 95 palavras e 4 sentenças

        **Resultado Esperado**: 95/4 = 23,75

        **Resultado Obtido**: 23,75

        **Status**: correto
    """

    name = 'Mean words per sentence'
    column_name = 'words_per_sentence'

    def value_for_text(self, t, rp=default_rp):
        return Words().value_for_text(t) / Sentences().value_for_text(t)


class SentencesPerParagraph(base.Metric):
    """
        **Nome da Métrica**: sentences_per_paragraph

        **Interpretação**: não está clara a relação entre a métrica  e a complexidade textual

        **Descrição da métrica**: média da quantidade de sentenças por parágrafo.

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: Divide-se o número de sentenças pelo número de parágrafos.

        **Recursos de PLN utilizados durante o cálculo**:

        **Limitações da métrica**:

        **Crítica**: Essa medida não tem uma relação direta com a complexidade. Se as sentenças forem pequenas, o texto
        é simples e se as sentenças forem longas, o texto é mais complexo. O processo de simplificação produz mais
        sentenças por parágrafo devido à operação de divisão de sentenças longas. Nesse caso, o parágrafo original,
        mais complexo, tem menos sentenças que o parágrafo simplificado.

        **Projeto**: CMP

        **Teste**: Se, como parece cada vez mais provável, as diretrizes nutricionais que seguimos por quarenta anos
        estavam profundamente equivocadas, tal erro não pode ser posto na conta dos bichos-papões das grandes empresas.
        Tampouco pode ser considerado um engano científico inócuo. O massacre sofrido por John Yudkin contradiz essa
        interpretação e sugere ter ocorrido um erro que os cientistas impuseram a si próprios – e, por consequência,
        a todos nós.

        Tendemos a pensar que os hereges são pessoas que nadam contra a corrente, indivíduos inclinados a desafiar o
        conhecimento dominante. Às vezes, porém, um herege é apenas um pensador convencional que permanece olhando na
        mesma direção, ao passo que todos os demais passaram a olhar na direção contrária. Quando, em 1957, John Yudkin
        aventou pela primeira vez a possibilidade de o açúcar representar um perigo para a saúde pública, a hipótese
        foi levada a sério, assim como seu proponente. Ao se aposentar, catorze anos depois, tanto a teoria como seu
        autor haviam sido ridicularizados e marginalizados. Somente agora, postumamente, é que seu trabalho vem sendo
        reconduzido ao pensamento científico consolidado.

        **As guinadas na avaliação do legado de Yudkin pouco têm a ver com a metodologia científica**: devem-se em
        grande medida ao comportamento não científico da ciência da nutrição ao longo dos anos. Essa história começou
        a vir à tona na última década, menos por obra de nutricionistas de peso do que por céticos em relação à ciência
        nutricional. Na pesquisa meticulosa que resultou no livro “The Big Fat Surprise”(A Surpresa Grande e Gorda),
        a jornalista Nina Teicholz investiga o postulado “gordura saturada provoca doença cardíaca”, e revela que a
        passagem de teoria controversa a verdade aceita não ocorreu pela comprovação, e sim graças à influência de umas
        poucas personalidades poderosas – e de uma delas em particular.

        Teicholz também descreve como todo um establishment de importantes cientistas nutricionais, inseguro quanto à
        própria autoridade médica e atento a ameaças a ela, perpetrou tanto a defesa contínua e exagerada de uma
        alimentação com baixo teor de gordura, quanto o ataque a quem oferecia indícios ou argumentos contrários. John
        Yudkin foi apenas a primeira e mais célebre vítima.

        Hoje, enquanto nutricionistas lutam para compreender um desastre que não previram – mas decerto podem ter
        deflagrado –, a ciência da nutrição passa por um doloroso período de reavaliação. Aos poucos, evita proibições
        relativas ao colesterol e à gordura, enquanto intensifica advertências ao uso do açúcar, sem, no entanto,
        recuar por completo. Seus representantes mais antigos, porém, seguem munidos de um instinto corporativo que os
        leva a difamar quem desafia, em alto e bom som, aquele conhecimento em ruínas. É isso que Teicholz vem
        experimentando nos últimos tempos.

        **Contagens**: 17 sentenças e 5 parágrafos

        **Resultado Esperado**: 3,4

        **Resultado Obtido**: 3,4

        **Status**: correto
    """

    name = 'Mean sentences per paragraph'
    column_name = 'sentences_per_paragraph'

    def value_for_text(self, t, rp=default_rp):
        return Sentences().value_for_text(t) / Paragraphs().value_for_text(t)


class SyllablesPerContentWord(base.Metric):
    """
        **Nome da Métrica**: syllables_per_content_word

        **Interpretação**: quanto maior o número de sílabas por palavras, maior a complexidade textual

        **Descrição da métrica**: Número médio de sílabas por palavras de conteúdo no texto

        **Definição dos termos que aparecem na descrição da métrica**: são palavras de conteúdo as palavras de 4 classes
        gramaticais: substantivos, verbos, adjetivos e advérbios. São consideradas palavras de conteúdo as palavras de
        5 categorias de etiquetas do tagger nlpnet: substantivos (tags N, NPROP), verbos (tags V, VAUX, PCP), adjetivos
        (tag ADJ), advérbios (tag ADV) e palavras denotativas (tag PDEN).

        **Forma de cálculo da métrica**: contam-se as sílabas das palavras de conteúdo e depois divide-se o resultado
        pela quantidade de palavras de conteúdo.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
        proposta

        **Contagens**: 10 palavras de conteúdo (acessório, utilizado, adolescentes, boné, itens, compõem, idealizada,
        vestimenta, proposta), 35 sílabas (o silabificador considera “acessório” proparoxítona)

        **Resultado Esperado**: 35/10 = 3,5

        **Resultado Obtido**: 3,5

        **Status**: correto
    """

    name = 'Mean syllables per content word'
    column_name = 'syllables_per_content_word'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word,
                                rp.tagged_words(t))
        content_words = map(lambda t: t[0], content_tokens)

        syllables = map(syllable_separator.separate, content_words)

        nwords = 0
        nsyllables = 0
        for w in syllables:
            nwords += 1
            nsyllables += len(w)

        return nsyllables / nwords


class VerbRatio(base.Metric):
    """
        **Nome da Métrica**: verbs

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: Proporção de verbos em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se todas as ocorrências de verbos (tags 'V', 'VAUX', 'PCP') no texto e
        divide-se pela quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**:

        **Crítica**: Essa métrica usa tokenização sem fazer descontrações. É preciso uniformizar essa escolha em todas
        as métricas

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
        proposta

        **Contagens**: 4 verbos, 17 palavras

        **Resultado Esperado**: 0,235

        **Resultado Obtido**: 0,235

        **Status**: correto
    """

    name = 'Verb Ratio'
    column_name = 'verbs'

    def value_for_text(self, t, rp=default_rp):
        verbs = [t for t in rp.tagged_words(t)
                 if pos_tagger.tagset.is_verb(t)
                 or pos_tagger.tagset.is_auxiliary_verb(t)
                 or pos_tagger.tagset.is_participle(t)]
        return len(verbs) / len(rp.all_words(t))


class NounRatio(base.Metric):
    """
        **Nome da Métrica**: noun_ratio

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: proporção de substantivos em relação ao total de palavras do texto.

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se as ocorrências de substantivos (tags ‘N’ e ‘NPROP’) Recursos de PLN
        utilizados durante o cálculo: POS tagger do nlpnet

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Acessório utilizado por adolescentes, o boné é um dos itens que compõem a vestimenta idealizada pela
        proposta.

        **Contagens**: 17 palavras, 5 substantivos

        **Resultado Esperado**: 6/17 = 0,352

        **Resultado Obtido**: 0,352

        **Status**: correto
    """

    name = 'Noun Ratio'
    column_name = 'noun_ratio'

    def value_for_text(self, t, rp=default_rp):
        nouns = filter(pos_tagger.tagset.is_noun, rp.tagged_words(t))
        return ilen(nouns) / ilen(rp.all_words(t))


class AdjectiveRatio(base.Metric):
    """
        **Nome da Métrica**: adjective_ratio

        **Interpretação**: supõe-se que, quanto maior o valor da métrica, maior a complexidade textual

        **Descrição da métrica**: proporção de adjetivos em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se as ocorrências de adjetivos (tag ‘ADJ’) e divide-se pelo total de
        palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger do nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma
        emenda aprovada na Comissão de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR) quem sugeriu a
        inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais,
        estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados
        pelo excesso de exposição aos raios solares. Se a ideia for aprovada, os estudantes receberão dois conjuntos
        anuais, completados por calçado, meias, calça e camiseta.

        **Contagens**: 6 adjetivos, 95 palavras

        **Resultado Esperado**: 6/95 = 0,063

        **Resultado Obtido**: 0,063

        **Status**: correto
    """

    name = 'Adjective Ratio'
    column_name = 'adjective_ratio'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        return ilen(adjectives) / ilen(rp.all_words(t))


class AdverbRatio(base.Metric):
    """
        **Nome da Métrica**: adverbs

        **Interpretação**: não está clara a relação da métrica com a complexidade textual

        **Descrição da métrica**: Proporção de advérbios em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: são considerados advérbios as palavras anotadas
        com as etiquetas ADV,  PREP+ADV e PDEN

        **Forma de cálculo da métrica**: Divide-se a quantidade de advérbios pela quantidade de palavras do texto.

        **Recursos de PLN utilizados durante o cálculo**: nltk para fazer a sentenciação e a tokenização e nlpnet para
        identificar os advérbios

        **Limitações da métrica**: a precisão da métrica depende do desempenho do nlpnet.

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste 1**: Daqui a alguns anos, certamente seremos menos deslumbrados com as redes sociais. Agora, porém,
        muitos abusos são cometidos por conta desse deslumbramento.

        **Contagens**: 22 palavras e 4 advérbios (daqui, certamente, menos, agora)

        **Resultado Esperado**: 0,182 (4/22)

        **Resultado Obtido**: 0,182

        **Status**: correto

        **Teste 2**: No caso do Jeca Tatu, o verme que o deixou doente foi outro: o Ancylostoma. A larva desse verme
        vive no solo e penetra diretamente na pele. Só o contrai quem anda descalço na terra contaminada por fezes
        humanas. Se não se tratar, a pessoa fica fraca, sem ânimo e com a pele amarelada. Daí a doença ser também
        conhecida como amarelão.

        **Contagens**: 5 sentenças com um total de 62 palavras (total 62) e 5 a advérbios (diretamente, só, não, daí,
        também).

        **Resultado Esperado**: 0,081 (5/62)

        **Resultado Obtido**: 0,081

        **Status**: correto

        **Teste 3**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos
        suficientes para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica
        a diretora do Departamento Pedagógico da SEC, Sonia Balzano

        **Contagens**: 8 advérbios, 38 palavras

        **Resultado Esperado**: 0,211 (8/38)

        **Resultado Obtido**: 0,211

        **Status**: correto
    """

    name = 'Adverb Ratio'
    column_name = 'adverbs'

    def value_for_text(self, t, rp=default_rp):
        adverbs = [t for t in rp.tagged_words(t)
                   if pos_tagger.tagset.is_adverb(t)
                   or pos_tagger.tagset.is_denotative_word(t)]
        return ilen(adverbs) / ilen(rp.all_words(t))


class PronounRatio(base.Metric):
    """
        **Nome da Métrica**: pronoun_ratio

        **Interpretação**: supõe-se que, quanto maior o valor da métrica, maior a complexidade textual

        **Descrição da métrica**: proporção de pronomes em relação à quantidade de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: contam-se as ocorrências de pronomes (tags: 'PROPESS',

        'PROSUB', 'PROADJ', 'PRO-KS', 'PRO-KS-REL',) e divide-se pelo total de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger do nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 2 pronomes, 69 palavras

        **Resultado Esperado**: 2/69 = 0,029

        **Resultado Obtido**: 0,029

        **Status**: correto
    """

    name = 'Pronoun Ratio'
    column_name = 'pronoun_ratio'

    def value_for_text(self, t, rp=default_rp):
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        return ilen(pronouns) / ilen(rp.all_words(t))


class ContentWordRatio(base.Metric):
    """
        **Nome da Métrica**: content_words

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: proporção de palavras de conteúdo em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras de conteúdo as
        palavras de 5 classes de etiquetas do tagger nlpnet: substantivos (tags N, NPROP), verbos (tags V, VAUX, PCP),
        adjetivos (tag ADJ), advérbios (tag ADV) e palavras denotativas (tag PDEN).

        **Forma de cálculo da métrica**: contam-se as palavras de conteúdo e divide-se o resultado pela quantidade de
        palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger nlpnet

        **Limitações da métrica**: a precisão da métrica depende do desempenho do tagger.

        **Crítica**:

        **Projeto**: Coh-Metrix-Port

        **Teste**: Não podemos acrescentar nenhuma despesa a mais no nosso orçamento. Já não temos recursos suficientes
        para a manutenção das escolas, por exemplo, e também precisamos valorizar o magistério - justifica a diretora
        do Departamento Pedagógico da SEC, Sonia Balzano.

        **Contagens**: 38 palavras, 27 palavras de conteúdo

        **Resultado Esperado**: 27/38 = 0,711

        **Resultado Obtido**: 0,711

        **Status**: correto
    """

    name = 'Content word Ratio'
    column_name = 'content_words'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        return ilen(content_words) / ilen(rp.all_words(t))


class FunctionWordRatio(base.Metric):
    """
        **Nome da Métrica**: function_words

        **Interpretação**: não está clara a relação entre a métrica e a complexidade textual

        **Descrição da métrica**: porcentagem de palavras funcionais em relação ao total de palavras do texto

        **Definição dos termos que aparecem na descrição da métrica**: são consideradas palavras funcionais as palavras
        de 6 classes gramaticais: artigos (tag: ‘ART’), conjunções (tags ‘KS’ e ‘KC’), interjeições (tag: ‘IN’),
        numerais (tag: ‘NUM’), pronomes (tags: 'PROPESS',

        'PROSUB', 'PROADJ', 'PRO-KS', 'PRO-KS-REL'), preposições (tags: 'PREP', 'PREP+PROPESS', 'PREP+ART',
        'PREP+PRO-KS', 'PREP+PRO-KS-REL', 'PREP+PROADJ', 'PREP+ADV', 'PREP+PROSUB'). Incluem-se nas palavras funcionais
        os advérbios com função coordenativa e subordinativa (tags: 'ADV-KS', 'ADV-KS-REL). ',

        **Forma de cálculo da métrica**: contam-se as palavras funcionais do texto e divide-se o resultado pela
        quantidade de palavras do texto

        **Recursos de PLN utilizados durante o cálculo**: POS tagger do nlpnet

        **Limitações da métrica**:

        **Crítica**:

        **Projeto**:  Coh-Metrix-Port

        **Teste**: Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de
        alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como
        forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se
        a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e
        camiseta.

        **Contagens**: 69 palavras, 27 palavras funcionais

        **Resultado Esperado**: 0,391

        **Resultado Obtido**: 0,391

        **Status**: correto

    """

    name = 'Function word Ratio'
    column_name = 'function_words'

    def value_for_text(self, t, rp=default_rp):
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        return ilen(function_words) / ilen(rp.all_words(t))


class BasicCounts(base.Category):
    name = 'Basic Counts'
    table_name = 'basic_counts'

    def __init__(self):
        super(BasicCounts, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(BasicCounts, self).values_for_text(t, rp)
