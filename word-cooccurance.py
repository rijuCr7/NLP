#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:04:03 2019

@author: swarnadeep
"""

import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) 
import os
import string

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

def extract_words(text,unique_words):
    text.translate(string.punctuation) 
    words = text.split() 
    for r in words: 
        if not r in stop_words:
            if not isImpure(r) and len(r) > 3:
                unique_words[r] = 0
    return unique_words

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

collocation_matrix = {}

def initialize_collocation_matrix(dir_path):
    files = get_files(dir_path)
    unique_words = {}    
    for file in files:
        file_path = dir_path + "/" + file
        fp = open(file_path,"r")
        file_content = fp.read()
        file_content = splitNumbersAndUnits(file_content)
        unique_words = extract_words(file_content,unique_words)
    #print(unique_words)
    for key in unique_words:
        collocation_matrix[key] = unique_words
    #print(collocation_matrix)

def fill_collocation(text):
    word_tokenize_list = word_tokenize(text)
    words = ""
    for word in word_tokenize_list:
        words = words + " " + word
    tokens = nltk.word_tokenize(words)
    bigrms = nltk.bigrams(tokens)
    bigrams = []
    for grm in bigrms:
        bigrams.append(grm)
    for bigram in bigrams:
        if bigram[0] in collocation_matrix.keys() and bigram[1] in collocation_matrix.keys():
            collocation_matrix[bigram[0]][bigram[1]] = collocation_matrix[bigram[0]][bigram[1]] + 1

def create_collocation_matrix(dir_path):
    initialize_collocation_matrix(dir_path)
    files = get_files(dir_path)
    for file in files:
        file_path = dir_path + "/" + file
        fp = open(file_path,"r")
        file_content = fp.read()
        file_content = splitNumbersAndUnits(file_content)
        fill_collocation(file_content)

create_collocation_matrix("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")
print(collocation_matrix)
        