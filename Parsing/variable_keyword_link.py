import json
import word_categories

variable_keyword_link = {
    "area": ["town", "part"],
    "food": ["restaurant", "food"],
    "pricerange": ["restaurant", "priced"],
    "name": []
}

#TODO define parsed sentence full
#TODO define disjointness
parsed_sentence = ["i want chinese food", "i", "want chinese food", "want", "chinese food", "chinese", "food", "want chinese food in the south part of town", "in the south part of town", "in", "the south part of town", "the", "south part of town", "south part", "of town", "south", "town"]
parsed_sentence_full = "i want chinese food in the south part of town"

#specify path
with open('C:/Users/User/Studie/MAIR/Git Chatbot/MAIRChatbot/Parsing/ontology_dstc2.json') as d:
    ontology_dstc2 = json.load(d)
    informable_dict = ontology_dstc2["informable"]

#select smallest parsed_sentence with type s as input
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
                        print(str(found_word_list) + " dit is de link + trigger word list die ie gevonden heeft")
                        slot_list.append(substring_finder(found_word_list, parsed_sentence))

    no_duplicate_list = duplicate_remover(slot_list)
    disjoint_checker(no_duplicate_list, parsed_sentence_full)

def substring_finder(found_word_list, parsed_sentence):
    substring_list = []
    for substring in parsed_sentence:
        if all(word in substring for word in found_word_list):
            substring_list.append(substring)
    shortest_substring = min(substring_list, key=len)
    print(shortest_substring + " ANTWOORD")
    return shortest_substring

def disjoint_checker(no_duplicate_list, parsed_sentence_full):

    parsed_sentence_full_old = parsed_sentence_full
    for substring in no_duplicate_list:
        cut_sentence = parsed_sentence_full_old.replace(substring, '')
        parsed_sentence_full_old = cut_sentence

    substring_length = 0
    for substring in no_duplicate_list:
        substring_length = substring_length + len(substring)

    print(len(parsed_sentence_full))
    print(len(cut_sentence))
    print(substring_length)

    if len(parsed_sentence_full) == len(cut_sentence) + substring_length:
        disjoint = True
    else:
        disjoint = False

    print(disjoint)
    return disjoint

def duplicate_remover(list):
    no_duplicates_list = []
    for slot in list:
        if slot in no_duplicates_list:
            pass
        else:
            no_duplicates_list.append(slot)
    return no_duplicates_list

if __name__ == "__main__":
    user_preference_identifier(parsed_sentence)

