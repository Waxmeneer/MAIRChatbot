
from LSTM import model_trainer, model_user


# Keep track of suggested restaurant if user wants another restaurant
# Make templates and keep track of order in which user states preferences
# aggregation?


def template_request(restaurant, sentence):
    possible_requests = {"phone": ["phone"],
                         "postcode": ["postcode", "post code"],
                         "addr": ["addr", "address"],
                         "price": ["price"],
                         "food": ["type"],
                         "area": ["area"]
                         }
    restaurant = restaurant[0]
    info = ''
    for key, values in possible_requests.items():
        for value in values:
            if value in sentence:
                info = key

    if info == "phone":
        return "The phone number of {} is {} ".format(str(restaurant[0]), str(restaurant[4]))
    elif info == "addr":
        return "The address of {} is {} ".format(str(restaurant[0]), str(restaurant[5]))
    elif info == "postcode":
        return "The postcode of {} is {} ".format(str(restaurant[0]), str(restaurant[6]))
    elif info == "price":
        return "The price range of {} is {} ".format(str(restaurant[0]), str(restaurant[1]))
    elif info == "area":
        return "The {} is in the {} part of town ".format(str(restaurant[0]), str(restaurant[2]))
    elif info == "food":
        return "The food type of {} is {} ".format(str(restaurant[0]), str(restaurant[3]))
    else:
        return "Sorry, what information would you like to know about {}? Phone number, address, postcode, price range, area or type of food?".format(
            str(restaurant[0]))


def restaurant_finder(filled_slots, restaurant_info, suggested_restaurants):
    possible_restaurants = []
    values_filled_slots = []

    # make list of slot values which are not None
    for key, value_list in filled_slots.items():
        slot = value_list[1:]
        for value in slot:
            if value == 'random':
                values_filled_slots.append(key)
            else:
                values_filled_slots.append(value)
    # make list of restaurant values and compare
    for restaurant in restaurant_info:
        info_elements = restaurant[1:4]
        if set(values_filled_slots).issubset(info_elements):
            if restaurant not in suggested_restaurants:
                possible_restaurants.append(restaurant)
    return possible_restaurants


def template_restart():
    return "What kind of restaurant would you like?"


def template_bye():
    return "Thank you for using team14 system. eet smakelijk!"


def template_hello():
    return "Welcome to the team14 restaurant system. You can tell your preference of area , price range or food type. How can we help?"

def template_inform(filled_slots, slot_dict, poss_rests, suggested_restaurants, restaurant_info):
    for key, val in slot_dict.items():
        filled_slots[key] = val
    informinfo = inform_to_string(filled_slots, poss_rests, suggested_restaurants, restaurant_info)
    return [informinfo[0],
            informinfo[1]]  # Need to also return suggested_restaurants, as a new restaurant may have been suggested.


# Puts all inform speech act info into a response string, combined with the updated already suggested restaurants.
def inform_to_string(filled_slots, poss_rests, suggested_restaurants, restaurant_info):
    if len(filled_slots.keys()) > 2 and len(poss_rests) > 0 or len(poss_rests)==1:
        suggested_restaurants.append(poss_rests[0])
        return ['Restaurant: \"' + poss_rests[0][0] + '\" is a nice restaurant ' + slots_to_string(filled_slots),
            suggested_restaurants]
    elif len(filled_slots.keys()) < 3 and len(poss_rests) > 0:
        missing_slot = get_missing_slot(filled_slots)
        return ['There are ' + str(len(poss_rests)) + ' restaurants found ' + slots_to_string(
            filled_slots) + 'What ' + missing_slot + ' would you like?', suggested_restaurants]

    else:  # When the amount of possible restaurants is 0
        if len(restaurant_finder(filled_slots, restaurant_info, []))>0: #If there are restaurants, but the user rejected all.
            return ['Sorry but there are no other restaurants ' + slots_to_string(filled_slots) + '\n' +
                    'Could you please change the food, area or pricerange?', suggested_restaurants]
        else:
            return ['Sorry but there are no restaurants ' + slots_to_string(filled_slots) + '\n' +
                    'Could you please change the food, area or pricerange?', suggested_restaurants]


