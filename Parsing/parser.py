from sent_converter import convertsentence as convsent
from word_categories import word_dictionary
import sys


taglist=[] #List of all the combinations of types of the words at the lowest layer.
parsedsentences = [] #All sentences that are not able to be parsed any further. 

#Labels all the words in a sentence with their possible types. Returns a list containing lists of all possible types per word.
def labelwordtypes(sentence):
    words = convsent(sentence) #Makes it lowercase, without interpunction and mapped to the closest spelling.
    typelist = []
    for word in words:
        types = []
        for item in word_dictionary.items():
            if word in item[1]:
                types.append(item[0])
        typelist.append(types)
    return(typelist)



#This method adds all combinations of types of the words of a sentence to the global taglist. 
def taglowestlayer(tagsentence, currenttags, taglist):
    if len(tagsentence)>0:
        tags=tagsentence[0]
        for tag in tags:
            prevtags = currenttags.copy() #This prevents python from creating one big list out of currenttags.
            prevtags.append(tag)
            rest = tagsentence[1:]
            taglowestlayer(rest, prevtags, taglist)
    
    else:
        taglist.append(currenttags)


parsedsentences = []
#Adds to the parsedsentences  list all sentences that cannot be parsed any further.
#Parameter sent consists of a sentence, containing a list of possible types for each word.
def mergetypes(sent): 
    c=0
    parsed = False
    while c+1<len(sent): #The last word can obviously not be parsed.          
        word=sent[c]
        nextword = sent[c+1]
        parsedtypes = parsetypes(word, nextword)
        if parsedtypes != None:
            copied = sent.copy()
            copied[c]=parsed
            del copied[c+1]
            parsed = True
            mergetypes(copied)
        c+=1
    if parsed==False:
        parsedsentences.append(sentence)
        


def parsetypes(type1, type2):
    type1split = type1.split('/')
    if len(type1split)>1: #If it has split on a /, the returned list will be >1. 
        rightside = type1split[len(type1split)]
        if rightside==type2:
            newtype = type1split[:len(type1split)-1].join('/')
            print(type1 +'+'+type2 +'='+newtype)
            return type1split[:len(type1split)-1].join('/') #This rejoins all the elements but the last, again separated by /.
    type2split = type2.split('\\')
    if len(type2split)>1:
        leftside = type2.split[0]
        if leftside==type1:
            newtype = type1split[1:].join('/')
            print(type1 +'+'+type2 +'='+newtype)
            return(newtype)
    return None



def parsesentence(sentence):
    wordtypesent = labelwordtypes(sentence)
    taglowestlayer() #creates all combinations of wordtypes.
    for taggedsent in taglist:
        mergetypes(taggedsent) #puts all maximally parsed sentences in the list: parsedsentences.
    leasttypessent = 100 #arbitrary
    smallestparses = []
    for parsedsent in parsedsentences
        if len(parsedsent)<leasttypesent:
            leassttypesent=len(parsedsent)
    for parsedsent in parsedsentences:
        if len(parsedsent)==leasttypesent:
            smallestparses.append(parsedsent)
    
    


