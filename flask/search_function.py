from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from collections import defaultdict
from nltk.corpus import stopwords
from math import log
import string
import json


def score_BM25(n, qf, N, dl, avdl):
    k1 = 2.0
    b = 0.75
    K = compute_K(dl, avdl, k1, b)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    return IDF * frac


def compute_K(dl, avdl, k1, b):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))


def get_indices():
    with open('inverted_index.json','r',encoding='utf-8-sig') as f:
        inverted_index = json.loads(f.read())
    with open('article_info.json','r',encoding='utf-8-sig') as f:
        articles = json.loads(f.read())
    with open('average_article_length.txt','r',encoding='utf-8-sig') as f:
        avdl = float(f.read())
    return inverted_index,articles,avdl


def search(query):
    relevance = defaultdict(float)
    m = MorphAnalyzer()
    inverted_index,articles,avdl = get_indices()
    N = len(articles)
    words = [x.lower().strip(string.punctuation+'»«–…') for x in word_tokenize(query)]
    lemmas = [m.parse(x)[0].normal_form for x in words
              if x and x not in set(stopwords.words('russian'))]
    for lemma in lemmas:
        if lemma in inverted_index:
            articles_w_lemma = inverted_index[lemma]
            n = len(articles_w_lemma)
            for a in articles_w_lemma:
                a_info = articles[a[0]]
                qf = a[1]
                dl = a_info[2]
                relevance[(a_info[0],a_info[1])] += score_BM25(n, qf, N, dl, avdl)
    res = sorted(relevance.items(),key=lambda x: x[1],reverse=True)
    res = [x[0] for x in res]
    return res

        
