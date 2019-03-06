#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:18:32 2019

@author: swarnadeep
"""

from __future__ import print_function
import sklearn
# Import all of the scikit learn stuff
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
import pandas as pd
import warnings
# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning,
module="pandas", lineno=570)
import numpy
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) 
import os
import string

def get_files(dir_path):
    files = []
    for file in os.listdir(dir_path):
        files.append(file)
    return files

#check if the string is impure or not
def isImpure(word):
    flag = False
    for index in range(len(word)):
        if word[index] in string.punctuation:
            flag = True
        elif word[index].isdigit():
            flag = True
    return flag

sentences = []
def splitNumbersAndUnits(text):
    term_list = word_tokenize(text)
    #print(term_list)
    new_term = ""
    change_terms = {}
    problem = []
    pos = 0
    for term in term_list:
        if term[0].isdigit():
            #print(term)
            problem.append(term)
    for word in problem:
        for i in range(0,len(word)):
            #print(word[i])
            if not word[i].isdigit():
                pos = i
                #print(pos)
                break
        #print(word[:pos])
        #print(word[pos:])
        new_term = word[:pos] + " " + word[pos:]
        change_terms[word] = new_term
        #print(new_term)
    #print(change_terms)
    new_text = ""
    for term in term_list:
        if term in change_terms.keys():
            new_text = new_text + " " + change_terms[term]
        else:
            new_text = new_text + " " + term
    return new_text


def extract_words(text,unique_words):
    text.translate(string.punctuation) 
    words = text.split() 
    for r in words: 
        if not r in stop_words:
            if not isImpure(r) and len(r) > 3:
                unique_words[r] = 0

file_names = []

def create_corpus_to_pass(dir_path):
    files = get_files(dir_path)
    #sentences = []
    vocab = ""
    unique_words = {}
    for file in files:
        file_path = dir_path + "/" + file
        file_names.append(file)
        fp = open(file_path,"r")
        file_content = fp.read()
        file_content = splitNumbersAndUnits(file_content)
        extract_words(file_content,unique_words)
        for keys in unique_words.keys():
            vocab = vocab + " " + keys
        sentences.append(vocab)
        unique_words = {}
        vocab = ""
        #print(sentences)

create_corpus_to_pass("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")
#create the term document matrix
vectorizer = TfidfVectorizer(min_df=1,stop_words='english')
dtm = vectorizer.fit_transform(sentences)
print(type(dtm))
#print(dtm.shape)
dtm = dtm.transpose(copy=False)
print(dtm.shape)
pd.DataFrame(dtm.toarray(),index=vectorizer.get_feature_names(),columns=file_names).head(10)
print(len(vectorizer.get_feature_names()))
#fit lsa
#use algorithm randomized for large datasets
lsa = TruncatedSVD(150,algorithm='randomized')#150 is the size of the of each word
dtm_lsa = lsa.fit_transform(dtm)
dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)
print(type(dtm_lsa))
data_embeddings = pd.DataFrame(dtm_lsa,index=vectorizer.get_feature_names())
print(type(data_embeddings))
sample_embedded = data_embeddings.loc[ 'able' , : ]
#print(sample_embedded)
#generate embedding dictionary
embedding = {}
for word in vectorizer.get_feature_names():
    embedding[word] = data_embeddings.loc[ word , : ]
    
print(embedding)