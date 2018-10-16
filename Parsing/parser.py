from sent_converter import convertsentence as convsent
from word_categories import type_dictionary
import sys


taglist=[] #List of all the combinations of types of the words at the lowest layer.
parsedsentences = [] #All sentences that are not able to be parsed any further. 

#Labels all the words in a sentence with their possible types. Returns a list containing lists of all possible types per word.
def labelwordtypes(sentence):
    words = convsent(sentence) #Makes it lowercase, without interpunction and mapped to the closest spelling.
    print('Recognized input sentence: ' + ' '.join(words))
    typelist = []
    for word in words:
        types = []
        for item in type_dictionary.items():
            if word in item[1]:
                types.append(item[0])
        typelist.append(types)
    return(typelist)



#This method adds all combinations of types of the words of a sentence to the global taglist. 
def taglowestlayer(tagsentence, currenttags):
    if len(tagsentence)>0:
        tags=tagsentence[0]
        for tag in tags:
            prevtags = currenttags.copy() #This prevents python from creating one big list out of currenttags.
            prevtags.append(tag)
            rest = tagsentence[1:]
            taglowestlayer(rest, prevtags)
    
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
            copied[c]=parsedtypes
            del copied[c+1]
            parsed = True
            mergetypes(copied)
        c+=1
    if parsed==False:
        parsedsentences.append(sent)
        

#Merges two types into the new type and returns this type. 
def parsetypes(type1, type2):
    type1split = type1.split('/')
    type2split = type2.split('/')
    if len(type1split)>1: #If it has split on a /, the returned list will be >1. 
        rightside = type1split[len(type1split)-1]
        if rightside==type2split[0]:
            newtype = '/'.join(type1split[:len(type1split)-1])
            if len(type2split)>1:
                rejoined = '/'.join(type2split[1:])
                newtype+='/' + rejoined #Review this!
            print(type1 +' + '+type2 +' = '+newtype + '  - /-elimination')
            return newtype #This rejoins all the elements but the last, again separated by /.
    type1split = type1.split('\\')
    type2split = type2.split('\\')
    if len(type2split)>1:
        leftside = type2split[0]
        if leftside==type1split[len(type1split)-1]:
            newtype = '/'.join(type2split[1:])
            print(type1 +' + '+type2 +' = '+newtype + '  - \\-elimination')
            return newtype
    return None



#Main function!
#Takes in a sentence string and outputs the smallest possible parse.
def parsesentence(sentence):
    wordtypesent = labelwordtypes(sentence)
    taglowestlayer(wordtypesent,[]) #creates all combinations of wordtypes.
    print("Possible sentence type combinations: " + str(taglist))
    print('')
    for taggedsent in taglist:
        print(taggedsent)
        mergetypes(taggedsent) #puts all maximally parsed sentences in the list: parsedsentences.
        print("Result: " + str(parsedsentences[len(parsedsentences)-1]))
        print('') #So that each step is shown for individual sentence parses
    leasttypesent = 100 #arbitrary
    smallestparses = []
    for parsedsent in parsedsentences:
        if len(parsedsent)<leasttypesent:
            leasttypesent=len(parsedsent)
    for parsedsent in parsedsentences:
        if len(parsedsent)==leasttypesent and parsedsent not in smallestparses:
            smallestparses.append(parsedsent)
    return smallestparses
    
    
if __name__ == "__main__":
    while True:          
        inp = input("Sentence to be parsed?")
        print(parsesentence(inp))
    
