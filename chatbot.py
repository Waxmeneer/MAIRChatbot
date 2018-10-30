import sys
from template_generator import *
from LSTM import model_user, model_trainer, load_tokenizer, load_model, load_speechactdict

sys.path.insert(0, 'Parsing')
from variable_keyword_link import slot_dict

user_sentences = []
system_sentences = []
current_suggested_restaurant = []
filled_slots = {}


def dialogue_ender():
    # clear all global variables
    global user_sentences
    global current_suggested_restaurant
    global filled_slots
    global system_sentences
    global asked_slots
    filled_slots = {}
    user_sentences = []
    current_suggested_restaurant = []
    system_sentences = []
    asked_slots = []


def manager():
    global user_sentences
    global current_suggested_restaurant
    global asked_slots
    global filled_slots
    global system_sentences
    user_response = ''
    model, tokenizer, speechactdict = load_model(), load_tokenizer(), load_speechactdict()
    restaurant_info = csv_reader()
    is_welcome = True
    # start dialogue
    while True:
        # get speech act of the user input. Get hello for the first loop
        if is_welcome:
            speech_act = 'hello'
        else:
            speech_act = model_user(user_response, model, tokenizer, speechactdict)

        # STORE SPEECH ACT AND SENTENCE
        user_sentence = {}
        print(speech_act, "is the classified speech act")
        user_sentence['sentence'] = user_response
        user_sentence['speech_act'] = speech_act
        user_sentences.append(user_sentence)
        
        #TODO working on adding random to slot values if user doesn't have preference
        # get filled slots, only if the speech act is inform
        if speech_act == "inform" and filled_slots == filled_slots.update(slot_dict(user_response)):
            if asked_slots is not None:
                for asked_slot in asked_slots:
                    filled_slots.update({asked_slot: [['random']]})
                    print(filled_slots, "random added to filled slots")

        if speech_act == "inform" \
                or speech_act == "reqmore" \
                or speech_act == "negate" \
                or speech_act == "confirm" \
                or speech_act == "affirm" \
                or speech_act == "ack" \
                or speech_act == "null" \
                or speech_act == "reqalts":
            # STORE / update SLOTS VALUE
            filled_slots.update(slot_dict(user_response))
            print(filled_slots)


            # GET POSSIBLE RESTAURANT
            current_suggested_restaurant = restaurant_finder(filled_slots, restaurant_info)

        # if user wants us to repeat last sentence do that otherwise, find template
        if speech_act == 'repeat':
            template_result = system_sentences[-1]

        elif speech_act == 'inform' and len(current_suggested_restaurant) > 1:
            result = template_generator(filled_slots, speech_act, current_suggested_restaurant, user_response)
            template_result = result[0]
            asked_slots = result[1]
            print(asked_slots)
        else:
            template_result = template_generator(filled_slots, speech_act, current_suggested_restaurant, user_response)
        # store system sentences
        system_sentences.append(template_result)

        print('System: ' + template_result)

        # if no restaurant found or user wants to reset, restart the dialogue
        if template_result == "We cannot find any restaurant. What other kind of restaurant would you like?" \
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
