import sys, string
import Levenshtein as ls
import word_categories as wc

#This method converts the words of a sentence to their closest ressembling words in the
#dictionary, found in word_categories.py. The input is a string of the sentence.
def convertsentence(sentence):
    st = sentence.lower()
    typelist = wc.type_dictionary.values()
    wordlist = []
    for type in typelist:
        for word in type:
            wordlist.append(word)
    newst = ''
    for letter in st:
        if letter not in set(string.punctuation): #All letters (and numbers) remain that are not punctuation.
            newst+=letter
    split = newst.split()
    c=0
    while c<len(split):
        word = split[c]
        if word not in wordlist:
            lowestdist = 100 #arbitrary high number. !!We could make that if the eventual best distance is too high, it yields an error¡¡ 
            bestword=''
            for compareword in wordlist:
                lsdist = ls.distance(word, compareword)
                if lsdist < lowestdist:
                    lowestdist=lsdist
                    bestword = compareword
            split[c]=bestword
        c+=1
    return split


if __name__ == "__main__":
    convertsentence(sys.argv[1])
 
