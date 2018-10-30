import sys
from template_generator import *
from LSTM import model_user, model_trainer, load_tokenizer, load_model, load_speechactdict

sys.path.insert(0, 'Parsing')
from variable_keyword_link import slot_dict

dialogue = []
suggested_restaurants = []
filled_slots = {}


def dialogue_ender():
    # clear all global variables
    global suggested_restaurants, filled_slots, asked_slots
    filled_slots = {}
    dialogue.clear()
    current_suggested_restaurant.clear()
    asked_slots.clear()


def manager():
    global dialogue, suggested_restaurants, filled_slots
    user_response = ''
    model, tokenizer, speechactdict = load_model(), load_tokenizer(), load_speechactdict()
    restaurant_info = csv_reader()
    is_welcome = True
    order=0
    # start dialogue
    print("Welcome to the Chatbot system: ")
    print("What kind of restaurant are you looking for? You can ask for example for food type, area or pricerange.")
    while True:
        # get speech act of the user input.
        inp = input("user: ")
        speech_act = model_user(inp, model, tokenizer, speechactdict)
        slots = slot_dict(inp)
        orderinfo=update_order(order, slots)
        order, slots = orderinfo[0], orderinfo[1]
        filled_slots = slot_change(filled_slots, slots, speech_act, dialogue)
        dialogue.append([speech_act, inp])
        
        print(speech_act, "is the classified speech act")
        """
        # if user wants us to repeat last sentence do that otherwise, find template
        if speech_act == 'repeat':
            template_result = system_sentences[-1]
        
        #Get asked slots of previous system utterance 
        elif speech_act == 'inform' and len(suggested_restaurants) > 1:
            result = template_generator(filled_slots, speech_act, suggested_restaurants, dialogue)
            template_result = result[0]
            asked_slots = result[1]
            print(asked_slots)
        else:"""
        template_result = template_generator(filled_slots, speech_act, suggested_restaurants, dialogue)
        template_str = template_result[0]
        template_sug = template_result[1]
        # store system sentences
        dialogue.append([99, template_str]) #99 is an arbitrary speech act.

        print('System: ' + template_str)

        # if no restaurant found or user wants to reset, restart the dialogue
        if template_str == "We cannot find any restaurant. What other kind of restaurant would you like?" \
                or speech_act == 'deny':
            dialogue_ender()

        # as long as the template result is not the end of dialogue, then keep expecting user input
        if template_str != 'Thank you for using team14 system. Bye.':
            user_response = input('User: ')
        # ending the dialog by saying bye and exiting the system
        else:
            # END DIALOGUE
            break

        is_welcome = False
        
def slot_change(filled_slots, slots, speech_act, dialogue):
    if speech_act == 'inform':
        for key, val in slots.items():
            print(slots)
            filled_slots[key]=val
    elif speech_act == 'request':
        pass
    elif speech_act == 'negate':
        pass
    return filled_slots

def update_order(order, slot_dict):
    count=0
    for item in slot_dict.values():
        for slot in item:
            slot[1]+=order
            count+=1
    order+=count
    return[order, slot_dict]
        
if __name__ == "__main__":
    manager()
