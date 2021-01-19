package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os/exec"
	"sort"
	"strings"
	"text/template"
	"time"

	"github.com/gorilla/mux"
)

type Metric struct {
	Source string `json:"s"`
	Class  string `json:"c"`
	Key    string `json:"k"`
	Desc   string `json:"d"`
}

var metricMap = map[string]Metric{
	"adj_arg_ovl":                         {"CMP", "Coreference", "adj_arg_ovl", "Quantidade média de referentes que se repetem nos pares de sentenças adjacentes do texto"},
	"arg_ovl":                             {"CMP", "Coreference", "arg_ovl", "Quantidade média de referentes que se repetem nos pares de sentenças do texto"},
	"adj_stem_ovl":                        {"CMP", "Coreference", "adj_stem_ovl", "Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de sentenças adjacentes do texto"},
	"stem_ovl":                            {"CMP", "Coreference", "stem_ovl", "Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de sentenças do texto"},
	"adj_cw_ovl":                          {"CMP", "Coreference", "adj_cw_ovl ", "Quantidade média de palavras de conteúdo que se repetem nos pares de sentenças adjacentes do texto"},
	"adjacent_refs":                       {"CMP", "Anaphoras", "adjacent_refs", "Média das proporções  de candidatos a referentes na sentença anterior em relação aos pronomes pessoais do caso reto nas sentenças"},
	"anaphoric_refs":                      {"CMP", "Anaphoras", "anaphoric_refs", "Média das proporções  de candidatos a referentes nas 5 sentenças anteriores em relação aos pronomes anafóricos das sentenças"},
	"if_ratio":                            {"CMP", "Logic operators", "if_ratio", "Proporção do operador lógico SE em relação à quantidade de palavras do texto"},
	"or_ratio":                            {"CMP", "Logic operators", "or_ratio ", "Proporção do operador lógico OU em relação à quantidade de palavras do texto"},
	"and_ratio":                           {"CMP", "Logic operators", "and_ratio", "Proporção do operador lógico E em relação à quantidade de palavras do texto"},
	"logic_operators":                     {"CMP", "Logic operators", "logic_operators", "Proporção de Operadores Lógicos em relação à quantidade de palavras do texto"},
	"negation_ratio":                      {"CMP", "Logic operators", "negation_ratio", "Proporção de palavras que denotam negação em relação à quantidade de palavras do texto"},
	"hypernyms_verbs":                     {"CMP", "Hypernyms", "hypernyms_verbs", "Quantidade Média de Hiperônimos por verbo nas sentenças"},
	"conn_ratio":                          {"CMP", "Connectives", "conn_ratio", "Proporção de Conectivos em relação à quantidade de palavras do texto"},
	"add_pos_conn_ratio":                  {"CMP", "Connectives", "add_pos_conn_ratio", "Proporção de conectivos  aditivos positivos em relação à quantidade de palavras do texto"},
	"add_neg_conn_ratio":                  {"CMP", "Connectives", "add_neg_conn_ratio", "Proporção de conectivos  aditivos negativos em relação à quantidade de palavras do texto"},
	"tmp_pos_conn_ratio":                  {"CMP", "Connectives", "tmp_pos_conn_ratio", "Proporção de conectivos  temporais positivosem relação à quantidade de palavras do texto"},
	"tmp_neg_conn_ratio":                  {"CMP", "Connectives", "tmp_neg_conn_ratio", "Proporção de conectivos  temporais negativos em relação à quantidade de palavras do texto"},
	"cau_pos_conn_ratio":                  {"CMP", "Connectives", "cau_pos_conn_ratio", "Proporção de conectivos  causais positivos em relação à quantidade de palavras do texto"},
	"cau_neg_conn_ratio":                  {"CMP", "Connectives", "cau_neg_conn_ratio", "Proporção de conectivos  causais negativos em relação à quantidade de palavras do texto"},
	"log_pos_conn_ratio":                  {"CMP", "Connectives", "log_pos_conn_ratio", "Proporção de Conectivos Lógicos Positivos em relação à quantidade de palavras do texto"},
	"log_neg_conn_ratio":                  {"CMP", "Connectives", "log_neg_conn_ratio", "Proporção de Conectivos Lógicos Negativos em relação à quantidade de palavras do texto"},
	"function_words":                      {"CMP", "Basic Counts", "function_words", "Proporção de Palavras Funcionais em relação à quantidade de palavras do texto"},
	"content_words":                       {"CMP", "Basic Counts", "content_words", "Proporção de palavras de conteúdo em relação à quantidade de palavras do texto"},
	"pronoun_ratio":                       {"CMP", "Basic Counts", "pronoun_ratio", "Proporção de pronomes em relação à quantidade de palavras do texto"},
	"adjective_ratio":                     {"CMP", "Basic Counts", "adjective_ratio", "Proporção de Adjetivos em relação à quantidade de palavras do texto"},
	"words":                               {"CMP", "Basic Counts", "words", "Quantidade de Palavras no texto"},
	"paragraphs":                          {"CMP", "Basic Counts", "paragraphs", "Quantidade de Parágrafos no texto"},
	"verbs":                               {"CMP", "Basic Counts", "verbs", "Proporção de Verbos em relação à quantidade de palavras do texto"},
	"adverbs":                             {"CMP", "Basic Counts", "adverbs", "Proporção de Advérbios em relação à quantidade de palavras do texto"},
	"words_per_sentence":                  {"CMP", "Basic Counts", "words_per_sentence", "Média de Palavras por Sentença"},
	"syllables_per_content_word":          {"CMP", "Basic Counts", "syllables_per_content_word", "Quantidade média de sílabas por palavra no texto"},
	"sentences_per_paragraph":             {"CMP", "Basic Counts", "sentences_per_paragraph", "Quantidade média de sentenças por parágrafo no texto"},
	"noun_ratio":                          {"CMP", "Basic Counts", "noun_ratio ", "Proporção de substantivos em relação à quantidade de palavras do texto"},
	"sentences":                           {"CMP", "Basic Counts", "sentences", "Quantidade de Sentenças no texto"},
	"flesch":                              {"CMP", "Classic Formulas", "flesch", "Índice Flesch"},
	"ttr":                                 {"CMP", "Tokens", "ttr", "Proporção de types (despreza repetições de palavras) em relação à quantidade de tokens (computa repetições de palavras) no texto"},
	"personal_pronouns":                   {"CMP", "Tokens", "personal_pronouns", "Proporção de Pronomes Pessoais em relação à quantidade de palavras do texto"},
	"verbs_ambiguity":                     {"CMP", "Ambiguity", "verbs_ambiguity", "Proporção de sentidos dos verbos do texto em relação à quantidade de verbos do texto"},
	"adjectives_ambiguity":                {"CMP", "Ambiguity", "adjectives_ambiguity", "Proporção de sentidos dos adjetivos do texto em relação à quantidade de adjetivos do texto"},
	"nouns_ambiguity":                     {"CMP", "Ambiguity", "nouns_ambiguity", "Proporção de sentidos dos substantivos do texto em relação à  quantidade de substantivos do texto"},
	"adverbs_ambiguity":                   {"CMP", "Ambiguity", "adverbs_ambiguity", "Proporção de sentidos dos advérbios do texto em relação à  quantidade de advérbios do texto"},
	"mean_noun_phrase":                    {"CMP", "Constituents", "mean_noun_phrase", "Média dos tamanhos médios dos sintagmas nominais nas sentenças"},
	"words_before_main_verb":              {"CMP", "Constituents", "words_before_main_verb", "Quantidade Média de palavras antes dos verbos principais das orações principais das sentenças"},
	"min_cw_freq":                         {"CMP", "Word frequencies", "min_cw_freq", "Média das frequências das palavras de conteúdo mais raras das sentenças do texto"},
	"cw_freq":                             {"CMP", "Word frequencies", "cw_freq", "Média das frequências absolutas das palavras de conteúdo do texto"},
	"brunet":                              {"CMD", "Classic Formulas", "brunet", "Índice de Brunet"},
	"honore":                              {"CMD", "Classic Formulas", "honore", "Estatística de Horoné"},
	"yngve":                               {"CMD", "z", "yngve", "Fórmula de Complexidade Sintática de Yngve"},
	"frazier":                             {"CMD", "z", "frazier", "Fórmula de Complexidade Sintática de Frazier"},
	"dep_distance":                        {"CMD", "z", "dep_distance", "Distância na árvore de dependências"},
	"content_density":                     {"GTN", "z", "content_density", "Proporção de palavras de conteúdo em relação à quantidade de palavras funcionais do texto"},
	"ratio_function_to_content_words":     {"GTN", "z", "ratio_function_to_content_words", "Proporção de palavras funcionais em relação à quantidade de palavras de conteúdo do texto"},
	"apposition_per_clause":               {"AIC", "z", "apposition_per_clause", "Quantidade média de apostos por oração do texto"},
	"clauses_per_sentence":                {"AIC", "z", "clauses_per_sentence", "Quantidade média de orações por sentença"},
	"prepositions_per_clause":             {"AIC", "z", "prepositions_per_clause", "Proporção de preposições em relação à quantidade de orações no texto"},
	"adjunct_per_clause":                  {"AIC", "z", "adjunct_per_clause", "Quantidade média de adjuntos adverbiais por oração do texto"},
	"prepositions_per_sentence":           {"AIC", "z", "prepositions_per_sentence", "Quantidade Média de preposições por sentença no texto"},
	"relative_clauses":                    {"AIC", "z", "relative_clauses", "Proporção de orações relativas em relação à quantidade de orações do texto"},
	"aux_plus_PCP_per_sentence":           {"AIC", "z", "aux_plus_PCP_per_sentence", "Proporção de verbos auxiliares seguidos de particípio em relação à quantidade de sentenças do texto"},
	"coordinate_conjunctions_per_clauses": {"AIC", "z", "coordinate_conjunctions_per_clauses", "Proporção de conjunções coordenativas em relação a todas as orações do texto"},
	"ratio_coordinate_conjunctions":       {"AIC", "z", "ratio_coordinate_conjunctions", "Proporção de conjunções coordenativas em relação a todas as conjunções do texto"},
	"first_person_possessive_pronouns":    {"AIC", "z", "first_person_possessive_pronouns", "Proporção de pronomes possessivos nas primeiras pessoas em relação à quantidade de pronomes possessivos do texto"},
	"first_person_pronouns":               {"AIC", "z", "first_person_pronouns", "Proporção de pronomes pessoais nas primeiras pessoas em relação à quantidade de pronomes pessoais do texto"},
	"gerund_verbs":                        {"AIC", "z", "gerund_verbs", "Proporção de verbos no gerúndio em relação a todos os verbos do texto"},
	"infinitive_verbs":                    {"AIC", "z", "infinitive_verbs", "Proporção de verbos no infinitivo em relação a todos os verbos do texto"},
	"inflected_verbs":                     {"AIC", "z", "inflected_verbs", "Proporção de verbos flexionados em relação a todos os verbos do texto"},
	"non-inflected_verbs":                 {"AIC", "z", "non-inflected_verbs", "Proporção de verbos no gerúndio/particípio/infinitivo em relação a todos os verbos do texto"},
	"participle_verbs":                    {"AIC", "z", "participle_verbs", "Proporção de verbos no particípio em relação a todos os verbos do texto"},
	"passive_ratio":                       {"AIC", "z", "passive_ratio", "Proporção de orações na voz passiva analítica em relação à quantidade de orações do texto"},
	"second_person_possessive_pronouns":   {"AIC", "z", "second_person_possessive_pronouns", "Proporção de pronomes possessivos nas segundas pessoas em relação à quantidade de pronomes possessivos do texto"},
	"second_person_pronouns":              {"AIC", "z", "second_person_pronouns", "Proporção de pronomes pessoais nas segundas pessoas em relação à quantidade de pronomes pessoais do texto"},
	"sentences_with_five_clauses":         {"AIC", "z", "sentences_with_five_clauses", "Proporção de sentenças com 5 orações em relação a todas as sentenças do texto"},
	"sentences_with_four_clauses":         {"AIC", "z", "sentences_with_four_clauses", "Proporção de sentenças com 4 orações em relação a todas as sentenças do texto"},
	"sentences_with_one_clause":           {"AIC", "z", "sentences_with_one_clause", "Proporção de sentenças com 1 oração em relação a todas as sentenças do texto"},
	"sentences_with_seven_more_clauses":   {"AIC", "z", "sentences_with_seven_more_clauses", "Proporção de sentenças com 7 ou mais orações em relação a todas as sentenças do texto"},
	"sentences_with_six_clauses":          {"AIC", "z", "sentences_with_six_clauses", "Proporção de sentenças com 6 orações em relação a todas as sentenças do texto"},
	"sentences_with_three_clauses":        {"AIC", "z", "sentences_with_three_clauses", "Proporção de sentenças com 3 orações em relação a todas as sentenças do texto"},
	"sentences_with_two_clauses":          {"AIC", "z", "sentences_with_two_clauses", "Proporção de sentenças com 2 orações em relação a todas as sentenças do texto"},
	"sentences_with_zero_clause":          {"AIC", "z", "sentences_with_zero_clause", "Proporção de sentenças sem verbos em relação a todas as sentenças do texto"},
	"simple_word_ratio":                   {"AIC", "z", "simple_word_ratio", "Proporção de palavras de conteúdo simples em relação a todas palavras de conteúdo do texto"},
	"ratio_subordinate_conjunctions":      {"AIC", "z", "ratio_subordinate_conjunctions", "Proporção de conjunções subordinativas em relação a todas conjunções do texto"},
	"third_person_possessive_pronouns":    {"AIC", "z", "third_person_possessive_pronouns", "Proporção de pronomes possessivos nas terceiras pessoas em relação à quantidade de pronomes possessivos do texto"},
	"third_person_pronouns":               {"AIC", "z", "third_person_pronouns", "Proporção de pronomes pessoais nas terceiras pessoas em relação à quantidade de pronomes pessoais do texto"},
	"adjective_diversity_ratio":           {"GTN", "z", "adjective_diversity_ratio", "Proporção de types de adjetivos  em relação à quantidade de tokens de adjetivos no texto"},
	"adjectives_max":                      {"GTN", "z", "adjectives_max", "Proporção máxima de adjetivos em relação à quantidade de palavras das sentenças"},
	"adjectives_min":                      {"GTN", "z", "adjectives_min", "Proporção mínima de adjetivos em relação à quantidade de palavras das sentenças"},
	"adjectives_standard_deviation":       {"GTN", "z", "adjectives_standard_deviation", "Desvio padrão das proporções entre adjetivos e a quantidade de palavras das sentenças"},
	"adverbs_diversity_ratio":             {"GTN", "z", "adverbs_diversity_ratio", "Proporção  de types de advérbios em relação à quantidade de tokens de  advérbios no texto"},
	"adverbs_max":                         {"GTN", "z", "adverbs_max", "Proporção máxima de advérbios em relação à quantidade de palavras das sentenças"},
	"adverbs_min":                         {"GTN", "z", "adverbs_min", "Proporção mínima de advérbios em relação à quantidade de palavras das sentenças"},
	"adverbs_standard_deviation":          {"GTN", "z", "adverbs_standard_deviation", "Desvio padrão das proporções entre advérbios e a quantidade de palavras das sentenças"},
	"concretude_mean":                     {"GTN", "Psycholinguistics", "concretude_mean", "Média dos valores de concretude das palavras de conteúdo do texto"},
	"concretude_std":                      {"GTN", "Psycholinguistics", "concretude_std", "Desvio padrão do valor de concretude das palavras de conteúdo do texto"},
	"concretude_1_25_ratio":               {"GTN", "Psycholinguistics", "concretude_1_25_ratio", "Proporção de palavras com valor de concretude entre 1 e 2.5  em relação a todas as palavras de conteúdo do texto"},
	"concretude_25_4_ratio":               {"GTN", "Psycholinguistics", "concretude_25_4_ratio", "Proporção de palavras com valor de concretude entre 2.5  e 4 em relação a todas as palavras de conteúdo do texto"},
	"concretude_4_55_ratio":               {"GTN", "Psycholinguistics", "concretude_4_55_ratio", "Proporção de palavras com valor de concretude entre 4 e 5.5  em relação a todas as palavras de conteúdo do texto"},
	"concretude_55_7_ratio":               {"GTN", "Psycholinguistics", "concretude_55_7_ratio", "Proporção de palavras com valor de concretude entre 5.5 e 7  em relação a todas as palavras de conteúdo do texto"},
	"content_word_diversity":              {"GTN", "z", "content_word_diversity", "Proporção de types de palavras de conteúdo em relação à quantidade de tokens de palavras de conteúdo no texto"},
	"content_word_max":                    {"GTN", "z", "content_word_max", "Proporção máxima de palavras de conteúdo em relação à quantidade de palavras das sentenças"},
	"content_word_min":                    {"GTN", "z", "content_word_min", "Proporção Mínima de palavras de conteúdo por quantidade de palavras nas sentenças"},
	"content_word_standard_deviation":     {"GTN", "z", "content_word_standard_deviation", "Desvio padrão das proporções entre as palavras de conteúdo e a quantidade de palavras das sentenças"},
	"content_words_ambiguity":             {"GTN", "z", "content_words_ambiguity", "Média de sentidos por palavra de conteúdo do texto"},
	"dalechall_adapted":                   {"GTN", "Classic Formulas", "dalechall_adapted", "Fórmula Dale Chall adaptada"},
	"verbal_time_moods_diversity":         {"GTN", "z", "verbal_time_moods_diversity", "Quantidade de diferentes tempos-modos verbais que ocorrem no texto"},
	"easy_conjunctions_ratio":             {"GTN", "z", "easy_conjunctions_ratio", "Proporção de conjunções fáceis em relação à quantidade de palavras do texto"},
	"familiaridade_mean":                  {"GTN", "Psycholinguistics", "familiaridade_mean", "Média dos valores de familiaridade das palavras de conteúdo do texto"},
	"familiaridade_std":                   {"GTN", "Psycholinguistics", "familiaridade_std", "Desvio padrão dos valores de familiaridade das palavras de conteúdo do texto"},
	"familiaridade_1_25_ratio":            {"GTN", "Psycholinguistics", "familiaridade_1_25_ratio", "Proporção de palavras com valor de familiaridade entre 1 e 2.5  em relação a todas as palavras de conteúdo do texto"},
	"familiaridade_25_4_ratio":            {"GTN", "Psycholinguistics", "familiaridade_25_4_ratio", "Proporção de palavras com valor de familiaridade entre 2.5  e 4 em relação a todas as palavras de conteúdo do texto"},
	"familiaridade_4_55_ratio":            {"GTN", "Psycholinguistics", "familiaridade_4_55_ratio", "Proporção de palavras com valor de familiaridade entre 4 e 5.5  em relação a todas as palavras de conteúdo do texto"},
	"familiaridade_55_7_ratio":            {"GTN", "Psycholinguistics", "familiaridade_55_7_ratio", "Proporção de palavras com valor de familiaridade entre 5.5 e 7  em relação a todas as palavras de conteúdo do texto"},
	"function_word_diversity":             {"GTN", "z", "function_word_diversity", "Proporção  de types de palavras funcionais em relação à quantidade de tokens de palavras funcionais no texto"},
	"gunning_fox":                         {"GTN", "Classic Formulas", "gunning_fox", "Índice Gunning Fog"},
	"hard_conjunctions_ratio":             {"GTN", "z", "hard_conjunctions_ratio", "Proporção de conjunções difíceis em relação à quantidade de palavras do texto"},
	"idade_aquisicao_mean":                {"GTN", "Psycholinguistics", "idade_aquisicao_mean", "Média dos valores de idade de aquisição das palavras de conteúdo do texto"},
	"idade_aquisicao_std":                 {"GTN", "Psycholinguistics", "idade_aquisicao_std", "Desvio padrão dos valores de idade de aquisição das palavras de conteúdo do texto"},
	"idade_aquisicao_1_25_ratio":          {"GTN", "Psycholinguistics", "idade_aquisicao_1_25_ratio", "Proporção de palavras com valor de idade de aquisição entre 1 e 2.5 em relação a todas as palavras de conteúdo do texto"},
	"idade_aquisicao_4_55_ratio":          {"GTN", "Psycholinguistics", "idade_aquisicao_4_55_ratio", "Proporção de palavras com valor de idade de aquisição entre 4 e 5.5 em relação a todas as palavras de conteúdo do texto"},
	"idade_aquisicao_55_7_ratio":          {"GTN", "Psycholinguistics", "idade_aquisicao_55_7_ratio", "Proporção de palavras com valor de idade de aquisição entre 5.5 e 7 em relação a todas as palavras de conteúdo do texto"},
	"idade_aquisicao_25_4_ratio":          {"GTN", "Psycholinguistics", "idade_aquisicao_25_4_ratio", "Proporção de palavras com valor de idade de aquisição entre 2.5  e 4 em relação a todas as palavras de conteúdo do texto"},
	"imageabilidade_mean":                 {"GTN", "Psycholinguistics", "imageabilidade_mean", "Média dos valores de imageabilidade das palavras de conteúdo do texto"},
	"imageabilidade_std":                  {"GTN", "Psycholinguistics", "imageabilidade_std", "Desvio padrão dos valores de imageabilidade das palavras de conteúdo do texto"},
	"imageabilidade_1_25_ratio":           {"GTN", "Psycholinguistics", "imageabilidade_1_25_ratio", "Proporção de palavras com valor de imageabilidade entre 1 e 2.5  em relação a todas as palavras de conteúdo do texto"},
	"imageabilidade_25_4_ratio":           {"GTN", "Psycholinguistics", "imageabilidade_25_4_ratio", "Proporção de palavras com valor de imageabilidade entre 2.5  e 4 em relação a todas as palavras de conteúdo do texto"},
	"imageabilidade_4_55_ratio":           {"GTN", "Psycholinguistics", "imageabilidade_4_55_ratio", "Proporção de palavras com valor de imageabilidade entre 4 e 5.5  em relação a todas as palavras de conteúdo do texto"},
	"imageabilidade_55_7_ratio":           {"GTN", "Psycholinguistics", "imageabilidade_55_7_ratio", "Proporção de palavras com valor de imageabilidade entre 5.5 e 7  em relação a todas as palavras de conteúdo do texto"},
	"indefinite_pronouns_diversity":       {"GTN", "z", "indefinite_pronouns_diversity", "Proporção  de types de pronomes indefinidos em relação à quantidade de tokens de  pronomes indefinidos no texto"},
	"medium_long_sentence_ratio":          {"GTN", "z", "medium_long_sentence_ratio", "Proporção de Sentenças Longas em relação a todas as sentenças do texto"},
	"max_noun_phrase":                     {"GTN", "z", "max_noun_phrase", "Máximo entre os tamanhos de sintagmas nominais do texto"},
	"medium_short_sentence_ratio":         {"GTN", "z", "medium_short_sentence_ratio", "Proporção de Sentenças Médias em relação a todas as sentenças do texto"},
	"min_noun_phrase":                     {"GTN", "z", "min_noun_phrase", "Mínimo entre os tamanhos de sintagmas nominais do texto"},
	"named_entity_ratio_sentence":         {"GTN", "z", "named_entity_ratio_sentence", "Média das proporções de Nomes Próprios em relação à quantidade de palavras das Sentenças"},
	"named_entity_ratio_text":             {"GTN", "z", "named_entity_ratio_text", "Proporção de Nomes Próprios em relação à quantidade de palavras do Texto"},
	"noun_diversity":                      {"GTN", "z", "noun_diversity", "Proporção de types de substantivos em relação à quantidade de tokens de  substantivos no texto"},
	"nouns_max":                           {"GTN", "z", "nouns_max", "Proporção máxima de substantivos em relação à quantidade de palavras das sentenças"},
	"nouns_min":                           {"GTN", "z", "nouns_min", "Proporção mínima de substantivos em relação à quantidade de palavras das sentenças"},
	"nouns_standard_deviation":            {"GTN", "z", "nouns_standard_deviation", "Desvio padrão das proporções entre substantivos e a quantidade de palavras das sentenças"},
	"subtitles":                           {"GTN", "z", "subtitles", "Proporção de Subtítulos em relação à quantidade de sentenças do texto"},
	"postponed_subject_ratio":             {"GTN", "z", "postponed_subject_ratio", "Proporção de sujeitos pospostos em relação a todos os sujeitos do texto"},
	"preposition_diversity":               {"GTN", "z", "preposition_diversity", "Proporção  de types de preposições em relação à quantidade de tokens de preposições no texto"},
	"pronoun_diversity":                   {"GTN", "z", "pronoun_diversity", "Proporção de types de pronomes em relação à quantidade de tokens de  pronomes no texto"},
	"pronouns_max":                        {"GTN", "z", "pronouns_max", "Proporção máxima de pronomes em relação à quantidade de palavras das sentenças"},
	"pronouns_min":                        {"GTN", "z", "pronouns_min", "Proporção mínima de pronomes em relação à quantidade de palavras das sentenças"},
	"pronouns_standard_deviation":         {"GTN", "z", "pronouns_standard_deviation", "Desvio padrão das proporções entre pronomes e a quantidade de palavras das sentenças"},
	"dialog_pronoun_ratio":                {"GTN", "z", "dialog_pronoun_ratio", "Proporção de pronomes pessoais que indicam uma conversa com o leitor em relação à quantidade de pronomes pessoais do texto"},
	"punctuation_diversity":               {"GTN", "z", "punctuation_diversity", "Proporção  de types de pontuações em relação à quantidade de tokens de pontuações no texto"},
	"punctuation_ratio":                   {"GTN", "z", "punctuation_ratio", "Proporção de sinais de pontuação em relação à quantidade de palavras do texto"},
	"abstract_nouns_ratio":                {"GTN", "z", "abstract_nouns_ratio", "Proporção de substantivos abstratos em relação à quantidade de palavras do texto"},
	"adverbs_before_main_verb_ratio":      {"GTN", "z", "adverbs_before_main_verb_ratio", "Proporção de orações com advérbio antes do verbo principal em relação à quantidade de orações do texto"},
	"subjunctive_future_ratio":            {"GTN", "z", "subjunctive_future_ratio", "Proporção de Verbos no Futuro do Subjuntivo em relação à quantidade de verbos flexionados no texto"},
	"indefinite_pronoun_ratio":            {"GTN", "z", "indefinite_pronoun_ratio", "Proporção de pronomes indefinidos em relação a todos os pronomes do texto"},
	"indicative_condition_ratio":          {"GTN", "z", "indicative_condition_ratio", "Proporção de Verbos no Futuro do Pretérito do Indicativo em relação à quantidade de verbos flexionados do texto"},
	"indicative_future_ratio":             {"GTN", "z", "indicative_future_ratio", "Proporção de Verbos no Futuro do Presente do Indicativo em relação à quantidade de verbos flexionados do texto"},
	"indicative_imperfect_ratio":          {"GTN", "z", "indicative_imperfect_ratio", "Proporção de Verbos no Pretérito Imperfeito do Indicativo em relação à quantidade de verbos flexionados no texto"},
	"indicative_pluperfect_ratio":         {"GTN", "z", "indicative_pluperfect_ratio", "Proporção de Verbos no Pretérito Mais que Perfeito do Indicativo em relação à quantidade de verbos flexionados no texto"},
	"indicative_present_ratio":            {"GTN", "z", "indicative_present_ratio", "Proporção de Verbos no Presente do Indicativo em relação à quantidade de verbos flexionados no texto"},
	"indicative_preterite_perfect_ratio":  {"GTN", "z", "indicative_preterite_perfect_ratio", "Proporção de Verbos no Pretérito Perfeito Simples do Indicativo em relação à quantidade de verbos flexionados no texto"},
	"infinite_subordinate_clauses":        {"GTN", "z", "infinite_subordinate_clauses", "Proporção de orações subordinadas reduzidas pela quantidade de orações do texto"},
	"oblique_pronouns_ratio":              {"GTN", "z", "oblique_pronouns_ratio", "Proporção de pronomes oblíquos em relação a todos os pronomes do texto"},
	"relative_pronouns_ratio":             {"GTN", "z", "relative_pronouns_ratio", "Proporção de Pronomes Relativos em relação à quantidade de pronomes do texto"},
	"subjunctive_imperfect_ratio":         {"GTN", "z", "subjunctive_imperfect_ratio", "Proporção de Verbos no Pretérito Imperfeito do Subjuntivo em relação à quantidade de verbos flexionados no texto"},
	"subjunctive_present_ratio":           {"GTN", "z", "subjunctive_present_ratio", "Proporção de Verbos no Presente do Subjuntivo em relação à quantidade de verbos flexionados no texto"},
	"subordinate_clauses":                 {"AIC", "z", "subordinate_clauses", "Proporção de orações subordinadas pela quantidade de orações do texto"},
	"temporal_adjunct_ratio":              {"GTN", "z", "temporal_adjunct_ratio", "Proporção de adjuntos adverbiais de tempo em relação a todos os adjuntos adverbiais do texto"},
	"demonstrative_pronoun_ratio":         {"GTN", "z", "demonstrative_pronoun_ratio", "Média de candidatos a referente (na sentença anterior) por pronome demonstrativo anafórico"},
	"coreference_pronoum_ratio":           {"GTN", "z", "coreference_pronoum_ratio", "Média de candidatos a referente (na sentença anterior) por pronome anafórico do caso reto"},
	"non_svo_ratio":                       {"GTN", "z", "non_svo_ratio", "Proporção de orações que não estão no formato SVO (sujeito-verbo-objeto) em relação a todas orações do texto"},
	"relative_pronouns_diversity_ratio":   {"GTN", "z", "relative_pronouns_diversity_ratio", "Proporção  de types de  pronomes relativos  em relação à quantidade de tokens de  pronomes relativos no texto"},
	"sentence_length_max":                 {"GTN", "z", "sentence_length_max", "Quantidade Máxima de palavras por sentença"},
	"sentence_length_min":                 {"GTN", "z", "sentence_length_min", "Quantidade Mínima de palavras por sentença"},
	"sentence_length_standard_deviation":  {"GTN", "z", "sentence_length_standard_deviation", "Desvio Padrão da quantidade de palavras por sentença"},
	"short_sentence_ratio":                {"GTN", "z", "short_sentence_ratio", "Proporção de Sentenças Curtas em relação a todas as sentenças do texto"},
	"std_noun_phrase":                     {"GTN", "z", "std_noun_phrase", "Desvio-padrão do tamanho dos sintagmas nominais do texto"},
	"verb_diversity":                      {"GTN", "z", "verb_diversity", "Proporção de types de verbos em relação à quantidade de tokens de verbos no texto"},
	"verbs_max":                           {"GTN", "z", "verbs_max", "Proporção máxima de advérbios em relação à quantidade de palavras das sentenças"},
	"verbs_min":                           {"GTN", "z", "verbs_min", "Proporção mínima de verbos em relação à quantidade de palavras das sentenças"},
	"negative_words":                      {"LIW", "z", "negative_words", "Proporção de palavras de polaridade negativa em relação a todas palavras do texto"},
	"positive_words":                      {"LIW", "z", "positive_words", "Proporção de palavras de polaridade positiva em relação a todas palavras do texto"},
	"verbs_standard_deviation":            {"GTN", "z", "verbs_standard_deviation", "Desvio padrão das proporções entre advérbios e a quantidade de palavras das sentenças"},
	"long_sentence_ratio":                 {"GTN", "z", "long_sentence_ratio", "Proporção de Sentenças Longas em relação a todas as sentenças do texto"},
	"cw_freq_brwac":                       {"RTS", "Word frequencies", "cw_freq_brwac", "Média dos valores das frequências das palavras de conteúdo do texto na escala logarítmica Zipf via BrWac"},
	"min_cw_freq_brwac":                   {"RTS", "Word frequencies", "min_cw_freq_brwac", "Média dos valores das frequências das palavras de conteúdo do texto na escala logarítmica Zipf via BrWac"},
	"freq_brwac":                          {"RTS", "Word frequencies", "freq_brwac", "Média dos valores das frequências das palavras do texto na escala logarítmica Zipf via BrWac"},
	"min_freq_brwac":                      {"RTS", "Word frequencies", "min_freq_brwac", "Média dos valores das frequências das palavras mais raras das sentenças do texto na escala logarítmica Zipf via BrWac"},
	"cw_freq_bra":                         {"RTS", "Word frequencies", "cw_freq_bra", "Média dos valores das frequências das palavras de conteúdo do texto na escala logarítmica Zipf via Corpus Brasileiro"},
	"min_cw_freq_bra":                     {"RTS", "Word frequencies", "min_cw_freq_bra", "Média dos valores das frequências das palavras de conteúdo mais raras das sentenças do texto na escala logarítmica Zipf via Corpus Brasileiro"},
	"freq_bra":                            {"RTS", "Word frequencies", "freq_bra", "Média dos valores das frequências das palavras do texto na escala logarítmica Zipf via Corpus Brasileiro"},
	"min_freq_bra":                        {"RTS", "Word frequencies", "min_freq_bra", "Média dos valores das frequências das palavras mais raras das sentenças do texto na escala logarítmica Zipf via Corpus Brasileiro"},
	"lsa_adj_mean":                        {"CMD", "LSA", "lsa_adj_mean", "Média de similaridade entre pares de sentenças adjacentes no texto"},
	"lsa_adj_std":                         {"CMD", "LSA", "lsa_adj_std", "Desvio padrão de similaridade entre pares de sentenças adjacentes no texto"},
	"lsa_all_mean":                        {"CMD", "LSA", "lsa_all_mean", "Média de similaridade entre todos os pares de sentenças no texto"},
	"lsa_all_std":                         {"CMD", "LSA", "lsa_all_std", "Desvio padrão de similaridade entre todos os pares possíveis de sentenças do texto"},
	"lsa_givenness_mean":                  {"CMD", "LSA", "lsa_givenness_mean", "Média do *givenness* da cada sentença do texto a partir da segunda"},
	"lsa_givenness_std":                   {"CMD", "LSA", "lsa_givenness_std", "Desvio padrão do *givenness* da cada sentença do texto a partir da segunda"},
	"lsa_paragraph_mean":                  {"CMD", "LSA", "lsa_paragraph_mean", "Média de similaridade entre pares de parágrafos adjacentes no texto"},
	"lsa_paragraph_std":                   {"CMD", "LSA", "lsa_paragraph_std", "Desvio padrão entre parágrafos adjacentes no texto"},
	"lsa_span_mean":                       {"CMD", "LSA", "lsa_span_mean", "Média do *span* da cada sentença do texto a partir da segunda"},
	"lsa_span_std":                        {"CMD", "LSA", "lsa_span_std", "Desvio padrão do span da cada sentença do texto a partir da segunda"},
	"cross_entropy":                       {"CMD", "Language Model", "cross_entropy", "Média da entropia cruzadas das sentenças do texto"},
}

