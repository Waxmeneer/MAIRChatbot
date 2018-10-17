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

#this functions loads the ontology that is used to find the trigger words
with open(os.getcwd() + '/ontology_dstc2.json') as d:
    ontology_dstc2 = json.load(d)
    informable_dict = ontology_dstc2["informable"]

#this function takes a working parsing path and detects keywords used within. It then matches these keywords to the linked linkwords (such as chinese to food) and find the smallest substring that contains the trigger word and all linked words
def user_preference_identifier(parsed_sentence):
    #list with slot values = empty
    slot_list = []

    found_word_list = []
    for key, value in informable_dict.items():
        print(key)
        found_word_list.clear()
        for trigger_word in value:
            if trigger_word in parsed_sentence_full:
                found_word_list.append(trigger_word)
                for link_word in variable_keyword_link[key]:
                    if link_word in parsed_sentence_full:
                        found_word_list.append(link_word)
                        slot_list.append(substring_finder(found_word_list, parsed_sentence))

    no_duplicate_list = duplicate_remover(slot_list)                #this function removes all duplicates from the list, this sometimes happens if multiple linkedwords are present in a sentence
    disjoint_checker(no_duplicate_list, parsed_sentence_full)       #This function checks if the trees are disjoint or not

#this function finds the shortest substring that contains both the triggerword and all linkedwords
def substring_finder(found_word_list, parsed_sentence):
    substring_list = []
    for substring in parsed_sentence:
        if all(word in substring for word in found_word_list):
            substring_list.append(substring)
    shortest_substring = min(substring_list, key=len)
    return shortest_substring

#this function checks if two parsing paths are disjoint by comparing if any of the words of the substrings are present in any of the other substrings
def disjoint_checker(no_duplicate_list, parsed_sentence_full):

    parsed_sentence_full_old = parsed_sentence_full
    for substring in no_duplicate_list:
        cut_sentence = parsed_sentence_full_old.replace(substring, '')
        parsed_sentence_full_old = cut_sentence

    substring_length = 0
    for substring in no_duplicate_list:
        substring_length = substring_length + len(substring)

    if len(parsed_sentence_full) == len(cut_sentence) + substring_length:
        disjoint = True
    else:
        disjoint = False

    print("Disjoint equals")
    print(disjoint)
    return disjoint

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
    while True:
        inp= input("Find user preference. Sentence? ")
        parsed_sentence = wordparsesteps(inp)
        parsed_sentence_full=inp
        user_preference_identifier(parsed_sentence)

