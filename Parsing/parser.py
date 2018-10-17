from sent_converter import convertsentence as convsent
from word_categories import type_dictionary
import sys
from pprint import pprint

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
    return([typelist, words])



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

#Adds to the parsedsentences  list all sentences that cannot be parsed any further.
#Parameter sent consists of a sentence, containing a list of possible types for each word.
def mergetypes(sent, orig, words, parseinfolist): 
    c=0
    parsed = False
    while c+1<len(sent): #The last word of a sentence can obviously not be parsed, when evaluating to the right side.          
        type, word =sent[c], words[c]
        nexttype, nextword = sent[c+1], words[c+1]
        parseinfo = parsetypes(type, word, nexttype, nextword)
        if parseinfo != None:
            newlist = parseinfolist.copy() #Prevents one big list out of parseinfolist for type combinations that have multiple parses.
            newlist.append(parseinfo)
            copied = sent.copy()
            copied[c]=parseinfo[0]
            del copied[c+1]
            wordsc = words.copy()
            wordsc[c]=wordsc[c]+' ' + wordsc[c+1]
            del wordsc[c+1]
            parsed = True
            mergetypes(copied, orig, wordsc, newlist)
        c+=1
    if parsed==False:
        parsedsentences.append([sent, orig, words, parseinfolist])
        

#Merges two types into the new type and returns this type. 
def parsetypes(type1, word1, type2, word2):
    type1 = remouterbracks(type1)
    type2 = remouterbracks(type2)
    splitforw1 = splitforslash(type1)
    #splitback1 = splitbackslash(type1)
    #splitforw2 = splitforslash(type2)
    splitback2 = splitbackslash(type2)
    if splitforw1!=None:
        rightelem=remouterbracks(splitforw1[1])
        if rightelem==type2:
            newtype=remouterbracks(splitforw1[0])
            #print(type1 +' + '+type2 +' = '+newtype + '  - /-elimination')
            return [newtype, "'"+word1 +"'"+ ': ' + type1 +  '   /-elimination   ' + "'"+word2+"'" +  ': ' +  type2 +'  == ' + "'"+word1 + ' ' + word2+"'" + ': ' + newtype]
    if splitback2!=None:
        rightelem = splitback2[0]
        if rightelem==type1:
            newtype=remouterbracks(splitback2[1])
            #print(type1 +' + '+type2 +' = '+newtype + '  - \\-elimination')
            return [newtype, "'"+word1 +"'"+ ': ' + type1 +  '   \\-elimination   ' + "'"+word2+"'" +  ': ' +  type2 +'  == ' + "'"+word1 + ' ' + word2+"'" + ': ' + newtype]
    return None

def remouterbracks(string):
    c=0
    #When the amounts of brackets are equal, the first bracket is matched. If that does not occur at the end of the string
    #the normal string is returned, else one without the brackets.
    leftbrackamt = 0
    rightbrackamt =0
    while c<len(string):
        if string[c]=='(':
            leftbrackamt+=1
        elif string[c]== ')':
            rightbrackamt+=1
        if leftbrackamt==rightbrackamt:
            if c==len(string)-1 and string[0]=='(':
                return string[1:len(string)-1]
            return string
        c+=1
    return string

#Splits a given type into two, splitting on a forward slash
def splitforslash(string):
    string = remouterbracks(string)
    strlen = len(string)
    leftbrackamt = 0
    rightbrackamt =0
    c=strlen-1
    while c>=0:
        if string[c]==')':
            rightbrackamt+=1
            c-=1
            while rightbrackamt!=leftbrackamt:
                if string[c]==')':
                    rightbrackamt+=1
                elif string[c]=='(':
                    leftbrackamt+=1
                c-=1
        if c>=0:
            if string[c]=='/':
                return [string[:c], string[c+1:]]
        c-=1
    return None

#Splits a given type into two, splitting on a backslash
def splitbackslash(string):
    string = remouterbracks(string)
    strlen = len(string)
    leftbrackamt = 0
    rightbrackamt =0
    c=0
    while c<strlen:
        if string[c]=='(':
            leftbrackamt+=1
            c+=1
            while rightbrackamt!=leftbrackamt:
                if string[c]==')':
                    rightbrackamt+=1
                elif string[c]=='(':
                    leftbrackamt+=1
                c+=1
        if c<strlen:
            if string[c]=='\\':
                return [string[:c], string[c+1:]]
        c+=1
    return None

        
#Main function!
#Takes in a sentence string and outputs the smallest possible parse.
def parsesentence(sentence):
    labels = labelwordtypes(sentence)
    wordtypes = labels[0]
    words = labels[1]
    taglowestlayer(wordtypes,[]) #creates all combinations of wordtypes.
    #print("Possible sentence type combinations: ")
    #print(taglist)
    print('')
    for taggedsent in taglist:
        mergetypes(taggedsent, taggedsent, words, []) #puts all maximally parsed sentences in the list: parsedsentences.
    leasttypesent = 100 #arbitrary
    smallestparses = []
    for parsedsent in parsedsentences:
        if len(parsedsent[0])<leasttypesent:
            leasttypesent=len(parsedsent[0])
    for parsedsent in parsedsentences:
        if len(parsedsent[0])==leasttypesent and parsedsent not in smallestparses:
            smallestparses.append(parsedsent)
    return smallestparses
    
    
if __name__ == "__main__":
    while True:
        inp = input("Sentence to be parsed? ")
        smallestparses = parsesentence(inp)
        results=[]
        for item in smallestparses:
            if item[0] not in results:
                print("Initial types: " + str(item[1]), end='\n\n')
                parseinfolist=item[3]
                for parse in parseinfolist:
                    print(parse[1], end='\n')
                print('\n')
                print(item[2])
                print('with resulting types: ' + str(item[0]))
                results.append(item[0])
                print('\n\n')
        taglist = []
        parsedsentences = []
    
