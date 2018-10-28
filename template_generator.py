import csv
#from LSTM import model_trainer, model_user
#Keep track of suggested restaurant if user wants another restaurant
#Make templates and keep track of order in which user states preferences
#aggregation?


#makes a list with lists of possible restaurants
#typical element in restaurant list is [name, pricerange, area, food, phone, addr, postcode]
def csv_reader():
    with open('restaurantinfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        restaurant_info = []
        for row in csv_reader:
            restaurant_info.append(list(row))
        restaurant_info.pop(0)
    return restaurant_info

def speech_act_finder(sentence):
    modelinf = model_trainer()
    model = modelinf[0]
    tokenizer = modelinf[1]
    speech_act = model_user(model, tokenizer, sentence)
    return speech_act

def request_info_finder(restaurant, sentence):
    possible_requests = {"phone": ["phone"],
                         "postcode": ["postcode", "post code"],
                         "addr": ["addr", "address"]}
    for key, value in possible_requests:
        if value in sentence:
            info = key

    if info == "phone":
        return "the phone number is" + str(restaurant[4])
    if info == "addr":
        return "the address is " + str(restaurant[5])
    if info == "postcode":
        return "the postcode is" + str(restaurant[6])
    return

def restaurant_finder(filled_slots, restaurant_info):
    possible_restaurants = []
    values_filled_slots = []

    #make list of slot values which are not None
    for key, value in filled_slots.items():
            values_filled_slots.append(str(value))

    #make list of restaurant values and compare
    for restaurant in restaurant_info:
        info_elements = restaurant[1:4]
        if set(values_filled_slots).issubset(info_elements):
            possible_restaurants.append(restaurant)
    return possible_restaurants

#gets if final restaurant or not (enkelvoud of meervoud zin teruggeven)
def template_generator(filled_slots, speech_act, current_suggested_restaurant):

    #ack,affirm,confirm,deny,inform,negate,null,repeat,reqalts,reqmore,request,restart

    if speech_act == "hello":
        return "Welcome to the team14 restaurant system. You can tell your preference of area , price range or food type. How can we help?"

    # if no preference / slots yet but the speech act is not inform, force them to give preference
    elif (not filled_slots) and (speech_act != 'inform'):
        # ask for restaurant preference
        return "What kind of food would you like?"

    elif (speech_act == "bye") or (speech_act == "thankyou"):
        return "Thank you for using team14 system. eet smakelijk!"

    elif speech_act == "request":
        #TODO which info is asked by user?
        return current_suggested_restaurant

    elif speech_act == "inform":
        # if no restaurant exists with a complete slots: give back to user and ask other preferences
        if len(current_suggested_restaurant) == 0:
            return "We cannot find any restaurant. What other kind of restaurant you like?"

        # if 1 such restaurant exists: return restaurant
        elif len(current_suggested_restaurant) == 1:
            name = str(current_suggested_restaurant[0][0])
            pricerange = str(current_suggested_restaurant[0][1])
            area = str(current_suggested_restaurant[0][2])
            food = str(current_suggested_restaurant[0][3])

            if area != '':
                return '{} is a {} {} restaurant in the are of {}'.format(name, pricerange, food, area)
            else:
                return '{} is a {} {} restaurant'.format(name, pricerange, food)

        # if more: return the number of restaurants and ask for missing slot info
        elif len(current_suggested_restaurant) > 1:
            response = 'There are {} restaurants found. '.format(len(current_suggested_restaurant))

            try:
                filled_slots['pricerange']
            except KeyError:
                response += 'What is your price range? '

            try:
                filled_slots['area']
            except KeyError:
                response += 'Where is your preference area? '

            try:
                filled_slots['food']
            except KeyError:
                response += 'What type of food do you like? '

            return response

if __name__ == "__main__":
    #need to be filled in volgorde van de user als er geen slot is niks meegeven
    filled_slots = {
        "pricerange": "expensive",
        "area": "north",
        "food": "french"
    }
    restaurant_info = csv_reader()
    print(restaurant_finder(filled_slots, restaurant_info))
    #analyze speech act for every sentence
    #keep track of current restaurant




