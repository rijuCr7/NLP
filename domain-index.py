"""from nltk.corpus import wordnet
synonyms = []
antonyms = []
for syn in wordnet.synsets("range"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
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
    question_terms = ["what","why","when","how","find","determine"]
    if sentence.endswith("?"):
        return True
    else:
        terms = word_tokenize(sentence)
        for term in terms:
            if term.lower() in question_terms:
                flag = True
    return flag


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
    output_length = replace(text,substitutions)
    return output_length

def standardizeTime(text):  
    #convert the time to the standard form
    substitutions={"seconds":"t",
                   "minutes":"t",
                   "hours":"t",
                   "second":"t",
                   "minute":"t",
                   "hour":"t"
                   }
    output_length = replace(text,substitutions)
    return output_length

def standardizeLength(text):
    substitutions={"metres":"l",
                   "degree":"l",
                   "degree":"l",
                   "kilometres":"l",
                   "centimetres":"l",
                   "ms":"l",
                   "cms":"l",
                   "kms":"l",
                   "m":"l",
                   "cm":"l",
                   "km":"l",
                   str(chr(176)):"l" #degree symbol
                   }
    output_length = replace(text,substitutions)
    return output_length
#accleration standardize korte hobe

def standardizeText(text):
    #insert accleration standardize here
    speed = standardizeSpeed(text)
    time_speed = standardizeTime(speed)
    length_time_speed =  standardizeTime(time_speed)
    return length_time_speed

def extractInformation(sentence):
    term_list = word_tokenize(sentence)
    if not isQuestion(sentence):
        for word in term_list:
            if word == "l/t":
                print("speed as value")
            if word == "l":
                print("distance as value")
            if word == "t":
                print("time as value")
#method to identify whether a statement is of any use to us i.e whether it contains any data or data
def is_useless(statement):
    #we assume that this method is run after the normalization of the text has been done
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
    """if statement.find("l/t") < 1:
        return False
    elif statement.find("l/t2") < 1:
        return False
    elif statement.find("t") < 1:
        return False
    elif statement.find("l") < 1:
        return False
    else:
        return True"""
        
def eliminateBrackets(problem):
    bracketed=problem[problem.find("(")+1:problem.find(")")]#finding string between 2 brackets
    print(bracketed)
    #if useless then eliminate the bracketed part
    print(is_useless(bracketed))
    temp_new_problem = problem.replace(bracketed," ")
    new_problem = temp_new_problem.replace("( )"," ")
    print(new_problem)
    """brackets = re.compile(r"^(.*?)/")
    new_problem = re.sub(r"^(.*?)/",'a', problem)
    if brackets.match(problem):
        print("Matched")
    else:
        print("Mismatch")
    print(new_problem)"""
def test():
    text = "Upton Chuck is riding the Giant Drop at Great America. If Upton free falls for 2.60 seconds, what will be his final velocity and how far will he fall?(Assume uniformity and SHUM )"
    sent_tokenize_list = sent_tokenize(text)
    print(sent_tokenize_list)
#test()
#print(isQuestion("If Upton free falls for 2.60 seconds, what will be his final velocity and how far will he fall?"))
#extractInformation(standardizeText("i run at a speed of 15 metres per second for 15 minutes"))
eliminateBrackets("Upton Chuck is riding the Giant Drop at Great America. If Upton free falls for 2.60 seconds, what will be his final velocity and how far will he fall?(Assume uniformity and SHUM )")































"""if re.match(r"l/t","l/t"):
    print("speed as value")
else:
    print("Pattern Mismatch")
#print(standardizeText("i run at a speed of 15 metres per second for 15 minutes"))
length = standardizeSpeed("i run at a speed of 15 metres per second for 15 minutes")
print(standardizeTime(length))
str1 = "97" + " " + str(chr(176))
print(standardizeSpeed(str1))"""
