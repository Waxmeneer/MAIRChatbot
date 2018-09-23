import sys, os, shutil
import random

def writeToFiles(text, actdict, trainfile, testfile):
	currentactdict = dict()
	for key in actdict.keys():
		currentactdict[key] = 0
		
	for line in text:
		acts = getspeechacts(line)
		if currentactdict[acts] <= actdict[acts]*0.85:
			trainfile.write(line)
			currentactdict[acts]+=1
		else:
			testfile.write(line)
			currentactdict[acts]+=1 #Not needed but remains for clarity
	trainfile.close()
	testfile.close()
	
def getspeechacts(line):
	words = line.split()
	count =0
	for word in words:
		if '()' in word: 
			return word 
			#Some sentences have multiple acts, which are divided by a | in the text file. 
			#However, the dictionary stores them together, as they occurred together in the sentence.

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
	
	#The script tries to find the speech act data files in the same directory, else it takes them from the github.
	speechfile = open(os.path.join(currentdir, datadir), "r")
	trainfile = open(os.path.join(currentdir, traindir), "w+")
	testfile = open(os.path.join(currentdir, testdir), "w+")
	speech = speechfile.readlines()
	random.shuffle(speech)     #It is debatable whether it is deemed useful to shuffle before splitting and could be removed.
	actdict = createactdict(speech)
	writeToFiles(speech, actdict, trainfile, testfile)

		
	
	
	
#Unused code that would split the dataset on files, not speech acts. 	
"""
traindest = os.path.join(os.getcwd(), "Shuffled train set")
testdest = os.path.join(os.getcwd(), "Shuffled test set")
if __name__ == "__main__":
	try:
		dirs = sys.argv[1]
	except:
		dirs = ["dstc2_test/data","dstc2_traindev/data"]
	input('This script will shuffle all files in the training and test sets and move them to a new location. Proceed?')
	input('Are you sure?')
	currentdir = os.getcwd()
	pathlist = []
	for dir in dirs:
		fulldir = os.path.join(currentdir, dir)
		for dataset in os.listdir(fulldir):
			if os.path.isdir(os.path.join(fulldir,dataset)):
				for directory in os.listdir(os.path.join(fulldir,dataset)):
					path = os.path.join(fulldir,dataset,directory)
					if os.path.isdir(path):
						pathlist.append(path)
	random.shuffle(pathlist)
	length = len(pathlist)
	c=0
	while c<length:
		if c<=int(0.85*length):
			shutil.move(pathlist[c], traindest)
		else:
			shutil.move(pathlist[c], testdest)
		c+=1
	input("Press enter to exit")
 """
