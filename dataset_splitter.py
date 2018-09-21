import sys, os, shutil
import random

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
            
