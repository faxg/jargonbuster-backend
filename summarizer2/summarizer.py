from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as LSASummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as LexRankSummarizer

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words



def createSummary (text, language="english", num_sentences=5, method="lexrank"):
    #LANGUAGE = "english"
    #SENTENCES_COUNT = 5
    # url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    
    tokenizer = Tokenizer(language)
    parser = PlaintextParser.from_string(text, tokenizer)
    
    stemmer = Stemmer(language)

    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    result = []
    for sentence in summarizer(parser.document, num_sentences):
        result.append (str(sentence))
    
    return result