type MetrixResultItem struct {
	Index       int    `json:"i"`
	Metric      string `json:"k"`
	Class       string `json:"c"`
	Source      string `json:"s"`
	Value       string `json:"v"`
	Description string `json:"d"`
}

type MetrixResultOrder []MetrixResultItem

func (a MetrixResultOrder) Len() int      { return len(a) }
func (a MetrixResultOrder) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
func (a MetrixResultOrder) Less(i, j int) bool {
	if a[i].Class == a[j].Class {
		return a[i].Metric < a[j].Metric
	}
	return a[i].Class < a[j].Class
}

type PageInfo struct {
	Version             string                      `json:"version"`
	StaticHash          string                      `json:"shash"`
	MetricList          []MetrixResultItem          `json:"metric_list"`
	SimpligoRankingList []SimpligoRankingResultItem `json:"simpligo_list"`
	ShowResults         bool                        `json:"show_res"`
	Text                string                      `json:"text"`
	Message             string                      `json:"msg"`
	ShowMessage         bool                        `json:"show_msg"`
}

var pageInfo PageInfo

func initialize() {

	pageInfo = PageInfo{}
	pageInfo.Version = "0.0.1"
	pageInfo.StaticHash = "007"

}

func finalize() {
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))
	r.HandleFunc("/", indexHandler)
	r.HandleFunc("/metrixdoc", metrixDocHandler)
	r.HandleFunc("/cohmetrixport", cohMetrixPortHandler)
	r.HandleFunc("/nilcmetrix", nilcMetrixHandler)
	r.HandleFunc("/simpligo-ranking", simpligoRankingHandler)
	r.HandleFunc("/api/v1/metrix/{subset}/{key}", metricsHandler).Methods("POST")
	r.HandleFunc("/api/v1/palavras/{retType}/{key}", palavrasHandler)

	return r
}

