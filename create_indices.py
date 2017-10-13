from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import string
import json
import os
import re


def inv_index(collection):
    inv_idx = defaultdict(list)
    for i,c in collection.items():
        counter_c = Counter(c)
        for word,freq in counter_c.items():
            inv_idx[word].append((i,freq))
    return inv_idx


extract_text = re.compile('\n([^@][^a-z].*$)',flags=re.DOTALL)
extract_link = re.compile('@url (.*)')
extract_title = re.compile('@ti (.*)')

m = MorphAnalyzer()
collection = {}
article_info = {}
avdl = 0

articles = os.listdir('./articles')
for article in articles:
    if article.endswith('.txt'):
        with open('./articles/'+article,'r',encoding='utf-8-sig') as f:
            all_text = f.read()
        link = extract_link.search(all_text).group(1)
        title = extract_title.search(all_text).group(1)
        text = extract_text.search(all_text)
        if text is not None:
            text = text.group(1)
            words = [x.lower().strip(string.punctuation+'»«–…') for x in word_tokenize(text)]
            lemmas = [m.parse(x)[0].normal_form for x in words if x and x not in set(stopwords.words('russian'))]
            collection[article] = lemmas
            article_info[article] = (link,title,len(lemmas))
            avdl += len(lemmas)

inverted_index = inv_index(collection)
avdl = avdl / len(collection)

with open('inverted_index.json','w',encoding='utf-8-sig') as f:
    s = json.dumps(inverted_index,ensure_ascii=False)
    f.write(s)
    
with open('article_info.json','w',encoding='utf-8-sig') as f:
    s = json.dumps(article_info,ensure_ascii=False,indent=2)
    f.write(s)
    
with open('average_article_length.txt','w',encoding='utf-8-sig') as f:
    f.write(str(avdl))
        
