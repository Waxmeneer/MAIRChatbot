import sys, string
import Levenshtein as ls
def sentenceconvert(sentence, wordlist):
    st = sentence.lower()
    wordlist = wordlist.split()
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
    print(split)


sentenceconvert(sys.argv[1], sys.argv[2])
 
