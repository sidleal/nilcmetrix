# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = '/Users/fafg/classifier/basedir'
#BASE_DIR = '/home/sidleal/sid/usp/coh-metrix-nilc'
BASE_DIR = '/opt/text_metrics'
DIR = BASE_DIR + '/tools/'

NLPNET_DATA_DIR = DIR + 'nlpnet'

OPENNLP_MACMORPHO_BIN = DIR + 'apache-opennlp-1.5.3/bin/opennlp'
OPENNLP_MACMORPHO_MODEL = DIR + 'pt-pos-maxent.bin'

OPENNLP_UNIVERSAL_BIN = OPENNLP_MACMORPHO_BIN
OPENNLP_UNIVERSAL_MODEL = DIR + 'pt_br_universal-pos-maxent.bin'

LX_STANFORD_PATH = DIR + 'stanford-parser-2010-11-30/'
LX_MODEL_PATH = DIR + 'lxparser/cintil.ser.gz'

MALT_WORKING_DIR = DIR + 'maltparser-1.8.1'
MALT_MCO = MALT_WORKING_DIR + '/ptmalt.linear-1.8.1.mco'
MALT_JAVA_ARGS = ['-Xmx512m']

KENLM_LANGUAGE_MODEL = DIR + 'kenlm/corpus_3gram.binary'

# LSA_DICT_PATH = DIR + 'lsa/lsamodel_wordids_190k.txt.bz2'
# LSA_MODEL_PATH = DIR + '/lsa/lsamodel_lsi.model'
LSA_MODEL_PATH = DIR + '/lsa/brwac_full_lsa_word_dict.pkl'

# CALL_PALAVRAS_FLAT = DIR + 'PALAVRAS/call_palavras_flat.php'
# CALL_PALAVRAS_FLAT = 'http://10.11.14.126/services/service_palavras_flat.php'
# CALL_PALAVRAS_FLAT = 'http://143.107.183.175:12680/services/service_palavras_flat.php'
#CALL_PALAVRAS_TREE = 'http://143.107.183.175:23380/services/service_palavras_tree.php'
CALL_PALAVRAS_FLAT = 'http://10.11.14.33:4000/services/service_palavras_flat.php'
CALL_PALAVRAS_TREE = 'http://10.11.14.33:4000/services/service_palavras_tree.php'
#CALL_PALAVRAS_TREE = 'http://fw.nilc.icmc.usp.br:23380/api/v1/palavras/tigerxml/'
#CALL_PALAVRAS_FLAT = 'http://fw.nilc.icmc.usp.br:23380/api/v1/palavras/flat/'

# FLAT_TREES = '/Users/fafg/classifier/trees'
FLAT_TREES = '/Users/fafg/classifier/trees'

SIMPLE_WORDS = DIR + 'listas/list_biderman.txt'

FREQUENCIES_BRWAC = DIR + 'listas/lista_brWaC_geral_v3_nlpnet.tsv'
FREQUENCIES_BRASILEIRO = DIR + 'listas/wl_cb_full_1gram_sketchengine.txt'

DISCOURSE_MARKERS = DIR + 'listas/Marcadores.txt'

AMBIGUOUS_DISCOURSE_MARKERS = DIR + 'listas/Ambiguos.txt'

PRONOMES_INDEFINIDOS = DIR + 'listas/Pronomes_Indefinidos.txt'

LIWC_POS = DIR + 'liwc/pos.txt'
LIWC_NEG = DIR + 'liwc/neg.txt'

PALAVRAS_DIFICEIS = DIR + 'listas/palavras_dificeis/dificeis.pkl'

CONJUNCOES_FUND1 = DIR + 'listas/conjuncoes_fund_1.txt'
CONJUNCOES_FUND2 = DIR + 'listas/conjuncoes_fund_2.txt'

CONCRETENESS = DIR + 'listas/concreteness/concreteness.pkl'

PSICOLINGUISTICO = DIR + 'listas/psicolinguistico.txt'
