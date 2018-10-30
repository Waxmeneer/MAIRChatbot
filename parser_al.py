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
        parsedtypes = parsetypes2(word, nextword)
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
    print("Possible sentence type combinations: ")
    pprint(taglist)
    print('===================================')
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


def find_closing_bracket_position(type_given):
    first_closing_bracket_position = 0
    # check is there is another "(" between the first "(" and the first ")"
    is_there_extra_bracket = (type_given[1:].split(')', 1)[0].find('(') != -1)
    # find that char after the last ")" of the first group
    first_closing_bracket_position = type_given.find(')', first_closing_bracket_position+1)
    if (is_there_extra_bracket):
        # check is there is another "(" between the second "(" and the second ")"
        is_there_extra_bracket = (type_given[1:].split(')', 1)[0].find('(') != -1)
        first_closing_bracket_position = type_given.find(')', first_closing_bracket_position+1)
    return first_closing_bracket_position

def break_type_into_two(type_given):
    #check if the first char is "("
    if (type_given[0] == '('):

        first_closing_bracket_position = find_closing_bracket_position(type_given)

        next_char_after_first_closing_bracket_position = first_closing_bracket_position + 1
        try:
            next_char_after_first_closing_bracket_char = type_given[next_char_after_first_closing_bracket_position]
            slash_or_backslash_position = next_char_after_first_closing_bracket_position
            # if the next char after the first ")" is "/"
            if (next_char_after_first_closing_bracket_char == '/'):
                # split into to by "/"
                split1_result = (type_given[:next_char_after_first_closing_bracket_position], type_given[next_char_after_first_closing_bracket_position + 1:], next_char_after_first_closing_bracket_char)
            # if the next char after the first ")" is "\"
            elif (next_char_after_first_closing_bracket_char == '\\'):
                # split into to by "\"
                split1_result = (type_given[:next_char_after_first_closing_bracket_position], type_given[next_char_after_first_closing_bracket_position + 1:], next_char_after_first_closing_bracket_char)
            return split1_result
        # if we don't have the next char
        except IndexError:
            #remove first "(" and first ")"
            removed_type1 = type_given[1:-1]
            return break_type_into_two(removed_type1)
    else:
        #find first "/" or first "\"
        if ((type_given.find('/') != -1) and ( type_given.find('\\') != -1)):
            slash_or_backslash_position = min(type_given.find('/'), type_given.find('\\'))
            return(type_given[:slash_or_backslash_position], type_given[slash_or_backslash_position + 1:], type_given[slash_or_backslash_position])
        elif ((type_given.find('/') != -1) or (type_given.find('\\') != -1)):
            slash_or_backslash_position = max(type_given.find('/'), type_given.find('\\'))
            return(type_given[:slash_or_backslash_position], type_given[slash_or_backslash_position+1:], type_given[slash_or_backslash_position])
        else:
            return type_given

# Merges two types into the new type and returns this type.
def parsetypes2(type1_original, type2_original):

    type1 = break_type_into_two(type1_original)
    type2 = break_type_into_two(type2_original)

    if (type(type1) != str):
        if ((type1[2] == '/') and (type1[1] == type2_original )):
            print(type1_original + ' + ' + type2_original + ' = ' + type1[0] + '  - /-elimination')
            return type1[0]
    elif (type(type2) != str):
        if ((type2[2] == '\\') and (type2[1] == type1_original)):
            print(type1_original + ' + ' + type2_original + ' = ' + type2[0] + '  - \\-elimination')
            return type2[0]

    return None


if __name__ == "__main__":
    while True:
        inp = input("Sentence to be parsed?")
        print(parsesentence(inp))
        taglist = []
        parsedsentences = []        


#For testing
'''
    pprint(parsetypes2('s/(np\\s)', '(np\\s)'))
    pprint(parsetypes2('(np/np)/(np/np)', '(np/np)'))
    
result = parsetypes2('s/(np\\s)', 'np\\s')
result = parsetypes2('(np/np)\\np', 's')
result = parsetypes2('(np/np)/np', 's')
result = parsetypes2('(np\\np)\\np', 's')

print ('================================')

result = parsetypes2('(np\\np)\\(np\\np)', 's')
result = parsetypes2('(np/np)/(np/np)', 's')
result = parsetypes2('(np\\np)/(np\\np)', 's')
result = parsetypes2('(np/np)\\(np/np)', 's')
result = parsetypes2('(np\\np)\\(np/np)', 's')
result = parsetypes2('(np/np)\\(np\\np)', 's')
result = parsetypes2('(np\\np)/(np/np)', 's')
result = parsetypes2('(np/np)/(np\\np)', 's')


print ('================================')

result = parsetypes2('np\\(np\\np)', 's')
result = parsetypes2('np\\(np/np)', 's')
result = parsetypes2('np/(np\\np)', 's')
result = parsetypes2('np/(np/np)', 's')

print ('================================')

result = parsetypes2('np\\n', 's')
result = parsetypes2('np/n', 's')

result = parsetypes2('(np/n)', 's')
result = parsetypes2('(np\\n)', 's')

result = parsetypes2('((np/n)/n)/np', 's')
'''