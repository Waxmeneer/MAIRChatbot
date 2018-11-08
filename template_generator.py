import random
from LSTM import model_trainer, model_user


# Keep track of suggested restaurant if user wants another restaurant
# Make templates and keep track of order in which user states preferences
# aggregation?

#In our program, these speech acts should get the same treatment as if they were inform speech acts.
informacts = ["inform", "reqmore", "negate", "affirm", 'ack', "null", "reqalts"]

# gets if final restaurant or not (enkelvoud of meervoud zin teruggeven)
def template_generator(filled_slots, slot_dict, suggested_restaurants, suggested_slot, restaurant_info, dialogue):
    poss_rests = restaurant_finder(filled_slots, restaurant_info, suggested_restaurants)
    speech_act = dialogue[len(dialogue) - 1][0]
    current_user_sentence = dialogue[len(dialogue) - 1][1]  # At the end of the dialogue list
    current_suggested_restaurant = suggested_restaurants[-1:] #last element of list, if it's empty then returns empty list
    if speech_act == "hello":
        return template_hello()
    # if no preference / slots yet but the speech act is not inform, force them to give preference
    #elif ( speech_act!='bye' and (not filled_slots) and (speech_act not in informacts)) or speech_act == 'restart':
        #return template_restart()
    # joni:not restart, but search for another restaurant I guess while holding on to filled slots...
    elif speech_act == 'deny': return template_restart()
    elif speech_act == 'restart': return template_restart()
    elif speech_act == "bye": return template_bye()
    elif speech_act == "thankyou": return template_bye()
    elif speech_act == 'options': return template_options(suggested_slot, poss_rests)
    elif speech_act == "confirm": return template_confirm(slot_dict, current_suggested_restaurant)
    elif speech_act == "request":
        if len(current_suggested_restaurant) == 0:
            return template_no_restaurant_found()
        # if 1 such restaurant exists: return restaurant info
        elif len(current_suggested_restaurant) == 1:
            return template_request(current_suggested_restaurant, current_user_sentence)
        # if more: return the number of restaurants and ask for missing slot info
        elif len(current_suggested_restaurant) > 1:
            return template_inform_multiple_results(filled_slots, current_suggested_restaurant)
    elif speech_act in informacts:
        # if no restaurant exists with a complete slots: give back to user and ask other preferences
        return(template_inform(filled_slots, slot_dict, poss_rests, suggested_restaurants, restaurant_info))


def template_request(restaurant, sentence):
    possible_requests = {"phone": ["phone"],
                         "postcode": ["postcode", "post code"],
                         "addr": ["addr", "address"],
                         "price": ["price"],
                         "food": ["type"],
                         "area": ["area"]}
    restaurant = restaurant[0]
    template = {}
    info=''
    for key, values in possible_requests.items():
        for value in values:
            if value in sentence:
                info = key

    if info == "phone":
        template[0] = "The phone number of {} is {} ".format(str(restaurant[0]), str(restaurant[4]) if str(restaurant[4]) else "unknown")
        template[1] = "The number is {} ".format(str(restaurant[4]) if str(restaurant[4]) else "unknown")
    elif info == "addr":
        template[0] = "The address of {} is {} ".format(str(restaurant[0]),str(restaurant[5]) if str(restaurant[5]) else "unknown")
        template[1] = "The address is {} ".format(str(restaurant[5]) if str(restaurant[5]) else "unknown")
    elif info == "postcode":
        template[0] = "The postcode of {} is {} ".format(str(restaurant[0]),str(restaurant[6]) if str(restaurant[6]) else "unknown")
        template[1] = "The postcode is {} ".format(str(restaurant[6]) if str(restaurant[6]) else "unknown")
    elif info == "price":
        template[0] = "The price range of {} is {} ".format(str(restaurant[0]),str(restaurant[1]) if str(restaurant[1]) else "unknown")
        template[1] = "The price range is {} ".format(str(restaurant[1]) if str(restaurant[1]) else "unknown")
    elif info == "area":
        template[0] = "The {} is in the {} part of town ".format(str(restaurant[0]), str(restaurant[2]) if str(restaurant[2]) else "unknown")
        template[1] = "The location is in the {} part of town ".format(str(restaurant[2]) if str(restaurant[2]) else "unknown")
    elif info == "food":
        template[0] = "The food type of {} is {} ".format(str(restaurant[0]),str(restaurant[3]) if str(restaurant[3]) else "unknown")
        template[1] = "The food type is {} ".format(str(restaurant[3]) if str(restaurant[3]) else "unknown")
    else:
        template[0] = "Sorry, what information would you like to know about {}? Phone number, address, postcode, price range, area or type of food?".format(str(restaurant[0]))
        template[1] = "Would you like some information about {}? You can ask the following information: Phone number, address, postcode, price range, area or type of food?".format(str(restaurant[0]))
    return return_random(template)