# Gets a slot that is not yet filled.
def get_missing_slot(filled_slots):
    possible_slots = ['food', 'area', 'pricerange']
    for slot in possible_slots:
        if slot not in filled_slots.keys():
            return slot


# Takes the filled slots, orders it by their utterance order, and transforms them to a string to be uttered by the system.
def slots_to_string(filled_slots):
    orderedlist = []
    string = ''
    for key, value in filled_slots.items():
        slots = value[1:]
        order = value[0]
        if key == 'area':
            orderedlist.append([order, 'in the ' + ",".join(slots) + ' part of town'])
        elif key == 'food':
            orderedlist.append([order, 'serving ' + ",".join(slots) + ' food'])
        elif key == 'pricerange':
            orderedlist.append([order, 'with a ' + ",".join(slots) + ' priced menu'])
            orderedlist.sort(key=lambda x: x[0])
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


def template_no_restaurant_found():
    return "We cannot find any restaurant. What other kind of restaurant you like?"


# gets if final restaurant or not (enkelvoud of meervoud zin teruggeven)
def template_generator(filled_slots, slot_dict, suggested_restaurants, restaurant_info, dialogue):
    poss_rests = restaurant_finder(filled_slots, restaurant_info, suggested_restaurants)
    speech_act = dialogue[len(dialogue) - 1][0]
    current_user_sentence = dialogue[len(dialogue) - 1][1]  # At the end of the dialogue list


    current_suggested_restaurant = suggested_restaurants[-1:] #last element of list, if it's empty then returns empty list
    if speech_act == "hello":
        return template_hello()

    # if no preference / slots yet but the speech act is not inform, force them to give preference
    elif ((not filled_slots) and (speech_act != 'inform')) or speech_act == 'restart':
        return template_restart()

    # joni:not restart, but search for another restaurant I guess while holding on to filled slots...
    elif speech_act == 'deny':
        return template_restart()

    elif speech_act == "bye":
        return template_bye()

    elif speech_act == "thankyou":
        return template_bye()

    elif speech_act == "request":

        if len(current_suggested_restaurant) == 0:
            return template_no_restaurant_found()

        # if 1 such restaurant exists: return restaurant info
        elif len(current_suggested_restaurant) == 1:
            return template_request(current_suggested_restaurant, current_user_sentence)

        # if more: return the number of restaurants and ask for missing slot info
        elif len(current_suggested_restaurant) > 1:
            return template_inform_multiple_results(filled_slots, current_suggested_restaurant)

    # negate is similar like inform, only usually started with "no"
    # reqmoe we can repeat the same answer for inform, only confirming
    # confirm  we can repeat the same answer for inform, only confirming
    # affirm this is also another way of confirming
    # ack use a lot words like "um" or "okay", another way of confirming or sometimes adding more info like "hmm how about korean?"
    # null super random, but when we return what we have in inform, it sounds still related
    # reqalts is very similar like inform

    elif speech_act == "inform" \
            or speech_act == "reqmore" \
            or speech_act == "negate" \
            or speech_act == "confirm" \
            or speech_act == "affirm" \
            or speech_act == "ack" \
            or speech_act == "null" \
            or speech_act == "reqalts":
        # if no restaurant exists with a complete slots: give back to user and ask other preferences
        return(template_inform(filled_slots, slot_dict, poss_rests, suggested_restaurants, restaurant_info))

if __name__ == "__main__":
    # need to be filled in volgorde van de user als er geen slot is niks meegeven
    filled_slots = {
        "pricerange": "expensive",
        "area": "north",
        "food": "french"
    }
    restaurant_info = csv_reader()
    print(restaurant_finder(filled_slots, restaurant_info))
    # analyze speech act for every sentence
    # keep track of current restaurant