func main() {

	initialize()

	var httpSrv *http.Server
	httpSrv = makeHTTPServer()

	httpSrv.Addr = ":8080"
	fmt.Printf("Starting HTTP server on %s\n", httpSrv.Addr)
	err := httpSrv.ListenAndServe()
	if err != nil {
		log.Fatalf("httpSrv.ListenAndServe() failed with %s", err)
	}

	defer finalize()

}

func makeHTTPServer() *http.Server {
	mux := Router()
	return &http.Server{
		ReadTimeout:  300 * time.Second,
		WriteTimeout: 300 * time.Second,
		IdleTimeout:  360 * time.Second,
		Handler:      mux,
	}
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	templateHandler(w, r, "index", pageInfo)
}

func metrixDocHandler(w http.ResponseWriter, r *http.Request) {
	templateHandler(w, r, "metrixdoc", pageInfo)
}

func cohMetrixPortHandler(w http.ResponseWriter, r *http.Request) {

	pInfo := pageInfo
	pInfo.ShowResults = false

	text := r.FormValue("text")

	if text != "" {

		nWords := strings.Count(text, " ") + 1
		if nWords > 2000 {
			ret := "Text is too big."
			log.Println(ret)
			pInfo.Message = ret
			pInfo.ShowMessage = true

		} else {

			_, list, err := callMetrix("port", text)
			if err != nil {
				log.Println(err)
				w.WriteHeader(http.StatusInternalServerError)
				fmt.Fprint(w, "Error "+err.Error())
				return
			}

			sort.Sort(MetrixResultOrder(list))

			for i, it := range list {
				if it.Source == "CMP" {
					it.Index = i + 1
					pInfo.MetricList = append(pInfo.MetricList, it)
				}
			}

			pInfo.ShowResults = true
			pInfo.Text = text
		}
	}

	templateHandler(w, r, "cohmetrixport", pInfo)
}

