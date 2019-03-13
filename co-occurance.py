#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 18:48:23 2019

@author: swarnadeep
"""

import numpy as np 
import nltk
from nltk import bigrams
import pandas as pd
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) 
import os
import string
from sklearn.decomposition import TruncatedSVD

vocab=[]
corpus=[]

collocation_matrix = {}
vocabulary={}
#return the names of files in the dictionary
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

def extract_words(text):
    text.translate(string.punctuation) 
    words = text.split()
    curr_words=[]
    for r in words: 
        if not r in stop_words:
            if not isImpure(r) and len(r) > 3:
                curr_words.append(r)
                vocabulary[r]=1
    return curr_words

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



def create_corpus(dir_path):
    files = get_files(dir_path)
    for file in files:
        file_path = dir_path + "/" + file
        fp = open(file_path,"r")
        file_content = fp.read()
        file_content = splitNumbersAndUnits(file_content)
        words=extract_words(file_content)
        for word in words:
            corpus.append(word)
        print(words,end=' ')
        #co_occurrence_matrix(file_content)

def make_co_occurrence_matrix(corpus):
    # Create bigrams from all words in corpus
    bi_grams = list(bigrams(corpus))
    # Frequency distribution of bigrams ((word1, word2), num_occurrences)
    bigram_freq = nltk.FreqDist(bi_grams).most_common(len(bi_grams))
    # Loop through the bigrams in the frequency distribution, noting the 
    # current and previous word, and the number of occurrences of the bigram.
    # Get the vocab index of the current and previous words.
    # Put the number of occurrences into the appropriate element of the array.
    for bigram in bigram_freq:
        current = bigram[0][1]
        previous = bigram[0][0]
        count = bigram[1]
        pos_current = vocab_to_index[current]
        pos_previous = vocab_to_index[previous]
        co_occurrence_matrix[pos_current][pos_previous] = count 

create_corpus("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")
#print(corpus)
for keys in vocabulary:
    vocab.append(keys)
#print(len(vocab))
vocab_to_index = { word:i for i, word in enumerate(vocab) }
#print(vocab_to_index)
co_occurrence_matrix = np.zeros((len(vocab), len(vocab)))
make_co_occurrence_matrix(corpus)
#print(co_occurrence_matrix)
#make svd
svd = TruncatedSVD(n_components=150, n_iter=7, random_state=42)
embeddings_matrix = svd.fit_transform(co_occurrence_matrix)
word_embeddings=pd.DataFrame(embeddings_matrix,index=vocab)
embedding = {}
for word in vocab:
    embedding[word] = word_embeddings.loc[ word , : ]

print(embedding)
