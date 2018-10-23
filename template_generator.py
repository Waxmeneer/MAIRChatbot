
def restaurant_finder(filled_slots):
    #if not all slots are filled
        #n of restaurants + info of slots + additional question about empty slot
        #restaurant
    #if all slots filled
        #restaurant = name
        #system_utterance = print(restaurant) + info of slots

    return system_utterance, restaurant

def info_finder(restaurant, request):
    #request_value = find request header in . csv in row of restaurant
    system_utterance = "The" + print(request) + "of"+ print(restaurant) + "is" + print(request_value)
    return system_utterance

def template_generator(speech_act, sentence):
    filled_slots = []
    restaurant = ""
    system_utterance = []


    #if speech act = inform()
        #update filled slots
            #if no value provided > update with random
        #system_utterance = restaurant_finder(filled_slots)
        # if system utterance starts with name
            #update restaurant
    #if speech act = request()
        #what is request?
        #system_utterance = info_finder(restaurant)


    return system_utterance