func nilcMetrixHandler(w http.ResponseWriter, r *http.Request) {

	pInfo := pageInfo
	pInfo.ShowResults = false

	text := r.FormValue("text")

	if text != "" {

		nWords := strings.Count(text, " ") + 1
		if nWords > 2000 {
			ret := "Text is too big."
			log.Println(ret)
			pInfo.Message = ret
			pInfo.ShowMessage = true

		} else {

			_, list, err := callMetrix("_all", text)
			if err != nil {
				log.Println(err)
				w.WriteHeader(http.StatusInternalServerError)
				fmt.Fprint(w, "Error "+err.Error())
				return
			}

			sort.Sort(MetrixResultOrder(list))

			for i, it := range list {
				it.Index = i + 1
				pInfo.MetricList = append(pInfo.MetricList, it)
			}

			pInfo.ShowResults = true
			pInfo.Text = text
		}
	}

	templateHandler(w, r, "nilcmetrix", pInfo)
}

func templateHandler(w http.ResponseWriter, r *http.Request, pageName string, pInfo PageInfo) {
	t, err := template.New(pageName+".html").Delims("[[", "]]").ParseFiles("./templates/" + pageName + ".html")
	if err != nil {
		fmt.Fprintf(w, "Error openning template: %v", err)
	}

	err = t.Execute(w, pInfo)
	if err != nil {
		fmt.Fprintf(w, "Error parsing template: %v.", err)
	}

}

