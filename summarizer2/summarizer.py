from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as LSASummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.kl import KLSummarizer



from sumy.summarizers.lex_rank import LexRankSummarizer

from sumy.nlp.stemmers import Stemmer, null_stemmer
from sumy.utils import get_stop_words



def createSummary (text, language="english", num_sentences=3, method="lexrank"):
    #LANGUAGE = "english"
    #SENTENCES_COUNT = 5
    # url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    

    # Language tokenizer
    tokenizer = Tokenizer(language)
    parser = PlaintextParser.from_string(text, tokenizer)
    # word stemming
    stemmer = Stemmer(language)

    if (method == "lexrank"):
        summarizer = LexRankSummarizer(stemmer)
    elif (method == "lsa"):
        summarizer = LSASummarizer(stemmer)
    elif (method == "luhn"):
        summarizer = LuhnSummarizer(stemmer)
    elif (method == "kl"):
        summarizer = KLSummarizer(stemmer)
    else:
        raise Exception (f'Unknown summarization method: ${method}')

    summarizer.stop_words = get_stop_words(language)

    result = []
    for sentence in summarizer(parser.document, num_sentences):
        result.append (str(sentence))
    
    return result

