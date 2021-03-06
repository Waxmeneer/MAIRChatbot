import sys, csv
from template_generator import *
from LSTM import model_user, model_trainer, load_tokenizer, load_model, load_speechactdict
sys.path.insert(0, 'Parsing') # The python files which involves parsing are situated in the parsing folder.
from variable_keyword_link import slot_dict
from sent_converter import convertsentence as convsent

# These global variables keep state of the conversation.
dialogue = []
suggested_restaurants = []
filled_slots = {}
empty_slots = ["food", "area", "pricerange"]
order = 0
suggested_slot = None

# These words either occur very rarely in the training corpus, leading to the classifier making mistakes, or are not yet
# in our dictionary. They directly indicate what the user wants the chatbot to do. These overrule the speech act generated
# by the classifier.
specialwords = {'restart': ['start over', 'restart', 'start again', 'reset'],
                'bye': ['bye','end', 'goodbye'],
                'any': ["any", "don't care", 'anything', "don't mind", "whatever", "whichever", "don't care"],
                'options': ['options', 'possibilities', 'help']}

# This function makes a list with lists of possible restaurants.
# Elements in the restaurant list are [name, pricerange, area, food, phone, addr, postcode]
def csv_reader():
    with open('restaurantinfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        restaurant_info = []
        for row in csv_reader:
            restaurant_info.append(list(row))
        restaurant_info.pop(0)
    return restaurant_info

# This function clears all global variables, in case of a restart or deny.
def clear_vars():
    global suggested_restaurants, filled_slots, suggested_slot, empty_slots
    filled_slots = {}
    dialogue.clear()
    suggested_restaurants.clear()
    empty_slots =["food", "area", "pricerange"]
    suggested_slot = None

# The main function. It handles the information gathering and template generation and also keeps track of the filled slots.
def manager():
    global dialogue, suggested_restaurants, filled_slots, empty_slots, order, suggested_slot
    model, tokenizer, speechactdict = load_model(), load_tokenizer(), load_speechactdict()
    restaurant_info = csv_reader()
    print(template_hello())
    # This function loops, only stopping when the user says goodbye.
    while True:
        # Gets the uttered user sentence, spelling checks it using Lehvenstein distance and rejoins the produced list.
        inp = input("User: "); splitinp = convsent(inp); inp = ' '.join(splitinp)
        speech_act = model_user(inp, model, tokenizer, speechactdict) #in the lstm.py file
        slots = slot_dict(inp)
        orderinfo = update_order(order, slots)
        order, slots = orderinfo[0], orderinfo[1]
        filled_slots = slot_change(filled_slots, slots, speech_act)
        # Updates the list of empty slots
        filled_keys = filled_slots.keys()
        for keys in filled_keys:
            if keys in empty_slots:
                empty_slots.remove(keys)
        # Certain words force the program to fill it slots with 'any' or determine the speech act by force.
        for key, list in specialwords.items():
            for value in list:
                if value in splitinp:
                    if key=='any':
                        any_filler(filled_slots, suggested_slot)
                    else:
                        speech_act = speech_act.replace(speech_act, key) # It overrules the speech_act in utterances as 'restart'.
        dialogue.append([speech_act, inp])
        template_result = template_generator(filled_slots, slots, suggested_restaurants, suggested_slot, restaurant_info, dialogue)
        if speech_act in informacts: # The list of acts similar to inform is present in the template_generator file.
            template_str = template_result[0]
            new_sugrest = template_result[1]
            if template_result[2]!= None:
                suggested_slot = template_result[2]
            suggested_restaurants = new_sugrest
        else:
            template_str = template_result
        # Stores system sentences in the dialogue list.
        dialogue.append([None, template_str])  # Stores it without speech act
        print('')
        print('System: ' + template_str)
        # If no restaurant found or user wants to reset, restarts the dialogue
        if speech_act == 'deny' or speech_act == 'restart':
            clear_vars()
        if speech_act == 'bye':
            break

# Fills the slots
def slot_change(filled_slots, slots, speech_act):
    if speech_act == 'inform':
        for key, val in slots.items():
            filled_slots[key] = val
    return filled_slots

# Order is kept to distinguish when a user uttered which slot.
def update_order(order, slot_dict):
    count = 0
    for item in slot_dict.values():
        item[0] += order #Every first element is the order
        count += 1
    order += count
    return [order, slot_dict]

#this functions fills any unfilled slots with the "any" dontcare value
def any_filler(filled_slots, suggested_slot):
    global order
    if suggested_slot==None:
        for slot in empty_slots:
            order+=1
            filled_slots[slot] = [order,"any"]
    else:
        filled_slots[suggested_slot]=[order,"any"]

if __name__ == "__main__":
    manager()