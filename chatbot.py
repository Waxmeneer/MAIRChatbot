from template_generator import *

user_sentences = {}
current_suggested_restaurant = {}
filled_slots = {}

def dialogue_ender():
    #clear all global variables
    global user_sentences
    global current_suggested_restaurant
    global filled_slots
    filled_slots = {}
    user_sentences = {}
    current_suggested_restaurant = {}

def manager():
    global user_sentences
    global current_suggested_restaurant
    global filled_slots
    user_response = ''
    restaurant_info = csv_reader()
    is_welcome = True

    # start dialogue
    while True:
        # to check if this is just welcome
        if is_welcome:
            speech_act = 'hello'
        # otherwise, check what is the speech act of the user response
        else:
            speech_act = speech_act_finder(user_response)

        # get filled slots, only if the speech act is inform
        if speech_act == 'inform':
            #TODO fill slots real
            filled_slots = {
                "pricerange": "expensive",
                "area": "north",
                "food": "french"
            }

        # read user input
        template_result = template_generator(filled_slots, restaurant_info, speech_act, current_suggested_restaurant)
        #+ store in user_sentences + store speechact as list

        print('System: '+template_result)

        # as long as the template result is not the end of dialogue, then keep expecting user input
        if template_result != 'Thank you for using team14 system. Bye.':
            user_response = input('User: ')
        # ending the dialog by saying bye and exiting the system
        else:
            # end dialogue
            break

        is_welcome = False;


    #else:
        #store filled slots in user sentences
        #check if such restaurant with preferences exist
            #if 1 such restaurant exists: return restaurant
                #store suggested restaurant
            #if more: return multiple restaurants and ask for missing slot info
            #if no restaurant exists: give back to user and ask other preferences


#def sentence_checker(sentence):
    #store user sentence
    #determine speech act

if __name__ == "__main__":
    manager()