func metricsHandler(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	subset := vars["subset"]

	if subset == "all" {
		subset = "_all"
	}

	key := vars["key"]

	if key != "token-here" {
		w.WriteHeader(http.StatusForbidden)
		return
	}

	retFormat := r.FormValue("format")
	if retFormat == "plain" {
		w.Header().Set("Content-Type", "text")
	} else {
		w.Header().Set("Content-Type", "application/json")
	}

	ret := ""

	defer r.Body.Close()
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		ret += "Error reading req: %v." + err.Error()
		log.Println(ret)
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, ret)
		return
	}

	text := string(body)
	ret += text + "\n"
	ret += "-------------------------------" + "\n"

	nWords := strings.Count(text, " ") + 1
	if nWords > 2000 {
		ret = "Text is too big."
		log.Println(ret)
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, ret)
		return
	}

	plain, list, err := callMetrix(subset, text)
	if err != nil {
		ret += "Error " + err.Error()
		log.Println(ret)
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, ret)
		return
	}

	if retFormat == "plain" {
		ret += plain
	} else {
		ret = metrixResultToJSON(list)
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(ret))
}

func metrixResultToJSON(list []MetrixResultItem) string {
	ret := "{"
	for _, item := range list {
		ret += "\"" + item.Metric + "\":" + item.Value + ","
	}
	ret = strings.TrimSuffix(ret, ",")
	ret += "}"
	return ret
}

