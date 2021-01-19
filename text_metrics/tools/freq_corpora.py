from __future__ import unicode_literals, print_function, division

import math

from text_metrics.conf import config
import codecs

# Word frequencies were calculated on the Zipf scale, based on the SUBTLEX-UK corpus
# (Van Heuven, Mandera, Keuleers, & Brysbaert, 2014). The Zipf scale is logarithmic, ranging
# from very low (Zipf value 1) to very high (Zipf value 7) frequency words; it is calculated
# as log10 (frequency per million words) + 3, or equivalently log10 (frequency per billion words).

brwac_size = 2691373903

def brwac_frequencies():
    with codecs.open(config['FREQUENCIES_BRWAC'], encoding='utf-8') as f:
        ret = {}
        for line in f.readlines():
            key = ('%s_%s' % (line.split('\t')[0], line.split('\t')[2][0:-1])).lower()
            val = int(line.split('\t')[1])
            norm_freq = val * 1000000 / brwac_size
            log_freq = round(math.log(norm_freq, 10) + 3, 3)
            ret[key] = log_freq
        return ret


brasileiro_size = 871117178

def brasileiro_frequencies():
    with codecs.open(config['FREQUENCIES_BRASILEIRO'], encoding='utf-8') as f:
        ret = {}
        for line in f.readlines():
            key = '%s' % line.split('\t')[0].lower()
            val = int(line.split('\t')[1])
            if key in ret:
                ret[key] += val
            else:
                ret[key] = val

        for k, v in ret.items():
            norm_freq = v * 1000000 / brasileiro_size
            log_freq = round(math.log(norm_freq, 10) + 3, 3)
            ret[k] = log_freq

        return ret
