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
def template_generator(filled_slots, restaurant_info, speech_act, current_restaurant):

    #ack,affirm,confirm,deny,inform,negate,null,repeat,reqalts,reqmore,request,restart

    if speech_act == "hello":
        return "Welcome to the team14 restaurant system. You can tell your preference of area , price range or food type. How can we help?"

    # if no preference / slots yet but the speech act is not inform
    elif (not filled_slots) and (speech_act != 'inform'):
        # ask for restaurant preference
        return "What kind of food would you like?"

    elif speech_act == "bye" or "thankyou":
        return "Thank you for using team14 system. Bye."

    elif speech_act == "request":
        #TODO which info is asked by user?
        return restaurant_finder(filled_slots, restaurant_info)

    elif speech_act == "inform":
        if len(restaurant_finder(filled_slots, restaurant_info)) == 1:
            restaurant = restaurant_finder(filled_slots, restaurant_info)
            return str(restaurant[0]) + "is a nice place"


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




