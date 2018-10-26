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
    splitsent = sent.split()
    for word in splitsent:
        for key, value in informable_dict.items():
            found_word_list.clear()
            if word in value:
                found_word_list.append(word)
                templist = []
                for link_word in variable_keyword_link[key]:
                    if link_word in splitsent:
                        templist.append(link_word)
                found_word_list+=templist
                slot_list.append([key,topnode_finder(found_word_list, parsed_sent)])
    for slot in slot_list:
        index=-1
        for parse in parsed_sent:
            if parse[0]==slot[1]:
                index=parse[4]
        node_list.append(subtree_finder(slot[1], parsed_sent, [], index))
    return [slot_list, node_list]

#Prints whether trees in the node_list are disjoint.
def disjoint_printer(node_list):
    for node in node_list:
        for item in node:
            print(item[0])
        print("")
    if disjoint_checker(node_list):
        print('Disjoint')
    else:
        print('Not disjoint')

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
            return node[0] #Returns the top node of the smallest substring, with its index.

#This function checks if two sets of nodes are disjoint.
def joint_subtrees(nodes1, nodes2):
    disjoint = False
    for node in nodes1:
        if node in nodes2:
            joint = True
    return joint

#Checks if any of the trees in a list are disjoint. If so, it returns True, else False.
def disjoint_checker(treelist):
    c=0
    while c<len(treelist):
        tree = treelist[c]
        c2=c+1
        while c2<len(treelist):
            tree2 = treelist[c2]
            if(joint_subtrees(tree, tree2)):
               return False
            c2+=1
        c+=1
    return True

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

#labels the nodes, so two nodes that are the same but at different places in the sentence are able to be distinguished.
def label_nodes(parsed_sent):
    c=0
    for parse in parsed_sent:
        parse.append(c)
        c+=1
    return parsed_sent


if __name__ == "__main__":
    inp= input("Find user preference. Sentence? ")
    parsed_sentence = wordparsesteps(inp)
    parsed_sentence = label_nodes(parsed_sentence)
    user_pref = user_preference_identifier(parsed_sentence, inp)
    disjoint_printer(user_pref[1])
    slot_list = user_pref[0]
    if disjoint_checker(user_pref[1]):
        pass###

