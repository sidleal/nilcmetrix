#!/bin/bash
docker run --rm --link pgs_cohmetrix:pgs_cohmetrix --link palavras:palavras -v /home/sidleal/coh-metrix-nilc:/opt/text_metrics cohmetrix:focal bash -c "python3 run_all.py \"$1\""
