#This python file trains a neural network on a set datafile (in the predefined directory "Train set"), and tests it on a test dataset.
#It then outputs the accuracy of the classification.

import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# The dictionary to be created with integers mapped to the speech acts. The structure is: {act:integer}
# The count increases as a new type of act is added, ensuring that each new type of act gets a unique integer.
speechactdict = {}
count=1

# Splits a single line into speech acts and utterances, where speech acts are the first word on the line.
def splitline(line, istrainset):
	actnr = ''
	text = ''
	global count #This lets us change the global variable 'count'
	words = line.split()
	text = " ".join(words[1:])
	act = words[0]
	act = act.replace('()', '')
	if act not in speechactdict.keys() and istrainset==True: #This adds the type of act into the global speechact dictionary, if it does not yet exist.
		speechactdict[act]=count
		count+=1	
	actnr = speechactdict[act]
	combined = [actnr, text]
	return combined


#Splits the lines of the specified file into speech acts and utterances, and returns a dictionary with the structure utterance:speech acts
#The second parameter indicates whether it concerns training data or test data, so that act types of the test data are not added to the dictionary of 
#speech acts. 
def splittext(file, istrainset):
    text = open(file, 'r')
    lines = text.readlines()
    linelist = []
    for line in lines:
        split = splitline(line, istrainset)
        act = split[0]
        utterance = split[1]
        linelist.append([utterance, act])
    return linelist

if __name__ == "__main__":
	#First the train data and test data is converted to lists of the utterances and acts. 
	trainlist = splittext("Train set/traindata.txt", True)
	testlist = splittext("Test set/testdata.txt", False)
	trainutterances, testutterances = [], []  # Two lists of (single element) utterances.
	trainacts, testacts = [], []  # Two lists of (single element) acts.
	for sentence in trainlist:
		trainutterances.append(sentence[0])
		trainacts.append(sentence[1])
	for sentence in testlist:
		testutterances.append(sentence[0])
		testacts.append(sentence[1])

	#Here we create a tokenizer, which is an easy way to label a unique integer per word.
	tokenizer = Tokenizer(oov_token=999)
	tokenizer.fit_on_texts(trainutterances)  # train tokenizer on speech utterances
	vocab_size = len(tokenizer.word_index)  # store vocabulary size for model input
	sequences_train = tokenizer.texts_to_sequences(trainutterances)  # convert words to vocabulary integers matrix
	sequences_test = tokenizer.texts_to_sequences(testutterances)

	#We then apply padding, so that all sentences are treated as if they contain 10 words. 
	padded_text_train = pad_sequences(sequences_train, padding='post', maxlen=10, truncating='post')
	padded_text_test = pad_sequences(sequences_test, padding='post', maxlen=10, truncating='post')

	#The few statements create the LSTM and its layers.
	model = Sequential()
	model.add(Embedding(input_dim=vocab_size + 1, mask_zero=True, output_dim=100, input_length=10))  # outputs 3D tensor
	model.add(LSTM(10, activation='relu'))
	model.add(Dense(units=len(speechactdict.keys())+1, activation='softmax')) #The last layer should have as many output nodes as there are possisble classes.
	model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

	#The to_categorical function from keras converts a list of classes into a binary class matrix. 
	#The amount of classes in the speech dictionary is used as its second argument, to intercept cases in where the training
	#set contains a certain class which the test set does not.
	trainacts_binary = to_categorical(trainacts, len(speechactdict.keys())+1)
	testacts_binary = to_categorical(testacts, len(speechactdict.keys())+1)
	model.fit(padded_text_train, trainacts_binary, epochs=10)

	#We then test model on the test data and print the score, which consists of the loss and accuracy. 	
	score = model.evaluate(padded_text_test, testacts_binary)
	print(score)
