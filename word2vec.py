#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:54:20 2019

@author: swarnadeep
"""

import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) 
import os
import string
import gensim 

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

vocab = []

def extract_words(text,unique_words):
    text.translate(string.punctuation) 
    words = text.split() 
    for r in words: 
        if not r in stop_words:
            if not isImpure(r) and len(r) > 3:
                unique_words[r] = 0


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

sentences = []
def create_corpus_to_pass(dir_path):
    files = get_files(dir_path)
    #sentences = []
    vocab = []
    unique_words = {}
    for file in files:
        file_path = dir_path + "/" + file
        fp = open(file_path,"r")
        file_content = fp.read()
        file_content = splitNumbersAndUnits(file_content)
        extract_words(file_content,unique_words)
        for keys in unique_words.keys():
            vocab.append(keys)
        sentences.append(vocab)
        unique_words = {}
        vocab = []
        print(sentences)


create_corpus_to_pass("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")

model = gensim.models.Word2Vec (sentences, size=150, window=10, min_count=2, workers=10)
model.train(sentences,total_examples=len(sentences),epochs=10)

print("================================")
vector = model.wv['long']
print(len(vector))