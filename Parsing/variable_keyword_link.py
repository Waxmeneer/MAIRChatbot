import json

variable_keyword_link = {
    "area": ["town", "part"],
    "food": ["restaurant", "food"],
    "pricerange": ["restaurant", "priced"],
    "name": []
}

def read_json(file):
    with open(file) as d:
        ontology_dstc2 = json.load(d)
        informable_dict = ontology_dstc2["informable"]
    print(informable_dict)

#select smallest parsed_sentence with type s as input
def user_preference_identifier(parsed_sentence):
    #list with slot values = empty
    #per value_slot search if trigger word is present
        #if not return NULL
        #else
            #look at parsing tree sentence and search for leafs with trigger word
                #if found > search for accompanying leafs with keyword
                    #put all nodes in list (double nodes excluded)
                    #make value equal to last of nodelist
    #check if nodelists for different values are disjoint
    if __name__ == "__main__":
        read_json('C:/Users/joniv/Documents/MAIR_lab/chatbot project/results/ontology_dstc2.json')
