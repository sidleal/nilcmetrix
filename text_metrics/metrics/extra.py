from __future__ import unicode_literals, print_function, division

from text_metrics import base
from text_metrics.resource_pool import rp as default_rp
from text_metrics.utils import ilen
from text_metrics.tools import syllable_separator, pos_tagger


class RatioFunctionToContentWords(base.Metric):
    """
    ## Inverso da Densidade de Conteúdo (content density).
    """

    name = 'Ratio of function words to content words'
    column_name = 'ratio_function_to_content_words'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        return ilen(function_words) / ilen(content_words)


class EXTRA(base.Category):
    name = 'EXTRA'
    table_name = 'extra'

    def __init__(self):
        super(EXTRA, self).__init__()
        self._set_metrics_from_module(__name__)
        # self.metrics = [m for m in self.metrics if m.name != 'AnaphoricReferencesBase']
        self.metrics.sort(key=lambda m: m.name)
