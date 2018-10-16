variable_keyword_link = {
    "addr": [],
    "area": ["town", "part"],
    "food": ["restaurant", "food"],
    "phone": [],
    "pricerange": ["restaurant", "priced"],
    "postcode": [],
    "signature": [],
    "name": []
}

#import .json ontology



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
