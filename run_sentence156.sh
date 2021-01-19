#!/bin/bash
docker run --rm --name cohmetrix --link pgs_cohmetrix:pgs_cohmetrix -v /home/sidleal/coh-metrix-nilc:/opt/text_metrics cohmetrix bash -c "python3 run156.py \"$1\""
