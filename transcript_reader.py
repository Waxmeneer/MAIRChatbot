import json
import os

#FUNCTION LIST
#=============================================================================
#function to load json file
def load_js_file_to_object( dirName, fileName ):
    completeFileAddress =  os.path.join(dirName, fileName)
    with open(completeFileAddress) as json_file:
        return json.load(json_file)

#function to calculate the biggest dialog length
def calculate_biggest_dialog_length( user, system ):
    userLen = len(user["turns"])
    systemLen = len(system["turns"])
    biggestLen = 0

    if userLen > systemLen:
        biggestLen = userLen
    else:
        biggestLen = systemLen

    return biggestLen

#function to print in console or/and write to file
def print_write_data( preText, data ):
    text = preText + data
    print(text)
    if (isPrint):
        newFile.write(text + "\r\n")
#=============================================================================

#CONFIGURATION
#=============================================================================
fileName = "dialog_combined_results.txt"
directoryToSearch = '.'
#=============================================================================

#START HERE

#console questions
while True:
    data = input("Select one option: (a)console, (b)print in one big file   ")
    if data.lower() not in ('a', 'b'):
        print("Invalid answer")
    else:
        break

# check print or console
isPrint = False if data.lower() == 'a' else True

#open file start writting
if isPrint:
    newFile = open(fileName,"w+")

number = 1;

#looping through list of all directory in current directory
for dirName, dirNames, fileNames in os.walk(directoryToSearch):
    # only taking directory that has 'voip' in its name
    if 'voip' in dirName:

        #load the json file
        user = load_js_file_to_object(dirName, 'label.json')
        system = load_js_file_to_object(dirName, 'log.json')

        #get length for the biggest, user and system length
        biggestLen = calculate_biggest_dialog_length(user, system)
        userLen = len(user["turns"])
        systemLen = len(system["turns"])

        #print dialog information
        print_write_data('number: ', str(number))
        print_write_data('session id: ', user["session-id"])
        print_write_data('', user["task-information"]["goal"]["text"])

        #print dialgo turns
        #looping through every turn
        for i in range(biggestLen):
            if i+1 <= systemLen:
                print_write_data('system: ', system["turns"][i]["output"]["transcript"])

            if i+1 <= userLen:
                print_write_data('user: ', user["turns"][i]["transcription"] )

        #end of dialog
        if isPrint:
            newFile.write("\r\n")
        else:
            print('===========================')
            input('Press enter to continue: ')

        number = number + 1

# close file
if isPrint:
    newFile.close()