def template_options(suggested_slot, poss_rests):
    templates=[]
    mapping_dict = {'pricerange':1, 'area':2, 'food':3}
    optionlist = []
    c=0
    if suggested_slot == None:
        for restaurant in poss_rests:
            for value in mapping_dict.values():
                if value!='':
                    optionlist.append(restaurant[value])
        optionset = set(optionlist)
        templates.append("All the options include: {}".format(' '.join(optionset)))
        templates.append("The options are: {}".format(' '.join(optionset)))
    else:
        for restaurant in poss_rests:
            optionlist.append(restaurant[mapping_dict[suggested_slot]])
        optionset = set(optionlist)
        templates.append("All options for the {} include: {}".format(suggested_slot,' '.join(optionset)))
        templates.append("The possibilities for the {} are: {}".format(suggested_slot,' '.join(optionset)))
    return(random.choice(templates))

def template_restart():
    template = []
    template+= 100* ["I have reset the preferences. Could you please specify your preferences again?"]
    template+= 100*["What kind of restaurant would you like?"]
    template+=["BEEP BOOP I HAVE RESTARTED. WHAT ARE YOUR PREFERENCES, FELLOW HUMAN?"] #Easter egg, 1/200 chance
    return random.choice(template)

def template_bye():
    template = []
    template.append("Thank you for using team14 system. Eet smakelijk!")
    template.append("Bye, enjoy your meal!")
    return random.choice(template)

def template_hello():
    template = {}
    template[0] = "\nSystem: Welcome to the team14 restaurant system. You can tell your preference of area , price range or food type. How can we help?"
    template[1] = "\nSystem: Hi, Welcome to the team14 restaurant system. We can help you to find a restaurant based on the area, type of food or price range you like"
    return return_random(template)

def template_inform(filled_slots, slot_dict, poss_rests, suggested_restaurants, restaurant_info):
    for key, val in slot_dict.items():
        filled_slots[key] = val
    informinfo = inform_to_string(filled_slots, poss_rests, suggested_restaurants, restaurant_info)
    return [informinfo[0], informinfo[1], informinfo[2]]  # Need to also return suggested_restaurants, as a new restaurant may have been suggested. Also the asked slot


def template_no_restaurant_found():
    template = {}
    template[0] = "No restaurant is found in our system. Perhaps different preferences?"
    template[1] = "We cannot find any restaurant. What other kind of restaurant you like?"
    return return_random(template)

def template_confirm(slot_dict, current_suggested_restaurant):
    restaurant = current_suggested_restaurant

    template = {}
    for key, value in slot_dict.items():

        if key == "pricerange":
            data_number = 1
            text_slot = "price range"
        elif key == "area":
            data_number = 2
            text_slot = "area"
        elif key == "food":
            data_number = 3
            text_slot = "food type"
        else:
            data_number = 0

        if data_number != 0:
            if value[1] == str(restaurant[data_number]):
                template[0] = "Yes"
                template[1] = "You are Right"
            else:
                template[0] = "No"
                template[1] = "Nope"

            template[0] += ", the {} of {} is {}".format(text_slot, str(restaurant[0]), str(restaurant[data_number]))
            template[1] += ", the {} of {} is actually {}".format(text_slot, str(restaurant[0]), str(restaurant[data_number]))

            if value[1] != str(restaurant[data_number]):
                template[0] += ", not {}".format(value[1])

    if template[0] == '':
        template[0] = "Sorry, what do you want to confirm? the area, the price range or food type"
    if template[1] == '':
        template[1] = "You can confirm one of the following information; the area, the price range or food type ?"
    return return_random(template)

#this function picks a random restaurant out of a list of possible restaurants
def random_restaurant_picker(list_of_restaurants):
    try: #If the list of restaurants is empty, it can't perform random.choice.
        random_restaurant = random.choice(list_of_restaurants)
    except:
        random_restaurant = []
    return [random_restaurant]


def restaurant_finder(filled_slots, restaurant_info, suggested_restaurants):
    # this function removes all 'dont care' slots out of the list, then searches for all possible remaining restaurants and picks one at random, should probably make this into it's own function sometime in the future
    values_filled_slots_pruned = []
    possible_restaurants_pruned = []
    filled_slots_pruned = {key: value for (key, value) in filled_slots.items() if value[1] != "any"}
    if filled_slots_pruned != filled_slots:
        for key, value_list in filled_slots_pruned.items():
            value = value_list[1]
            values_filled_slots_pruned.append(value)
        for restaurant in restaurant_info:
            info_elements = restaurant[1:4]
            if set(values_filled_slots_pruned).issubset(info_elements) and restaurant not in suggested_restaurants:
                possible_restaurants_pruned.append(restaurant)
        return possible_restaurants_pruned
    possible_restaurants = []
    for restaurant in restaurant_info:
        info_elements = restaurant[1:4]
        if(slots_in_restinfo(filled_slots_pruned, info_elements)):
            if restaurant not in suggested_restaurants:
                possible_restaurants.append(restaurant)
    return possible_restaurants