func callMetrix(subset string, text string) (string, []MetrixResultItem, error) {
	shellOut, err := execShellMetrix(subset, text)
	if err != nil {
		return "", []MetrixResultItem{}, err
	}

	list := shellOutToList(shellOut)

	return shellOut, list, nil
}

func preProc(text string) string {
	text = strings.Replace(text, "\"", "{{quotes}}", -1)
	text = strings.Replace(text, "“", "{{quotes}}", -1)
	text = strings.Replace(text, "”", "{{quotes}}", -1)
	text = strings.Replace(text, "\r\n", "{{enter}}", -1)
	text = strings.Replace(text, "\n", "{{enter}}", -1)
	text = strings.Replace(text, "!", "{{exclamation}}", -1)
	text = strings.Replace(text, "#", "{{sharp}}", -1)
	text = strings.Replace(text, "&", "{{ampersand}}", -1)
	text = strings.Replace(text, "%", "{{percent}}", -1)
	text = strings.Replace(text, "$", "{{dollar}}", -1)
	text = strings.Replace(text, "è", "e", -1)
	text = strings.Replace(text, "ì", "i", -1)
	text = strings.Replace(text, "ò", "o", -1)
	text = strings.Replace(text, "ù", "u", -1)
	text = strings.Replace(text, "`", "\"", -1)
	text = strings.Replace(text, "´", "\"", -1)

	text = strings.Replace(text, " à ", "{{crase}}", -1)
	text = strings.Replace(text, "à", "a", -1)
	text = strings.Replace(text, "{{crase}}", " à ", -1)
	return text
}

