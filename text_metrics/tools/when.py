#!/usr/bin/env python
#-*- encoding:utf-8 -*-

# WHEN_rules.py : Identify temporal expressions in the text

# This code is available under the MIT License.
# (c)2016 Alessandro Bokan Garay,
#         Deutsches Forschungszentrum für Künstliche Intelligenz (DFKI)

from __future__ import unicode_literals

import re

numbers = [
    'um(a)?', 'dois', 'duas', 'três', 'quatro', 'cinco', 'seis', 'sete',
    'oito', 'nove', 'dez', 'once', 'doze', 'treze', 'quatorze', 'quinze',
    'dezesseis', 'dezessete', 'dezoito', 'dezenove'
]

cardinals = [
    'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta',
    'oitenta', 'noventa', 'cem', 'cento'
]

days = [
    'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo'
]

months = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
    'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
]

time = [
    'microssegundo', 'segundo', 'minuto', 'hora', 'dia', 'semana', 'mês',
    'ano', 'década', 'milênio', 'semestre', 'bimestre', 'trimestre',
    'época', 'tempo', 'set', 'etapa',
]

adverbs = [
    'hoje', 'amanhã', 'ontem', 'anteontem', 'tarde', 'madrugada', 'noite',
    'meia-noite', 'manhã',
]

demostratives = [
    'em(\s(o|a)(s)?)?', 'de', 'na(s)?', 'no(s)?', 'este(s)?', 'esta(s)?',
    'esse(s)?', 'essa(s)?', 'nesse(s)?', 'nessa(s)?', 'neste(s)?',
    'nesta(s)?', 'desse(s)?', 'dessa(s)?', 'deste(s)?', 'desta(s)?',
    'aquele(s)?', 'aquela(s)?', 'naquele(s)?', 'naquela(s)?', 'daquele(s)?',
    'daquela(s)?', 'há', 'depois de', 'no dia', 'aos',
]

referencial_exp = [
    'anteriormente', 'antigamente', 'atualmente', 'correntemente',
    'futuramente', 'imediatamente', 'modernamente', 'posteriormente',
    'postumamente', 'precedentemente', 'presentemente', 'recentemente',
    'subseqüentemente', 'tardiamente', 'ulteriormente', 'ultimamente',
]

duration_exp = [
    'brevemente', 'eternamente', 'momentaneamente', 'provisoriamente',
    'temporariamente', 'instantaneamente', 'durante'
]

frequency_exp = [
    'diariamente', 'semanalmente', 'mensalmente', 'anualmente', 'raramente',
    'constantemente', 'bimestralmente', 'trimestralmente', 'permanetemente',
    'periodicamente', 'quinzenalmente', 'semestralmente',
    '(quo|co)tidianamente', 'eventualmente', 'habitualmente', 'regularmente',
    'reiteradamente', 'rotineiramente', 'usualmente', 'ocasionalmente',
    'freq(u|ü)entemente', 'amiúde', 'todos os dias', 'todas as noites',
    'com freq(u|ü)ência', 'todas as manhãs', 'todas as tardes',
    '(várias|muitas|algumas|às|por)\svezes'
]

N = '|'.join(numbers)
C = '|'.join(cardinals)
D = '|'.join(days)
T = '|'.join(time)
M = '|'.join(months)
AT = '|'.join(adverbs)
PP = '|'.join(demostratives)
DE = '|'.join(duration_exp)
RE = '|'.join(referencial_exp)
FE = '|'.join(frequency_exp)
S = 'á|é|í|ó|ú|ã|õ|â|ê|ô|à|ü'


def filterTemporalExpressions(TEs):
    """
    Delete all the temporal expressions (TEs) that are included within
    other expressions.

    :param TEs: [('em 28 de fevereiro de 2002', 0, 26),
                 ('em 28 de fevereiro', 65, 83)]

    return: [('em 28 de fevereiro de 2002', 0, 26)]

    """
    i = 0
    while i != len(TEs):
        j = i + 1
        while j != len(TEs):
            a, b = TEs[i][0], TEs[j][0]
            if a in b:
                del TEs[i]
                j -= 1
            elif b in a:
                del TEs[j]
                j -= 1
            j += 1
        i += 1
    return TEs


