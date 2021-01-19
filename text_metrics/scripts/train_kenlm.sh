#!/bin/sh

KENLM_PATH=$HOME/Develop/kenlm/
CORPORA_PATH=$HOME/Develop/corpora/

$KENLM_PATH/bin/lmplz -o 3 -S 50% -T /tmp \
 < $CORPORA_PATH/ngram_corpus_clean.txt \
 | gzip > $CORPORA_PATH/corpus_3gram.arpa.gz
