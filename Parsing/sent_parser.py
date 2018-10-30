#This python file takes in sentences when called via console.
#It then parses this sentence into a final type, and shows all steps.

from word_categories import type_dictionary
from sent_converter import convertsentence as convsent

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

#Adds to the parsedsentences list all sentences that cannot be parsed any further.
#Parameter sent consists of a sentence, containing a list of possible types for each word.
def mergetypes(sent, orig, words, parseinfolist): 
    c=0
    parsed = False
    while c<len(sent)-1: #The last word of a sentence can obviously not be parsed, when evaluating to the right side.          
        type, word =sent[c], words[c]
        nexttype, nextword = sent[c+1], words[c+1]
        parseinfo = parsetypes(type, word, nexttype, nextword)
        if parseinfo != None:
            parseinfolistc = parseinfolist.copy() #Prevents one big list out of parseinfolist for type combinations that have multiple parses.
            parseinfolistc.append(parseinfo)
            
            sentc = sent.copy()
            sentc[c]=parseinfo[0][0] #First element of the parseinfo list is the newtype.
            del sentc[c+1]
            
            wordsc = words.copy()
            wordsc[c]=parseinfo[0][1] #Second element is the merged words.
            del wordsc[c+1]
            parsed = True
            
            mergetypes(sentc, orig, wordsc, parseinfolistc)
        c+=1
    if parsed==False:
        parsedsentences.append([sent, orig, words, parseinfolist])
        

#Merges two types into the new type and returns this type. 
def parsetypes(type1, word1, type2, word2):
    type1 = remouterbracks(type1)
    type2 = remouterbracks(type2)
    splitforw = splitforslash(type1)
    splitback = splitbackslash(type2)
    if splitforw!=None: #Has performed a / split.
        rightelem=remouterbracks(splitforw[1])
        if rightelem==type2:
            newtype=remouterbracks(splitforw[0])
            return [[newtype, word1 + " " + word2],[type1, word1], [type2, word2], '/']
    if splitback!=None: #Has performed a \ split.
        rightelem = splitback[0]
        if rightelem==type1:
            newtype=remouterbracks(splitback[1])
            return [[newtype, word1 + " " + word2], [type1, word1], [type2, word2], '\\']
    return None



#This function removes the outer brackets of a type and returns the result, regardless of whether it actually removed them.

#When the amounts of brackets are equal, the first bracket is matched. If that does not occur at the end of the string
#the normal string is returned, else one without the brackets.
def remouterbracks(string):
    leftbrackamt = 0
    rightbrackamt =0
    c=0
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

#This function splits a given type into two, splitting on a forward slash
#It avoids splitting within brackets, when the brackets are not brackets around the whole type.
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
            while rightbrackamt!=leftbrackamt and c<strlen:
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
            while rightbrackamt!=leftbrackamt and c<strlen:
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


        
#This is the main function of the program.
#It takes in a sentence string and outputs the smallest possible parses. There may be more than one smallest parse.
def parsesentence(sentence):
    labels = labelwordtypes(sentence)
    wordtypes = labels[0]
    words = labels[1]
    taglowestlayer(wordtypes,[]) #creates all combinations of wordtypes.
    #print("Possible sentence type combinations: ")
    #print(taglist)
    #print('')
    for taggedsent in taglist:
        mergetypes(taggedsent, taggedsent, words, []) #puts all maximally parsed sentences in the list: parsedsentences.
    leasttypesent = 100 #arbitrary high number
    smallestparses = []
    for parsedsent in parsedsentences: #Here it finds the lowest amount of types in the parsedsentences list.
        if len(parsedsent[0])<leasttypesent:
            leasttypesent=len(parsedsent[0])
    for parsedsent in parsedsentences: #Here, it puts all parses in a list if they have an amount of types equal to the lowest amount. 
        if len(parsedsent[0])==leasttypesent and parsedsent not in smallestparses:
            smallestparses.append(parsedsent)
    return smallestparses

#When the function is called for part 3, it just returns the steps in which the words were parsed together. 
def wordparsesteps(sentence):
    taglist.clear()
    parsedsentences.clear()
    smallestparses = parsesentence(sentence)
    return smallestparses

#When the file is executed as main file, the user can put in a sentence.
#This sentence is parsed, showing all steps towards the final type.
if __name__ == "__main__":
    while True:
        inp = input("Sentence to be parsed? ")
        smallestparses = parsesentence(inp) 
        results=[]
        for item in smallestparses: #item consists of respectively: final type, the original sentence types, the parsed combinations of words and the parse information such as steps.
            if item[0] not in results:
                print("Initial types: " + str(item[1]), end='\n\n')
                parseinfolist=item[3]
                for parse in parseinfolist:
                    newword, word1, word2, elim = parse[0],parse[1],parse[2], parse[3] #Where a word consists of both the type and its text.
                    print("'"+word1[1] +"'"+ ': ' + word1[0] +  '   ' + elim + '-elimination   ' + "'"+word2[1]+"'" +  ': ' +  word2[0] +'  == ' + "'"+newword[1] + "'" + ': ' + newword[0])
                print('\n')
                print(item[2])
                print('with resulting types: ' + str(item[0]))
                results.append(item[0])
                print('\n\n')
        taglist = []
        parsedsentences = []