def removeWhiteSpaces(TEs):
    """
    Remove the white-spaces in the temporal expressions

    :param TEs: [('sábado ', 0, 7), (' no dia', 56, 63)]

    :return: [('sábado', 0, 6), (' no dia ', 57, 63)]

    """
    for i in range(len(TEs)):
        if TEs[i][0].startswith(" "):
            TEs[i] = (TEs[i][0][1:], TEs[i][1] + 1, TEs[i][2])
        if TEs[i][0].endswith(" "):
            TEs[i] = (TEs[i][0][:-1], TEs[i][1], TEs[i][2] - 1)

    return TEs


def getTemporalExpressions(s):
    """
    Get all the temporal expressions (TEs) present in the sentence using
    "regular expressions". TEs are divided in 5 categories according to
    Batista et al. (2008): "ABSOLUTO", "DURACAO", "ENUNCIADO", "HORA"
    and "INTERVALO". This function received a sentence and return the
    temporal expressions and their positions

    :param s: "Sábado amanhece com poucas nuvens. Chance de chuva forte no dia"

    :return: [('sábado', 10, 22), (' no dia ', 133, 137)]

    """
    s = s.lower()
    # "ABSOLUTO" category
    r1 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(de|em|até|desde|para)\s\d{4}', s)]
    r2 = [(s[i.start():i.end()].strip(), i.start(), i.end()) for i in re.finditer('(^|\s)(em|até|desde)?(\s\d{1,2}\s(de))?\s(' + M + ')\s(de)\s\d{4}', s)]
    # "DURACAO" category
    r3 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)((cerca|mais|menos)\s)?((de|há|durante|em|por)\s)?((((' + C + ')\se\s)?(' + N + '))|(\d+))\s(' + T + ')(s|es)?(\se\s((((' + C + ')\se\s)?(' + N + '))|(\d+))\s(' + T + ')(s|es))?', s)]
    r4 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(' + DE + ')', s)]
    # "ENUNCIADO" category
    r5 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)((' + D + ')(s)?(-feira(s)?)|sábado(s)?|domingo(s)?)', s)]
    r6 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(na\s(' + AT + ')\s)?(' + PP + ')\s(' + D + ')(s)?(-feira(s)?)?(\,?\s?\(?\d+\)?)?', s)]
    r7 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)((até(\sa)?|(a\spartir\s)?de)\s)?(' + AT + ')', s)]
    # TODO "\w" da seguinte exressão não identifica "próximo"
    r8 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(' + PP + ')\s((\w|' + S + ')+\s)?((' + T + ')|(' + AT + '))(s|es)?', s)]
    r9 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(no\sdia|até|em|(a\spartir\s)?de|desde|('+ PP +'))(\s\d{1,2}\s(de))?\s(' + M + ')(\s(de)\s\d{4})?', s) if s[i.start() - 4:i.start()] not in ['rio ']]
    # "HORA" category
    r10 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(desde\sas|por\svolta\sdas|até|até\sàs|às|aos)\s((\d{1,2}(h|\shoras)(\d{1,2}(m(in)?)?)?)|(\d{1,2}(m(in)?|\sminutos)))', s)]
    r11 = [(s[i.start():i.end()].strip(), i.start(), i.end()) for i in re.finditer('\s\d{1,2}:\d{1,2}(\s(AM|PM))?', s)]
    # "INTERVALO" category
    r12 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(de|entre|desde)\s(' + M + ')\s(a|e|até)\s(' + M + ')(\sde\s\d{4})?', s)]
    r13 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(de|entre|entre\sos\sdias|desde)\s(\d{1,2})\s(a|e|até)\s(\d{1,2})(\sde\s(' + M + '))', s)]
    r14 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(entre)\s(as)\s(\d{1,2}(h(\d{1,2}(m)?)?)?)\s(e)\s(as)\s(\d{1,2}(h(\d{1,2}(m)?)?)?)', s)]
    r15 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(entre\s)?\d{4}(-|\s(a|e)\s)\d{4}', s)]
    # "REFERENCIAL" category
    r16 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)\d{1,2}(/|\.)\d{1,2}(/|\.)(\d{4}|\d{1,2})', s)]
    r17 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)\d{4}-\d{1,2}-\d{1,2}', s)]
    r18 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(' + RE + ')', s)]
    # "FREQUENCIA" category
    r19 = [(s[i.start():i.end()], i.start(), i.end()) for i in re.finditer('(^|\s)(' + FE + ')', s)]
    # All temporal expressions (TEs)
    TEs = list(set(r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14 + r15 + r16 + r17 + r18 + r19))
    # Filter temporal expressions
    TEs = filterTemporalExpressions(TEs)
    # Remove whitespaces
    TEs = removeWhiteSpaces(TEs)
    return sorted(TEs, key=lambda tup: tup[1])
