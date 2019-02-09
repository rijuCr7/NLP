"""from nltk.corpus import wordnet
synonyms = []
antonyms = []
for syn in wordnet.synsets("distance"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import os
#test_str = 'i run at a speed of 15 meters per second for 15 minutes'
#new_string = re.sub(r'meters per second','m/s',test_str)

"""
possible values to be extracted from a kinematics problem
1)time
2)distance
3)accleration
4)speed
"""
#print(new_string)

#function to test whether a sentence is a question or not
def isQuestion(sentence):
    flag = False
    question_terms = ["calculate","what","why","when","how","find","determine"]
    if sentence.endswith("?"):
        return True
    else:
        terms = word_tokenize(sentence)
        for term in terms:
            if term.lower() in question_terms:
                flag = True
    return flag

#copied from github,match multiple regular expressions
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

def standardizeSpeed(text):
    """convert the units to the standard form as prescribed"""
    substitutions={"metres per second":"l/t",
                   "metres per hour":"l/t",
                   "metres per minute":"l/t",
                   "kilometres per second":"l/t",
                   "kilometres per hour":"l/t",
                   "miles per second":"l/t",
                   "miles per hour":"l/t",
                   "miles per minute":"l/t",
                   "konts":"l/t",
                   "feet per second":"l/t",
                   }
    #check for short forms first
    short_form = {"km/hr":"l/t",
                  "km/h":"l/t",
                  "m/s":"l/t",
                  "mi/h":"l/t",
                  "kmh":"l/t"
                  }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        if word.lower() in short_form.keys():
            output_length = output_length + " " + short_form[word.lower()]
        else:
            output_length = output_length + " " + word
    #output_length = replace(text,substitutions)
    return output_length
    #output_length = replace(text,substitutions)
    #return output_length

def standardizeTime(text):  
    #convert the time to the standard form
    substitutions={"seconds":"t",
                   "minutes":"t",
                   "hours":"t",
                   "second":"t",
                   "minute":"t",
                   "hour":"t",
                   "s":"t"
                   }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        if word.lower() in substitutions.keys():
            output_length = output_length + " " + substitutions[word.lower()]
        else:
            output_length = output_length + " " + word
    #output_length = replace(text,substitutions)
    return output_length
import string
def standardizeLength(text):
    substitutions={"metres":"l",
                   "miles":"l",
                   "degree":"l",
                   "meters":"l",
                   "miles":"l",
                   "kilometres":"l",
                   "centimetres":"l",
                   "ms":"l",
                   "mi":"l",
                   "m":"l",
                   "cms":"l",
                   "kms":"l",
                   "m":"l",
                   "cm":"l",
                   "km":"l",
                   str(chr(176)):"l" #degree symbol
                   }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        for punct in string.punctuation:
            if punct != '/':
                word = word.replace(punct,"")
        if word.lower() in substitutions.keys():
            output_length = output_length + " " + substitutions[word.lower()]
        else:
            output_length = output_length + " " + word
    #output_length = replace(text,substitutions)
    return output_length

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
#accleration standardize korte hobe
def standardizeAcc(text):
    substitutions={"m/s2":" l/t2",
                   "m/s^2":" l/t2"
                   }
    output_length = replace(text,substitutions)
    return output_length

def standardizeText(text):
    #insert accleration standardize here
    accleration = standardizeAcc(text)
    speed = standardizeSpeed(accleration)
    time_speed = standardizeTime(speed)
    length_time_speed =  standardizeLength(time_speed)
    final_standard=""
    tokens = word_tokenize(length_time_speed)
    #checking for spurious units
    for i in range(0,len(tokens)):
        #print(length_time_speed[i])
        if i >= 0:
            if tokens[i] == 'l/t':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 'l':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 't':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 'l/t2':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            else:
                final_standard = final_standard + " " + tokens[i]
    return final_standard

#this method is always run after the standardizeText method 
def extractInformation(sentence):
    term_list = word_tokenize(sentence)
    information = set()
    #print(term_list)
    for word in term_list:
        if word == "l/t":
            print("Speed as Value")
        if word == "l":
            print("Distance as Value")
        if word == "t":
            print("Time as Value")
        if word == "l/t2":
            print("Acceleration as Value")                
    for i in range(len(term_list)):
        word = term_list[i]
        if word.lower() in speed.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "l/t" == term_list[j]:
                    flag = True
                    break
            if flag :
                information.add("Speed(V)")
                print("Speed as Value")
            else:
                information.add("Speed(Q)")
                print("Speed as Question")
        if word.lower() in distance.values():
            print(word.lower())
            flag = False
            punctuation = "!#$%&'()*+,-.:;<=>?@[\]^_`{|}~"
            useless = False
            for j in range(i+1,len(term_list)):
                if "l" == term_list[j]:
                    flag = True
                    break
                elif term_list[j] in punctuation:
                    useless = True
            if flag and not useless:
                information.add("Distance(V)")
                print("Distance as Value")
            else:
                if not useless:
                    information.add("Distance(Q)")
                    print("Distance as Question")
        if word.lower() in time.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "t" == term_list[j]:
                    flag = True
                    break
            if flag :
                information.add("Time(V)")
                print("Time as Value")
            else:
                information.add("Time(Q)")
                print("Time as Question")
        if word.lower() in accleration.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "l/t2" == term_list[j]:
                    flag = True
                    break
            if flag :
                information.add("Acceleration(V)")
                print("Accleration as Value")
            else:
                information.add("Acceleration(Q)")
                print("Accleration as Question")
    return information
            
def extractProblemInfo(problem):
    sent_tokenize_list = sent_tokenize(problem)
    #print(sent_tokenize_list)
    for sent in sent_tokenize_list:
        #print(sent)
        #print("================")
        extractInformation(standardizeText(sent))
#we assume that this method is run after the normalization of the text has been done
def is_useless(statement):
    term_list = word_tokenize(statement)
    #print(term_list)
    flag = True
    for word in term_list:
        if word == "l/t":
            flag =  False
            break
        if word == "t":
            flag = False
            break
        if word == "l":
            flag = False
            break
        if word == "l/t2":
            flag = False
            break
    return flag

        
def eliminateBrackets(problem):
    bracketed=problem[problem.find("(")+1:problem.find(")")]#finding string between 2 brackets
    #print(bracketed)
    #if useless then eliminate the bracketed part
    print(is_useless(bracketed))
    if is_useless(bracketed):
        temp_new_problem = problem.replace(bracketed," ")
        new_problem = temp_new_problem.replace("( )"," ")
        return new_problem
    else:
        return problem
#creating dictionaries for synomyms 
distance = {'distance':"distance",
            'displacement':"displacement",
            'area':"area",
            'height':"height",
            'far':"far",
            'tall':"tall",
            'length':"length",
            'orbit':"orbit",
            'high':"high",
            'angle':"angle",
            'altitude':"altitude",
            'radius':"radius",
            'scope':"scope",
            'seperation':"seperation",
            'size':"size",
            'stretch':"stretch",
            'width':"width",
            'degreee':"degree",
        }
speed = {'velocity':"velocity",
         'agility':"agility",
         'pace':"pace",
         'quickness':"quickness",
         'swiftness':"swiftnes",
         'speed':"speed",
         'fast':"fast"
         }
time = {'time':"time",
        'long':"long",
        'seconds':"seconds",
        'hang time':"hang time",
        'hangtime':"hangtime",
        'hang-time':"hang-time",
        'in the air':"in the air"
        }

accleration = {'acceleration':"acceleration",
               'deceleration':"deceleration"
               }

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def test():
    text = "An airplane accelerates down a runway at 3.20 m/s2 for 32.8 s until is finally lifts off the ground. Determine the distance traveled before takeoff."
    sent_tokenize_list = sent_tokenize(text)
    for sent in sent_tokenize_list:
        print(sent)
        print("=============")
    #print(sent_tokenize_list)
#test()
#print(is_useless("Assume uniformity and SHUM at 18 l/t"))
problem = " A plane drops a C.A.R.E. package to some needy people in the jungle from a height of 1000 m. How long will it take the package to strike the ground?   "
#A car starts from rest and accelerates uniformly over a time of 5.21 seconds for a distance of 110 m. 
#extractInformation(standardizeText(problem))
#Determine the distance traveled before takeoff.
#problem = "An airplane accelerates down a runway at 3.20 m/s2 for 32.8 s until is finally lifts off the ground"
#print(standardizeText(problem))
#print(space_unit_values(problem))
#print(extractProblemInfo(standardizeText(problem)))
#print(standardizeText(problem))
#test()
#print(isQuestion("If Upton free falls for 2.60 seconds, what will be his final velocity and how far will he fall?"))
#extractInformation(standardizeText("i run at a speed of 15 metres per second for 15 minutes"))

"""
Main Driver Code to perform all tests on a folder

"""
# In[01]
""" Returns a list containing all files in a directory"""
def get_files(dir_path):
    files = []
    for file in os.listdir(dir_path):
        files.append(file)
    return files
# In[02]
def list_indexing_terms(dir_path):
    #results = open("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/write.txt","w")
    files = get_files(dir_path)
    count = 0
    for file in files:
        file_path = dir_path + "/" + file
        #print(file_path)
        #processing each file seperately
        fp = open(file_path,"r")
        file_content = fp.read()
        print(file)
        print("===============================")
        print(file_content)
        print("================================")
        extractProblemInfo(standardizeText(splitNumbersAndUnits(file_content)))
        print("===================================")
        count = count + 1
    print(count)
       
list_indexing_terms("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")