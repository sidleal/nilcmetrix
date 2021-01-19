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


class HypernymsVerbs(base.Metric):
    """
        **Nome da Métrica**: hypernyms_verbs

        **Interpretação**: teoricamente, quanto menos hiperônimos tem uma palavra, menos complexa ela é; portanto,
        quanto menor a métrica, menor a complexidade textual

        **Descrição da métrica**: Quantidade média de hiperônimos por verbo do texto

        **Definição dos termos que aparecem na descrição da métrica**:

        **Forma de cálculo da métrica**: primeiramente os verbos do texto são lematizados. Depois cada lema é procurado
        na Wordnet.Br. Se o verbo é encontrado, registra-se a quantidade de hiperônimos que ele possui. Somam-se as
        quantidades de hiperônimos de todos os verbos do texto encontrados na Wordnet.Br e divide-se o resultado pela
        quantidade desses verbos. Se o verbo não está na Wordnet.Br ele não participa do cálculo, mas se ele estiver e
        não possuir hyperônimos, ele participa do cálculo com 0 hiperônimos.

        **Recursos de PLN utilizados durante o cálculo**: léxico do DELAF para lematizar as formas verbais e Wordnet.Br
         para procurar hiperônimos

        **Limitações da métrica**:

        **Crítica**: a métrica não deveria considerar verbos auxiliares, pois quando um verbo é auxiliar ele tem uma
        função na gramática (tempo, aspecto, modalidade, construção de voz passiva) e não um “sentido”. Assim, os verbos
        que estiverem funcionando como auxiliares não têm hiperônimos.

        **Projeto**: Coh-Metrix-Port

        **Teste**: Ele sonha muito quando está acordado.

        **Contagens**: 2 verbos: sonhar (3 hiperônimos), acordar (0 hiperônimos)

        **Resultado Esperado**: 3/2 = 1,5

        **Resultado Obtido**: 1,5

        **Status**: correto
    """

    name = 'Mean number of Wordnet.Br hypernyms per verb'
    column_name = 'hypernyms_verbs'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        verb_tokens = [token[0] for token in rp.tagged_words(t)
                       if rp.pos_tagger().tagset.is_verb(token)
                       or rp.pos_tagger().tagset.is_participle(token)]
        verbs = [rp.db_helper().get_delaf_verb(verb) for verb in verb_tokens]
        lemmas = [verb.lemma for verb in verbs if verb is not None]
        hyper = [rp.db_helper().get_hypernyms(lemma) for lemma in lemmas]
        hyper_levels = [lemma.hyper_levels for lemma in hyper
                        if lemma is not None]
        return sum(hyper_levels) / len(hyper_levels) if hyper_levels else 0


class Hypernyms(base.Category):
    """
    """
    name = 'Hypernyms'
    table_name = 'hypernyms'

    def __init__(self):
        super(Hypernyms, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Hypernyms, self).values_for_text(t, rp)
