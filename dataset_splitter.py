import sys, os, shutil
import random

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
	speechfile = file.open(os.path.join(currentdir, datadir), "r")
	trainfile = file.open(os.path.join(currentdir, traindir), "w")
	testfile = file.open(os.path.join(currentdir, testdir), "w")
	speechactdict = dict()
	totalacts=0
	c=0
	random.shuffle(speechfile)
	while c<len(speechfile):
		line = speechfile[c]
		actsamt = countspeechacts(line)
		totalacts+=actsamt
		c+=1
	currentactsamt=0
	for line in speechfile:
		currentactsamt+= countspeechacts(line)
		if currenactsamt<=0.85*totalacts:
			trainfile.write(line + "\n")
		else:
			testfile.write(line + "\n")	
	trainfile.close()
	testfile.close()

	
def countspeechacts(line):
	split = line.split()
	count =0
	for word in split:
		for "()" in word:
			count+=1
	return count

	
	
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
