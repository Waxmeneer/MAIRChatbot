import sys, os, shutil
import random

#This python script splits speech act data into a training set and test set, so that the training set contains 85% of the data
#and the test set 15%. The proportions of speech acts are preserved.

#This function writes the lines of a list of text to a training set and test set. The proportions
#of speech acts are weighed, so that both files contain more or less the same amount relatively.
def writeToFiles(text, actdict, trainfile, testfile):
	currentactdict = dict() #This dictionary keeps track of the amount of speech acts that have been counted so far.
	for key in actdict.keys():
		currentactdict[key] = 0	
	for line in text:
		acts = getspeechacts(line)
		if currentactdict[acts] <= actdict[acts]*0.85: #The 0.85 makes that the train set contains 85% of the data and the test set 15%
			trainfile.write(line)
			currentactdict[acts]+=1
		else:
			testfile.write(line)
			currentactdict[acts]+=1 #Not needed but remains for clarity
	trainfile.close()
	testfile.close()

#This method returns the speech act or acts for a given line. Note that multiple speech acts consist of one word
#in the data set, where the acts are separated by a |. Consequence is that they will not be put in the dictionary as
#separate values.
def getspeechacts(line):
	words = line.split()
	count =0
	for word in words:
		if '()' in word: 
			return word 

def createactdict(text):
	actdict = dict()
	for line in text:
		acts = getspeechacts(line)
		if acts in actdict:
			actdict[acts]+=1
		else:
			actdict[acts]=1
	return actdict
	

if __name__ == "__main__":
	#The user can specify the paths of the speech acts file, training data folder and test data folder. If they aren't 
	#specified as extra arguments, the script takes the default ones.
	try:
		datadir= sys.argv[1]
		traindir = sys.argv[2]
		testdir = sys.argv[3]
	except:
		print("Default directories selected")
		datadir = "speech_act_results.txt"
		traindir = "Train set/traindata.txt"
		testdir = "Test set/testdata.txt"
	currentdir = os.getcwd()
	
	#These try and excepts give the user feedback on what went wrong.
	try:
		speechfile = open(os.path.join(currentdir, datadir), "r")
	except:
		print("Speech act file not present, default is: speech_act_results.txt")
	try:
		trainfile = open(os.path.join(currentdir, traindir), "w+")
	except:
		print("Training folder not present, default is: Train set")
	try:
		testfile = open(os.path.join(currentdir, testdir), "w+")
	except:
		print("Test folder not present, default is: Test set")
	speech = speechfile.readlines()
	random.shuffle(speech)     #It is debatable whether it is deemed useful to shuffle before splitting and could be removed.
	actdict = createactdict(speech)
	writeToFiles(speech, actdict, trainfile, testfile)