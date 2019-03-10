""" Understand the pickle data format"""
import os
import re
import pickle
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
# In[01]
#the index data structure
class Index:
    def __init__(self,word,positions):
        self.word      = word
        self.positions  = positions
        self.left      = None
        self.right     = None
    #adding to the index
    def addToIndex(self,entry,positions):
        #if word not presant in the index,add it along with its positions
        if self.word:
            if entry < self.word:
                if self.left is None:
                    self.left = Index(entry,positions)
                else:
                    self.left.insert(entry,positions)
            elif entry > self.word:
                if self.right is None:
                    self.right = Index(entry,positions)
                else:
                    self.right.insert(entry,positions)
            elif entry == self.word:
                self.positions  = self.positions + positions #concat the positions list
def splitByWhiteSpaceAndRemovePunctuation(file_name):
    file = open(file_name, 'rt')
    text = file.read()
    file.close()
    # split into words by white space
    words = text.split()
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    filtered_sentence = []
    #stop_words = set(stopwords.words('english'))
    stopwords = open('swede_stop.txt','rt')
    stop_words = stopwords.read()
    stemmer = PorterStemmer()
    for w in stripped: 
        if (stemmer.stem(w.lower())) not in stop_words: 
            filtered_sentence.append(w)
    return " ".join(filtered_sentence)
# In[02]
#building postings list from a single file
def buildPostings(file_name):
    #we are assuming that each file is small enough to load into the ram at a time
    read_file = ""#empty string to load the file into memory
    """with open(file_name,'r') as file:
        read_file = file.read().replace('\n',' ')"""
    read_file = splitByWhiteSpaceAndRemovePunctuation(file_name)
    #print(read_file)
    usedWords = [] # list to store already indxed words
    indexed_File = {}
    #assuming that the file is normalized and cleaned
    for word in read_file.split():
        if word.lower() in usedWords:
            continue
        elif word.lower() not in usedWords:
            usedWords.append(word.lower())
            pattern = "\\b" + "(?i)" + word + "\\b"
            reg_match = re.finditer(pattern,read_file)
            for match in reg_match:
                indexed_File.setdefault(word,[]).append(match.start())
    #print(indexed_File)        
    """pickle.dump(indexed_File,open("index01.p","wb"))
    print("Dictionary successfully written into the file")
    print("Printing the contents of the file")
    pickle_in = open("index01.p","rb")"""
    #example_dict = pickle.load(pickle_in)
    #print(example_dict)
    return indexed_File
    
#getting the contents of a folder
def get_files(dir_path):
    files = []
    for file in os.listdir(dir_path):
        files.append(file)
    return files
# In[03]    
#buildPostings('test.txt')
def test():
    str1 = "I am a good boy good boy girlgood"
    print("Enter a string to match")
    patt  = input()
    pattern = "\\b" + "(?i)" + patt + "\\b"
    m = re.finditer(pattern,str1)
    for match in m:
        print(match.start())


# In[04]
#test()
def splitDecision(file,threshhold):
    file_info = os.stat(file)
    if file_info.st_size < threshhold:
        return False
    return True

def add_to_master_Index(inverted,doc_id,doc_index):
    if doc_index:
        for word,locations in doc_index.items():
            indices = inverted.setdefault(word,{})
            indices[doc_id] = locations
    return inverted
# In[05]
def masterIndex(files):
    #pass the list containing file names as input
    inverted = {}
    documents = {} #array containing file objects
    for file in files:
        documents [file] = file
    print(documents)
    for doc_id,doc_name in documents.items():
        path = "/home/swarnadeep/Documents/Machine Learning/Selma/" + doc_name
        doc_index = buildPostings(path)
        print(doc_index)
        add_to_master_Index(inverted,doc_id,doc_index)
    #print(inverted)
    pickle.dump(inverted,open("master_index.p","wb"))
    print("Dictionary successfully written into the file")
def printFile():
    print("Printing the contents of the file")
    pickle_in = open("master_index.p","rb")
    example_dict = pickle.load(pickle_in)
    print(example_dict)
#masterIndex(get_files("/home/swarnadeep/Documents/Machine Learning/Selma/"))
#printFile()
# In[06]
def splitFile(file,chunk_size):
    chunk = chunk_size  # number of lines from the big file to put in small file
    this_small_file = open('0.txt', 'w')#name of the starting file
    with open(file) as file_to_read:
        for i, line in enumerate(file_to_read.readlines()):
            file_name = f'{i // chunk}'
            #print(i, file_name)  # a bit of feedback that slows the process down a
            if file_name == this_small_file.name:
                this_small_file.write(line)
            else:
                this_small_file.write(line)
                this_small_file.close()
                this_small_file = open(f'{file_name}', 'w')


                

   