func execShellMetrix(subset string, text string) (string, error) {
	log.Println("/bin/bash", "-c", "python3 /opt/text_metrics/run"+subset+".py \""+text+"\"")

	text = preProc(text)

	cmd := exec.Command("/bin/bash", "-c", "python3 /opt/text_metrics/run"+subset+".py \""+text+"\"")
	out, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("cmd.Run() failed with %v", err.Error())
	}
	fmt.Printf("combined out:\n%s\n", string(out))
	return string(out), nil
}

func shellOutToList(shellOut string) []MetrixResultItem {
	list := []MetrixResultItem{}

	out := strings.Split(shellOut, "++")
	if len(out) < 2 {
		return list
	}
	feats := strings.Split(strings.TrimSpace(out[1]), ",")

	for i, feat := range feats {
		kv := strings.Split(feat, ":")
		if len(kv) > 1 {
			if metric, found := metricMap[kv[0]]; found {
				list = append(list, MetrixResultItem{i, metric.Key, metric.Class, metric.Source, kv[1], metric.Desc})
			} else {
				list = append(list, MetrixResultItem{i, kv[0], "", "", kv[1], ""})
			}
		}
	}
	return list
}

func palavrasHandler(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	retType := vars["retType"]

	if retType != "tigerxml" && retType != "flat" {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	key := vars["key"]
	if key != "m3tr1x01" {
		w.WriteHeader(http.StatusForbidden)
		return
	}

	content := r.FormValue("content")
	options := r.FormValue("options")

	resp, err := http.PostForm("http://palavras:8080/palavras/"+retType,
		url.Values{"sentence": {content}, "options": {options}})
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Printf("Error: %v\n", err)
		return
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(fmt.Errorf("Error reading response: %v", err))
	}

	bodyString := string(body)
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "text")
	fmt.Fprint(w, bodyString)

}
