import re
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as nltk_stopwords

nltk.download('stopwords')

class StandardPipeline:
    def __init__(self,stopwords=STOP_WORDS):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.disable_pipes("ner")
    def __call__(self, doc):
        doc = self.nlp(doc)
        return [token._lemma for token in doc if not token in stopwords and not token.is_punct]


class StemTokenizer:
    def __init__(self, stopwords=nltk_stopwords.words('english'),stemmer=PorterStemmer,lemmatizer=None):
        self.tokenizer = re.compile(r"\w\w+")
        self.stopwords = set(stopwords)
        self.stemmer = stemmer
        self.lemmatizer = lemmatizer
    def __call__(self, doc):
        tokens = self.tokenizer.findall(doc)
        tokens = [self.stemmer.stem(t) for t in tokens if not t in self.stopwords]
        if lemmatizer != None:
            tokens = [self.lemmatizer.lemmatize(t) for t in token ]
        return tokens












