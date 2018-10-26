import json
import word_categories
from sent_parser import wordparsesteps
import os
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
def user_preference_identifier(parsed_sent, sent):
    #list with slot values = empty
    slot_list = []
    node_list = []
    found_word_list = []
    for key, value in informable_dict.items():
        found_word_list.clear()
        for trigger_word in value:
            if trigger_word in sent:
                found_word_list.append(trigger_word)
                for link_word in variable_keyword_link[key]:
                    if link_word in sent:
                        found_word_list.append(link_word)
                slot_list.append([key,topnode_finder(found_word_list, parsed_sent)])

    slot_list = duplicate_remover(slot_list)                #this function removes all duplicates from the list, this sometimes happens if multiple linkedwords are present in a sentence
    for slot in slot_list:
        node_list.append(subtree_finder(slot[1], parsed_sent, []))
    if(disjoint_checker(node_list)): #This function checks if the trees are disjoint or not
        return None
    else:
        return slot_list
        

#this function finds the top node of the subtree that contains both the triggerword and all linkedwords
def topnode_finder(found_word_list, parsed_sentence):
    subtree_list = []
    for parse in parsed_sentence:
        wordinf = parse[0]
        wordstring = wordinf[1]
        if all(word in wordstring for word in found_word_list):
            subtree_list.append(wordstring) 
    smallest =  min(subtree_list, key=len)
    for node in parsed_sentence:
        if node[0][1] == smallest:
            return node[0] #Returns the top node of the smallest substring.

#This function checks if two sets of nodes are disjoint.
def disjoint_subtrees(nodes1, nodes2):
    disjoint = False
    for node in nodes1:
        if node in nodes2:
            disjoint = True
    return disjoint

#Checks if any of the trees in a list are disjoint. If so, it returns True, else False.
def disjoint_checker(treelist):
    c=0
    while c<len(treelist):
        tree = treelist[c]
        c2=c+1
        while c2<len(treelist):
            tree2 = treelist[c2]
            if(disjoint_subtrees(tree, tree2)):
               return True
            c2+=1
        c+=1
    return False

#Finds the subtree belonging to a top node.
def subtree_finder(topnode, parsed_sent, nodelist):
    nodelist.append(topnode)
    for node in parsed_sent:
        if node[0]==topnode:
            subtr1 = node[1]
            subtr2 = node[2]
            subtree_finder(subtr1, parsed_sent, nodelist)
            subtree_finder(subtr2, parsed_sent, nodelist)
            return(nodelist)



#this function removes duplicates from any lists that is used as input
def duplicate_remover(list):
    no_duplicates_list = []
    for slot in list:
        if slot in no_duplicates_list:
            pass
        else:
            no_duplicates_list.append(slot)
    return no_duplicates_list

if __name__ == "__main__":
    inp= input("Find user preference. Sentence? ")
    parsed_sentence = wordparsesteps(inp)
    print(user_preference_identifier(parsed_sentence, inp))

