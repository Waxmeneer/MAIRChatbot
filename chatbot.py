from template_generator import *
from LSTM import model_user

user_sentences = []
system_sentences = []
current_suggested_restaurant = []
filled_slots = {}

def dialogue_ender():
    #clear all global variables
    global user_sentences
    global current_suggested_restaurant
    global filled_slots
    global system_sentences
    filled_slots = {}
    user_sentences = []
    current_suggested_restaurant = []
    system_sentences = []

def manager():
    global user_sentences
    global current_suggested_restaurant
    global filled_slots
    global system_sentences
    user_response = ''
    restaurant_info = csv_reader()
    is_welcome = True

    # start dialogue
    while True:
        # GET SPEECH ACT
        # to check if this is just welcome
        if is_welcome:
            speech_act = 'hello'
        # otherwise, check what is the speech act of the user response (joni: speech act is always null?)
        else:
            print(user_response, "user_response")
            speech_act = model_user(user_response)
            print(speech_act, "is the classified speech act")

        # STORE SPEECH ACT AND SENTENCE (joni: this works)
        user_sentence = {}
        user_sentence['sentence'] = user_response
        user_sentence['speech_act'] = speech_act
        user_sentences.append(user_sentence)

        # get filled slots, only if the speech act is inform
        if speech_act == 'inform' \
            or speech_act == "reqmore" \
            or speech_act == "negate" \
            or speech_act == "confirm" \
            or speech_act == "affirm" \
            or speech_act == "ack" \
            or speech_act == "null" \
            or speech_act == "reqalts":
            #TODO get real slots value (joni: don't know which part of the parser this is?
            get_filled_slots = {
                "pricerange": "expensive",
                "area": "north",
                "food": "french"
            }
            # STORE / update SLOTS VALUE
            filled_slots = get_filled_slots

            #GET POSSIBLE RESTAURANT
            current_suggested_restaurant = restaurant_finder(filled_slots, restaurant_info)

        # if user wants us to repeat last sentence do that otherwise, find template
        if speech_act == 'repeat':
            template_result = system_sentences[-1]
        else:
            template_result = template_generator(filled_slots, speech_act, current_suggested_restaurant, user_response)
        #store system sentences
        system_sentences.append(template_result)

        print('System: '+template_result)

        # if no restaurant found or user wants to reset, restart the dialogue
        if template_result == "We cannot find any restaurant. What other kind of restaurant would you like?"\
            or speech_act == 'deny':
            dialogue_ender()

        # as long as the template result is not the end of dialogue, then keep expecting user input
        if template_result != 'Thank you for using team14 system. Bye.':
            user_response = input('User: ')
        # ending the dialog by saying bye and exiting the system
        else:
            # END DIALOGUE
            break

        is_welcome = False

if __name__ == "__main__":
    manager()
