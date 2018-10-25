import csv

#Keep track of suggested restaurant if user wants another restaurant
#Make templates and keep track of order in which user states preferences
#aggregation?


#makes a list with lists of possible restaurants
#typical element in restaurant list is [name, pricerange, area, food, phone, addr, postcode]
def csv_reader():
    with open('C:/Users/joniv/Documents/AI_courses/MAIR/MAIR_lab/MAIRChatbot-master/restaurantinfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        restaurant_info = []
        for row in csv_reader:
            restaurant_info.append(list(row))
        restaurant_info.pop(0)
    return restaurant_info

def restaurant_finder(filled_slots, restaurant_info):
    possible_restaurants = []
    values_filled_slots = []

    for key, value in filled_slots.items():
            values_filled_slots.append(str(value))

    #make list of restaurant values and compare
    for restaurant in restaurant_info:
        info_elements = restaurant[1:4]
        if set(values_filled_slots).issubset(info_elements):
            print("found restaurant")
            possible_restaurants.append(restaurant)


    if len(possible_restaurants) == 1:
        return str(restaurant[0]) + " is a nice place " + str(template_generator(filled_slots, 1))
    else:
        return "there are " + str(len(possible_restaurants)) + " restaurants" + str(template_generator(filled_slots, 0))


#gets if final restaurant or not (enkelvoud of meervoud zin teruggeven)
def template_generator(filled_slots, final_restaurant):
    #TODO make templates
    return " hello"

if __name__ == "__main__":
    #need to be filled in volgorde van de user als er geen slot is niks meegeven
    filled_slots = {
        "pricerange": "expensive",
        "area": "north",
        "food": "french"
    }
    restaurant_info = csv_reader()
    print(restaurant_finder(filled_slots, restaurant_info))




