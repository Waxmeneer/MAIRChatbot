import json
import word_categories
from sent_parser import wordparsesteps
import os
from sent_converter import convertsentence
#this creates a link between slot type and linkwords linked to that slot type
variable_keyword_link = {
    "area": ["town", "part"],
    "food": ["restaurant", "food"],
    "pricerange": ["restaurant", "priced"],
    "name": []
}

#this loads the ontology that is used to find the trigger words
with open(os.getcwd() + '/ontology_dstc2.json') as d:
    ontology_dstc2 = json.load(d)
    informable_dict = ontology_dstc2["informable"]

#this function takes a working parsing path and detects keywords used within. It then matches these keywords to the linked linkwords (such as chinese to food) and find the smallest substring that contains the trigger word and all linked words
def make_slot_list(parsed_sent, sent):
    #list with slot values = empty
    slot_dict = dict()
    slot_dict_no_links = dict()
    node_list = []
    slot_list = []
    order=1 #So the system can trace back which order the words were typed.
    for word in sent:
        for key, value in informable_dict.items():
            if word in value:
                if key in slot_dict:
                    slot_dict[key].append(word)
                    slot_dict_no_links[key].append([word, order])
                    order+=1
                else:
                    slot_dict[key]=[word]
                    slot_dict_no_links[key]=[[word, order]]
                    order+=1
            if word in variable_keyword_link[key]:
                if key in slot_dict: #Only puts the linked word in if there is already a variable word.
                    slot_dict[key].append(word)
    for key in slot_dict:
        slot_list.append([key,topnode_finder(slot_dict[key], parsed_sent)])
    return [slot_list, slot_dict_no_links]


#this function finds the top node of the subtree that contains both the triggerword and all linkedwords
#If the parsing fails, it returns the words as singular words.
def topnode_finder(found_word_list, parsed_sentence):
    subtree_list = []
    for parse in parsed_sentence:
        for parsedword in parse[0:2]:
            wordstring = parsedword[1]
            if all(word in wordstring for word in found_word_list):
                subtree_list.append(wordstring)
    try:
        smallest =  min(subtree_list, key=len)
        for node in parsed_sentence:
            c=0
            while c<3: #So that it mathes to the newtype, type1 and type2 to find a corresponding node.
                if node[c][1] == smallest:
                    return [node[c], node[4]] #Returns the top node of the smallest substring, with its index.
                c+=1
    except: #Excepts the case that the word is not present in any parses.
        pass
    return [found_word_list, 99] #Only reaches this point whenever the words in found_word_list aren't parsed in the tree.

#This function checks if two sets of nodes are joint.
def joint_subtrees(nodes1, nodes2):
    joint = False
    for node in nodes1:
        if node in nodes2:
            joint = True
    return joint

#Checks if any of the trees in a list are joint. If so, it returns False, else True.
def joint_remover(slot_list, slot_dict, parsed_sent):
    disjointlist = []
    if len(slot_list)>1: #1 or less slots cant be joint.
        treelist = []
        for slot in slot_list:
            treelist.append(subtree_finder(slot[1][0], parsed_sent, [], slot[1][1]))
        c=0
        while c<len(treelist):
            tree = treelist[c]
            c2=c+1
            while c2<len(treelist):
                tree2 = treelist[c2]
                if(joint_subtrees(tree, tree2)):
                    #These few statements print the check of jointness, with the according subtrees.
                    #The numbers in the subtrees are indexes of the parses, so words that occur twice in a sentence
                    #can be separated.
                    """
                    cat1 = slot_list[c][0]
                    keyw1 = get_keywords(slot_dict[cat1])
                    cat2 = slot_list[c2][0]
                    keyw2 = get_keywords(slot_dict[cat2])
                    print("The keywords of category: \"" + cat1 + "\"" + " (" + str(keyw1)+ ")" + " with subtree:")
                    print(tree, end='\n\n')
                    print("Is disjoint with the keywords of category: \"" + cat2 + "\"" + " ("  + str(keyw2) + ")"  + " with subtree: ")
                    print(tree2, end='\n\n')
                    """
                    disjointlist.append(c)
                    disjointlist.append(c2)
                c2+=1
            c+=1
    for number in sorted(set(disjointlist), reverse=True): #Reverse so that the later elements are removed first so the indexes dont change.
        category = slot_list[number][0]
        del slot_list[number]
        del slot_dict[category]
    return [slot_list, slot_dict]

def get_keywords(category):
    catlist = []
    for elem in category:
        keyw = elem[0]
        catlist.append(keyw)
    return catlist
#Finds the subtree belonging to a top node.
def subtree_finder(topnode, parsed_sent, nodelist, index):
    nodelist.append([topnode, index])
    for node in parsed_sent:
        if node[0]==topnode:
            subtr1 = node[1]
            subtr2 = node[2]
            index = node[4]
            subtree_finder(subtr1, parsed_sent, nodelist, index)
            subtree_finder(subtr2, parsed_sent, nodelist, index)
            return(nodelist)
    return(nodelist)

#labels the nodes, so two nodes that are the same but at different places in the sentence are able to be distinguished.
def label_nodes(parsed_sent):
    c=0
    for parse in parsed_sent:
        parse.append(c)
        c+=1
    return parsed_sent

#This function is the main function. It takes in a sentence (string) and returns all filled slots, checked for jointness.
#It checks all smallest parsed subtrees.
def slot_dict(inp):
    smallestparses = wordparsesteps(inp)
    inp = convertsentence(inp)
    for parse in smallestparses:
        parsed_sentence = parse[3]
        parsed_sentence = label_nodes(parsed_sentence)
        slot_list, slot_dict = make_slot_list(parsed_sentence, inp)[0], make_slot_list(parsed_sentence, inp)[1]
        disjoint_dict = joint_remover(slot_list, slot_dict, parsed_sentence)
        if len(disjoint_dict[1])>0:
            return disjoint_dict[1]
    return {}

if __name__ == "__main__":
    while True:
        inp= input("Find user preference. Sentence? ")
        print(slot_dict(inp))

