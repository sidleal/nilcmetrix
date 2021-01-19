# -*- coding: utf-8 -*-
import text_metrics
import datetime

begintime = datetime.datetime.now()
print(begintime)

# text = "Cassiano Cordi e outros. Para filosofar. Compreendendo o tempo e o espaço."
# text = "Isso é um teste de palavras difíceis, tipo borlas."

# text = """
# Os partidos estão mais cautelosos. A Casa tem em torno de 160 contratos para serem analisados. Vários contratos são antigos.
# """

# text = """
# Os partidos estão mais cautelosos.
# """

# text = """
# A Casa tem em torno de 160 contratos para serem analisados.
# """

# text = """
# Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de alunos dos ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como forma de proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se a idéia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e camiseta.
# """

# text = """
# Paubrasilia echinata  é o nome científico do pau-brasil, que é uma leguminosa nativa da floresta atlântica e que está ameaçada de extinção, incluída na Lista Oficial de Espécies da Flora Brasileira Ameaçadas de Extinção. A árvore pode chegar a até 30 metros de altura, tem seu tronco e galhos de cor acinzentada e com espinhos. As flores apresentam cinco pétalas, quatro totalmente amarelas e uma que é amarela com uma mancha vermelha no centro. Essa pétala diferente é chamada de “estandarte”, por chamar a atenção das abelhas, que são seus polinizadores. Ela funciona como um guia visual para as abelhas encontrarem o néctar ao visitarem as flores do pau-brasil.
# Os frutos são vagens verdes que quando estão maduras se tornam secas e marrons. Esse tipo de fruto é chamado de legume, que é um fruto bem comum na família do pau-brasil. No pau-brasil há espinhos até nas vagens, que alguns autores já compararam com ouriços.
# Atualmente, o pau-brasil é muito encontrado em áreas urbanas (praças, parques e avenidas) e dessa forma podem contribuir para a movimentação dos polinizadores entre espaços verdes urbanos e áreas naturais de floresta atlântica próximas desses espaços. Assim, dizemos que suas árvores plantadas nesses locais podem ajudar para a conservação “ex situ” que para a ciência quer dizer “fora do seu lugar de origem”. Mesmo assim, a espécie continua interagindo com o meio ambiente e cumprindo seu papel na natureza.
# """

text = """
Paubrasilia echinata  é o nome científico do pau-brasil, que é uma leguminosa nativa da floresta atlântica e que está ameaçada de extinção, incluída na Lista Oficial de Espécies da Flora Brasileira Ameaçadas de Extinção. A árvore pode chegar a até 30 metros de altura, tem seu tronco e galhos de cor acinzentada e com espinhos. As flores apresentam cinco pétalas, quatro totalmente amarelas e uma que é amarela com uma mancha vermelha no centro. Essa pétala diferente é chamada de “estandarte”, por chamar a atenção das abelhas, que são seus polinizadores. Ela funciona como um guia visual para as abelhas encontrarem o néctar ao visitarem as flores do pau-brasil.
"""

t = text_metrics.Text(text)


ret = text_metrics.nilc_metrics.values_for_text(t).as_flat_dict()

print("===============")
print(text)
print("===============")
print(ret)
print("mean_noun_phrase", ret["mean_noun_phrase"])

print("cw_freq:", ret["cw_freq"])
print("min_cw_freq:", ret["min_cw_freq"])

print("cw_freq_brwac:", ret["cw_freq_brwac"])
print("min_cw_freq_brwac:", ret["min_cw_freq_brwac"])
print("freq_brwac:", ret["freq_brwac"])
print("min_freq_brwac:", ret["min_freq_brwac"])

print("cw_freq_bra:", ret["cw_freq_bra"])
print("min_cw_freq_bra:", ret["min_cw_freq_bra"])
print("freq_bra:", ret["freq_bra"])
print("min_freq_bra:", ret["min_freq_bra"])

print("----------------------")

print('lsa_adj_mean:', ret['lsa_adj_mean'])
print('lsa_adj_std:', ret['lsa_adj_std'])
print('lsa_all_mean:', ret['lsa_all_mean'])
print('lsa_all_std:', ret['lsa_all_std'])
print('lsa_paragraph_mean:', ret['lsa_paragraph_mean'])
print('lsa_paragraph_std:', ret['lsa_paragraph_std'])
print('lsa_givenness_mean:', ret['lsa_givenness_mean'])
print('lsa_givenness_std:', ret['lsa_givenness_std'])
print('lsa_span_mean:', ret['lsa_span_mean'])
print('lsa_span_std:', ret['lsa_span_std'])


endtime = datetime.datetime.now()

print(endtime)
print("tempo:", endtime - begintime)

