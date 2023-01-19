import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as nltk_stopwords


class StandardPipeline:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.disable_pipes("ner")
        self.stop_words = STOP_WORDS
        self.enable_lemmatizer = False

    def __call__(self, doc):
        doc = self.nlp(doc)
        if self.enable_lemmatizer:
            return [token.lemma_ for token in doc
                    if not token in self.stop_words and not token.is_alpha]
        return [token for token in doc
                if not token in self.stop_words and token.is_alpha]


class StemTokenizer:
    def __init__(self, regex=r"\w\w+"):
        self.tokenizer = re.compile(regex)
        self.stopwords = set(nltk_stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.enable_lemmatizer = False
        self.lemmatizer = None

    def __call__(self, doc):
        tokens = self.tokenizer.findall(doc)
        tokens = [self.stemmer.stem(t)
                  for t in tokens if not t in self.stopwords]
        if self.enable_lemmatizer:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        return tokens
