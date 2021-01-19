# -*- coding: utf-8 -*-
import text_metrics
import datetime
import os

print(datetime.datetime.now())

feat_list = ["adjective_ratio", "adverbs", "content_words", "flesch", "function_words", "sentences_per_paragraph", "syllables_per_content_word", "words_per_sentence", "noun_ratio", "paragraphs", "sentences", "words", "pronoun_ratio", "verbs", "logic_operators", "and_ratio", "if_ratio", "or_ratio", "negation_ratio", "cw_freq", "min_cw_freq", "hypernyms_verbs", "brunet", "honore", "personal_pronouns", "ttr", "conn_ratio", "add_neg_conn_ratio", "add_pos_conn_ratio", "cau_neg_conn_ratio", "cau_pos_conn_ratio", "log_neg_conn_ratio", "log_pos_conn_ratio", "tmp_neg_conn_ratio", "tmp_pos_conn_ratio", "adjectives_ambiguity", "adverbs_ambiguity", "nouns_ambiguity", "verbs_ambiguity", "yngve", "frazier", "dep_distance", "content_density", "words_before_main_verb", "adjacent_refs", "anaphoric_refs", "adj_arg_ovl", "arg_ovl", "adj_stem_ovl", "stem_ovl", "adj_cw_ovl", "adj_mean", "adj_std", "all_mean", "all_std", "paragraph_mean", "paragraph_std", "givenness_mean", "givenness_std", "span_mean", "span_std", "apposition_per_clause", "clauses_per_sentence", "prepositions_per_clause", "adjunct_per_clause", "prepositions_per_sentence", "relative_clauses", "aux_plus_PCP_per_sentence", "coordinate_conjunctions_per_clauses", "ratio_coordinate_conjunctions", "first_person_possessive_pronouns", "first_person_pronouns", "gerund_verbs", "infinitive_verbs", "inflected_verbs", "non-inflected_verbs", "participle_verbs", "passive_ratio", "second_person_possessive_pronouns", "second_person_pronouns", "sentences_with_five_clauses", "sentences_with_four_clauses", "sentences_with_one_clause", "sentences_with_seven_more_clauses", "sentences_with_six_clauses", "sentences_with_three_clauses", "sentences_with_two_clauses", "sentences_with_zero_clause", "simple_word_ratio", "ratio_subordinate_conjunctions", "third_person_possessive_pronouns", "third_person_pronouns", "adjective_diversity_ratio", "adjectives_max", "adjectives_min", "adjectives_standard_deviation", "adverbs_diversity_ratio", "adverbs_max", "adverbs_min", "adverbs_standard_deviation", "concretude_mean", "concretude_std", "concretude_1_25_ratio", "concretude_25_4_ratio", "concretude_4_55_ratio", "concretude_55_7_ratio", "content_word_diversity", "content_word_max", "content_word_min", "content_word_standard_deviation", "content_words_ambiguity", "dalechall_adapted", "verbal_time_moods_diversity", "easy_conjunctions_ratio", "familiaridade_mean", "familiaridade_std", "familiaridade_1_25_ratio", "familiaridade_25_4_ratio", "familiaridade_4_55_ratio", "familiaridade_55_7_ratio", "function_word_diversity", "gunning_fox", "hard_conjunctions_ratio", "idade_aquisicao_mean", "idade_aquisicao_std", "idade_aquisicao_1_25_ratio", "idade_aquisicao_4_55_ratio", "idade_aquisicao_55_7_ratio", "idade_aquisicao_25_4_ratio", "imageabilidade_mean", "imageabilidade_std", "imageabilidade_1_25_ratio", "imageabilidade_25_4_ratio", "imageabilidade_4_55_ratio", "imageabilidade_55_7_ratio", "indefinite_pronouns_diversity", "medium_long_sentence_ratio", "max_noun_phrase", "mean_noun_phrase", "medium_short_sentence_ratio", "min_noun_phrase", "named_entity_ratio_sentence", "named_entity_ratio_text", "noun_diversity", "nouns_max", "nouns_min", "nouns_standard_deviation", "subtitles", "postponed_subject_ratio", "preposition_diversity", "pronoun_diversity", "pronouns_max", "pronouns_min", "pronouns_standard_deviation", "dialog_pronoun_ratio", "punctuation_diversity", "punctuation_ratio", "abstract_nouns_ratio", "adverbs_before_main_verb_ratio", "subjunctive_future_ratio", "indefinite_pronoun_ratio", "indicative_condition_ratio", "indicative_future_ratio", "indicative_imperfect_ratio", "indicative_pluperfect_ratio", "indicative_present_ratio", "indicative_preterite_perfect_ratio", "infinite_subordinate_clauses", "oblique_pronouns_ratio", "relative_pronouns_ratio", "subjunctive_imperfect_ratio", "subjunctive_present_ratio", "subordinate_clauses", "temporal_adjunct_ratio", "demonstrative_pronoun_ratio", "coreference_pronoum_ratio", "non_svo_ratio", "relative_pronouns_diversity_ratio", "sentence_length_max", "sentence_length_min", "sentence_length_standard_deviation", "short_sentence_ratio", "std_noun_phrase", "verb_diversity", "verbs_max", "verbs_min", "verbs_standard_deviation", "long_sentence_ratio", "ratio_function_to_content_words"]
#feat_list_79 = ["adjective_ratio", "adverbs", "syllables_per_content_word", "words_per_sentence", "noun_ratio", "pronoun_ratio", "verbs", "negation_ratio", "cw_freq", "min_cw_freq", "first_person_pronouns", "ttr", "conn_ratio", "add_neg_conn_ratio", "add_pos_conn_ratio", "cau_neg_conn_ratio", "cau_pos_conn_ratio", "log_neg_conn_ratio", "log_pos_conn_ratio", "tmp_neg_conn_ratio", "tmp_pos_conn_ratio", "adjectives_ambiguity", "adverbs_ambiguity", "nouns_ambiguity", "verbs_ambiguity", "yngve", "frazier", "dep_distance", "words_before_main_verb", "mean_noun_phrase", "min_noun_phrase", "max_noun_phrase", "std_noun_phrase", "passive_ratio", "adj_arg_ovl", "arg_ovl", "adj_stem_ovl", "stem_ovl", "adj_cw_ovl", "third_person_pronouns", "concretude_mean", "concretude_std", "concretude_1_25_ratio", "concretude_25_4_ratio", "concretude_4_55_ratio", "concretude_55_7_ratio", "content_word_diversity", "familiaridade_mean", "familiaridade_std", "familiaridade_1_25_ratio", "familiaridade_25_4_ratio", "familiaridade_4_55_ratio", "familiaridade_55_7_ratio", "idade_aquisicao_mean", "idade_aquisicao_std", "idade_aquisicao_1_25_ratio", "idade_aquisicao_4_55_ratio", "idade_aquisicao_55_7_ratio", "idade_aquisicao_25_4_ratio", "imageabilidade_mean", "imageabilidade_std", "imageabilidade_1_25_ratio", "imageabilidade_25_4_ratio", "imageabilidade_4_55_ratio", "imageabilidade_55_7_ratio", "sentence_length_max", "sentence_length_min", "sentence_length_standard_deviation", "verb_diversity", "adj_mean", "adj_std", "all_mean", "all_std", "givenness_mean", "givenness_std", "span_mean", "span_std", "content_density", "ratio_function_to_content_words"]

for dirname, dirnames, filenames in os.walk('/opt/text_metrics/porsimples_text_all'):
    for filename in filenames:
        # filename = filename.replace("\udcc2", "")
        # filename = filename.replace("\udcba", "")

        file_path = os.path.join(dirname, filename)
        metric_path = file_path.replace(".txt", ".metrix")
        print(datetime.datetime.now())
        print(file_path)
        print(metric_path)

        if not os.path.isfile(metric_path):

            f_text = open(file_path, "r", encoding="windows-1252")
            text = ""
            for line in f_text:
                text += line
            f_text.close()

            dest = open(metric_path, "w", encoding="utf-8")

            t = text_metrics.Text(text)
            ret = text_metrics.all_metrics.values_for_text(t).as_flat_dict()
            nret = {}
            for k,v in ret.items():
                nret[k.replace(" ", "_")] = v 
                
            for f in feat_list:
                dest.write("%s:\t%s\n" % (f, nret[f]))

            dest.close()

