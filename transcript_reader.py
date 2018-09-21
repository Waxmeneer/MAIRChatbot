import json, sys,os, re

#FUNCTION LIST
#=============================================================================
#Function to load the json files.
def load_js_file_to_object( dirName, fileName ):
    completeFileAddress =  os.path.join(dirName, fileName)
    with open(completeFileAddress) as json_file:
        return json.load(json_file)

#Function that returns the biggest dialogue length.
def calculate_biggest_dialog_length( user, system ):
    userLen = len(user["turns"])
    systemLen = len(system["turns"])
    biggestLen = 0

    if userLen > systemLen:
        biggestLen = userLen
    else:
        biggestLen = systemLen

    return biggestLen

#Function to print in console or/and write to a file.
def print_write_data( preText, data ):
    text = preText + data
    print(text)
    if (isPrint):
        newFile.write(text + "\r\n")
#=============================================================================

if __name__ == "__main__":
	#CONFIGURATION
	#=============================================================================
	#The user can either specify where the data of the transcripts is stored, or not define
	#it, in which case the program uses the predefined location.
	try:
		dirs = sys.argv[1]
	except:
		dirs = ["dstc2_test/data","dstc2_traindev/data"]
	currentdir = os.getcwd()
	fileName = "dialog_combined_results.txt"
	directoryToSearch = '.'
	#=============================================================================

	#START HERE
	#The user has two options, either to let the transcripts be written to the console or to one big file
	#(which is also printed on the console).
	while True:
		data = input("Select one option: (a)console, (b)print in one big file, (c)speech act   ")
		if data.lower() not in ('a', 'b', 'c'):
			print("Invalid answer")
		else:
			break

	# Simple boolean that indicates whether the program has to write to a file.
	isPrint = False if data.lower() == ('a' or 'c') else True

	# Simple boolean that indicates whether the program needs to print speech act.
	isSpeechAct = True if data.lower() == 'c' else False
	
	#rename the file name for speech act
	if isSpeechAct:
		fileName = "speech_act_results.txt"

	#Open a file to allow the writing of the dialogue to a file.
	if isPrint:
		newFile = open(fileName,"w+")

	number = 1;

	#Loops through the location of the training set and test set.
	for dir in dirs:
		fulldir = os.path.join(currentdir, dir)
		subdirs = [subdir for subdir in os.listdir(fulldir)]
		#Loops through the different sets of data presetn in both the folders.
		for dataset in subdirs:
			#This if statement catches some unwanted files that might be present in the folder
			#(e.g. the .DS_Store files that Mac may computers may create)
			if os.path.isdir(os.path.join(fulldir,dataset)):
				for tcdir in os.listdir(os.path.join(fulldir, dataset)):
					#This creates the full directory of the transcript datafiles.
					tcdir = os.path.join(fulldir, dataset, tcdir)
					#This again catches potentially unwanted files.
					if os.path.isdir(tcdir):
						#Loads the json file.
						user = load_js_file_to_object(tcdir, 'label.json')
						system = load_js_file_to_object(tcdir, 'log.json')

						#Gets the biggest length of both participants in the dialogue, and the individual user and system length.
						biggestLen = calculate_biggest_dialog_length(user, system)
						userLen = len(user["turns"])
						systemLen = len(system["turns"])

						if not isSpeechAct:
							#Prints dialogue information.
							print_write_data('number: ', str(number))
							print_write_data('session id: ', user["session-id"])
							print_write_data('', user["task-information"]["goal"]["text"])

						#Prints dialogue turn utterances.
						for i in range(biggestLen):

							if isSpeechAct:
								if i+1 <= userLen:
									speechAct = user["turns"][i]["semantics"]["cam"]
									speechAct = re.sub(r'\(.*?\)', '()', speechAct)
									print_write_data(speechAct + ' ', user["turns"][i]["transcription"] )
							else:
            							if i+1 <= systemLen:
                							print_write_data('system: ', system["turns"][i]["output"]["transcript"])

            							if i+1 <= userLen:
                							print_write_data('user: ', user["turns"][i]["transcription"] )


						#End of dialog
						if not isSpeechAct:
							if isPrint:
								newFile.write("\r\n")
							else:
								print('===========================')
								input('Press enter to continue: ')
								print("")

						number = number + 1

	# Closes the file
	if isPrint:
		newFile.close()
