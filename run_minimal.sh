#!/bin/bash
docker run --rm --link pgs_cohmetrix:pgs_cohmetrix -v /home/sidney/Downloads/nilcmetrix:/opt/text_metrics cohmetrix:focal bash -c "python3 run_min.py \"$1\""
