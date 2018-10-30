#maybe we need to adjust our manual dictionary of words and really assign type to word without description??
type_mapping = {
    "nouns": ["n"],
    "sentence": ["s"],
    "nounPhrase": ["np"],
    "determiners": ["np/n"],
    "adjectives": ["n/n"],
    "preposition": ["pp/np"],
    "endFill": ["s/s"],
    "beginFill": ["s\s"],
    "dependent_prepositions": ["(s\s)/pp"],
    "nounPhrase_1": ["np\np"],
    "nounPhraes_2": ["(np\np)/np"],
    "connectives": ["(s\s)/s"],
    "intransitiveVerbs": ["np\s"],
    "auxiliaryVerbs": ["(np\s)/(np\s)"],
    "transitiveVerbs": ["(np\s)/np"],
    "questionWords": ["s"]
}


#dependent_prepositions > verbs that are commonly followed by a preposition such as "looking for"

#16 different types

#\elimination rule> np\s if there is a np on the left this becomes a s
#/elimination rule > np/n if there is a noun on the right this becomes a np