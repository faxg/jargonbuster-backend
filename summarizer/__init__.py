import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

from summarizer.lsa_summarizer import LsaSummarizer
from summarizer.base_summarizer import BaseSummarizer