#The idea of this function is that it checks if slots are in the restaurant info, and it even works if a slot like
#food has multiple values, like "chinese or french".
def slots_in_restinfo(filled_slots, info_elements):
    for key, value in filled_slots.items():
        slot_in_rest = False
        for slot in value:
            if slot in info_elements:
                slot_in_rest = True
        if slot_in_rest==False:
            return False
    return True

# choose one random template from all given possible templates
def return_random(template):
    max = len(template) - 1
    return template[random.randint(0, max)]


# Puts all inform speech act info into a response string, combined with the updated already suggested restaurants.
def inform_to_string(filled_slots, poss_rests, suggested_restaurants, restaurant_info):
    template = {}
    missing_slot = None
    if(len(filled_slots.keys())) == 0: #In this case, the function returns a standard string.
        return("What kind of restaurant would you like?", suggested_restaurants, missing_slot)
    if len(filled_slots.keys()) > 2 and len(poss_rests) > 0 or len(poss_rests)==1:
        suggested_restaurants.append(poss_rests[0])
        template[0] = "Restaurant: \"{}\" is a nice restaurant {}".format(poss_rests[0][0], slots_to_string(filled_slots, poss_rests[0]))
        template[1] = "We believe this restaurant is the perfect restaurant for you: \"{}\", {}".format(poss_rests[0][0], slots_to_string(filled_slots, poss_rests[0]))
    elif len(filled_slots.keys()) < 3 and len(poss_rests) > 0:
        missing_slot = get_missing_slot(filled_slots)
        template[0] = 'There are {} restaurants found {}What {} would you like?'.format(str(len(poss_rests)), slots_to_string(filled_slots, []), missing_slot)
        template[1] = 'We found {} restaurants {}What is your {} preference?'.format(str(len(poss_rests)), slots_to_string(filled_slots, []), missing_slot)
    else:  # When the amount of possible restaurants is 0
        if len(restaurant_finder(filled_slots, restaurant_info,[])) > 0:  # If there are restaurants, but the user rejected all.
            template[0] = 'Sorry but there are no other restaurants {}\nSystem: Could you please change the food, area or pricerange? To fully restart, type \'restart\'.'.format(slots_to_string(filled_slots, []))
            template[1] = 'Unfortunately we could not find any other restaurants {}\nCould you perhaps specify different food, area or pricerange? To restart altogether, type \'restart\'.'.format(slots_to_string(filled_slots, []))
        else:
            template[0] = 'Sorry but there are no restaurants {}\nSystem: Could you please change the food, area or pricerange? To fully restart, type \'restart\'.'.format(slots_to_string(filled_slots, []))
            template[1] = 'Unfortunately we could not find any restaurants {} \nSystem: Could you perhaps choose a different food type, area or pricerange? To restart altogether, type \'restart\'.'.format(slots_to_string(filled_slots, []))
    return [return_random(template), suggested_restaurants, missing_slot]

# Gets a slot that is not yet filled.
def get_missing_slot(filled_slots):
    possible_slots = ['food', 'area', 'pricerange']
    random.shuffle(possible_slots) #Possible slots is shuffled, so that the system doesn't always ask the user in the same order.
    for slot in possible_slots:
        if slot not in filled_slots.keys():
            return slot


# Takes the filled slots, orders it by their utterance order, and transforms them to a string to be uttered by the system.
def slots_to_string(filled_slots, restaurant):
    orderedlist = []
    string = ''
    for key, value in filled_slots.items():
        slots = value[1:]
        order = value[0]
        if key == 'area':
            if ('any' in slots and restaurant!=[]) or restaurant!=[] : #If the slot is any, the function should return the info from the restaurant instead of the user input.
                templates = ['in the ' + restaurant[2] + ' part of town', 'in the ' + restaurant[2] + ' district of town']
            else:
                templates = ['in the ' + " or ".join(slots) + ' part of town', 'in the ' + " or ".join(slots) + ' district of town']
            orderedlist.append([order, return_random(templates)])
        elif key == 'food':
            if ('any' in slots and restaurant!=[]) or restaurant!=[]:
                orderedlist.append([order, 'serving ' + restaurant[3] + ' food'])
            else:
                orderedlist.append([order, 'serving ' + " or ".join(slots) + ' food'])
        elif key == 'pricerange':
            if ('any' in slots and restaurant!=[]) or restaurant!=[]:
                templates = ['with ' + restaurant[1] + ' priced meals', 'having ' + restaurant[1] + ' prices']
            else:
                templates = ['with ' + " or ".join(slots) + ' priced meals', 'having ' + " or ".join(slots) + ' prices']
            orderedlist.append([order, return_random(templates)])
    orderedlist.sort(key=lambda x: x[0]) #sorts the list by the order variable.
    for slot in orderedlist:
        string += slot[1]
        try: #If in some case the orderlist is empty, this catches it.
            if slot == orderedlist[-1]: #The last element is the end of the sentence
                string+='. '
            else:
                string+=' '
        except:
            pass
    return string
