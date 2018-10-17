import json

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
with open('C:/Users/joniv/Documents/MAIR_lab/chatbot project/results/ontology_dstc2.json') as d:
    ontology_dstc2 = json.load(d)
    informable_dict = ontology_dstc2["informable"]



#select smallest parsed_sentence with type s as input
def user_preference_identifier(parsed_sentence):
    #list with slot values = empty

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
    substring_finder(found_word_list, parsed_sentence)
                           

def substring_finder(found_word_list, parsed_sentence):
    substring_list = []
    for substring in parsed_sentence:
        if all(word in substring for word in found_word_list):
            substring_list.append(substring)
    shortest_substring = min(substring_list, key=len)
    print(shortest_substring + " ANTWOORD")
    return shortest_substring

if __name__ == "__main__":
    user_preference_identifier(parsed_sentence)
