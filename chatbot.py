import sys, csv
from template_generator import *
from LSTM import model_user, model_trainer, load_tokenizer, load_model, load_speechactdict

sys.path.insert(0, 'Parsing')
from variable_keyword_link import slot_dict

dialogue = []
suggested_restaurants = []
filled_slots = {}

# makes a list with lists of possible restaurants
# typical element in restaurant list is [name, pricerange, area, food, phone, addr, postcode]
def csv_reader():
    with open('restaurantinfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        restaurant_info = []
        for row in csv_reader:
            restaurant_info.append(list(row))
        restaurant_info.pop(0)
    return restaurant_info



def dialogue_ender():
    # clear all global variables
    global suggested_restaurants, filled_slots, asked_slots
    filled_slots = {}
    dialogue.clear()
    suggested_restaurants.clear()
    asked_slots.clear()


def manager():
    global dialogue, suggested_restaurants, filled_slots
    user_response = ''
    model, tokenizer, speechactdict = load_model(), load_tokenizer(), load_speechactdict()
    restaurant_info = csv_reader()
    is_welcome = True
    order = 0
    # start dialogue
    print(template_hello())
    while True:
        # get speech act of the user input.
        inp = input("user: ")
        speech_act = model_user(inp, model, tokenizer, speechactdict)
        slots = slot_dict(inp)
        orderinfo = update_order(order, slots)
        order, slots = orderinfo[0], orderinfo[1]
        filled_slots = slot_change(filled_slots, slots, speech_act, dialogue)
        dialogue.append([speech_act, inp])

        # if user wants us to repeat last sentence do that otherwise, find template
        #if speech_act == 'repeat':
         #   template_result = system_sentences[-1]

        template_result = template_generator(filled_slots, slots, suggested_restaurants, restaurant_info, dialogue)
        try: #Suggested restaurants only changes on inform.
            template_str = template_result[0]
            template_sug = template_result[1]
            suggested_restaurants = template_sug
        except:
            template_str = template_result
        # store system sentences
        dialogue.append([99, template_str])  # 99 is an arbitrary speech act.
        print('')
        print('System: ' + template_str)
        # if no restaurant found or user wants to reset, restart the dialogue
        if template_str == "We cannot find any restaurant. What other kind of restaurant would you like?" \
                or speech_act == 'deny':
            dialogue_ender()


def slot_change(filled_slots, slots, speech_act, dialogue):
    if speech_act == 'inform':
        for key, val in slots.items():
            filled_slots[key] = val
    elif speech_act == 'request':
        pass
    elif speech_act == 'negate':
        pass
    return filled_slots


def update_order(order, slot_dict):
    count = 0
    for item in slot_dict.values():
        item[0] += order #Every first element is the order
        count += 1
    order += count
    return [order, slot_dict]


if __name__ == "__main__":
    manager()