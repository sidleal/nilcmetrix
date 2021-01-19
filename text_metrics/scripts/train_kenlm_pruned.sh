#!/bin/sh

KENLM_PATH=$HOME/Develop/kenlm/
CORPORA_PATH=$HOME/Develop/corpora/

$KENLM_PATH/bin/lmplz -o 3 -S 40% -T /tmp --prune 0 0 1 \
 < $CORPORA_PATH/ngram_corpus_clean.txt \
 > $CORPORA_PATH/corpus_3gram_pruned.arpa

$KENLM_PATH/bin/build_binary \
        $CORPORA_PATH/corpus_3gram_pruned.arpa \
        $CORPORA_PATH/corpus_3gram_pruned.binary

rm $CORPORA_PATH/corpus_3gram_pruned.arpa
