import keras
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#The dictionary with integers mapped to the speech acts.
speechactdict = {'ack':1,'affirm':2,'bye':3,'confirm':4,'deny':5,'hello':6,'inform':7,'negate':8,
                 'null':9,'repeat':10,'reqalts':11,'reqmore':12,'request':13,'restart':14,'thankyou':15}

# Splits a single line into speech acts and utterances, where speech acts are the first word on the line.
def splitline(line):
    acts = []
    text = ''
    try:
        words = line.split()
        text = " ".join(words[1:])
        actbundle = words[0]
        splitacts = actbundle.split('|')
        for bracketact in splitacts:
            act = bracketact.replace('()', '')
            actnr = speechactdict[act]
            acts.append(actnr)
    except:
        print("No speech act found!")
        return ['', '']
    combined = [acts, text]
    return combined


# Splits the lines of the specified file into speech acts and utterances, and returns a dictionary with the structure utterance:speech acts
def splittext(file):
    text = open(file, 'r')
    lines = text.readlines()
    linedict = dict()
    for line in lines:
        split = splitline(line)
        acts = split[0]
        utterance = split[1]
        linedict[utterance] = acts
    return linedict

#train and test data
Traindata = splittext("Train set/traindata.txt")
Testdata = splittext("Test set/testdata.txt")

#create tokenizer
tokenizer = Tokenizer(oov_token=999)
tokenizer.fit_on_texts(Traindata.keys())   #train tokenizer on speech utterances
vocab_size = len(tokenizer.word_index)  #store vocabulary size for model input
sequences = tokenizer.texts_to_sequences(Traindata.keys()) #convert words to vocabulary integers matrix

#apply padding
padded_text = pad_sequences(sequences, padding='post', maxlen=10, truncating='post')
print(tokenizer.word_index)
print(padded_text)

#create LSTM
model = Sequential()
model.add(Embedding(input_dim=vocab_size+1, mask_zero=True, output_dim=100, input_length=10)) #outputs 3D tensor
model.add(LSTM(50, activation='relu'))
model.add(Dense(units=15, activation='softmax'))

#train model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
trainacts = Traindata.values()
model.fit(padded_text, trainacts, epochs=2)

#test model
#score = model.evaluate()
#print(score)



	
#train model compile() >  categorical cross-entropy as loss function and accuracy as evaluation measure.
