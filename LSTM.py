import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# The dictionary with integers mapped to the speech acts.
speechactdict = {'ack': 1, 'affirm': 2, 'bye': 3, 'confirm': 4, 'deny': 5, 'hello': 6, 'inform': 7, 'negate': 8,
                 'null': 9, 'repeat': 10, 'reqalts': 11, 'reqmore': 12, 'request': 13, 'restart': 14, 'thankyou': 15}

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
    linelist = []
    for line in lines:
        split = splitline(line)
        acts = split[0]
        utterance = split[1]
        for act in acts:
            linelist.append([utterance, act])
    return linelist


# train and test data
trainlist = splittext("Train set/traindata.txt")
trainutterances, testutterances = [], []  # Two lists of (single element) utterances.
trainacts, testacts = [], []  # Two lists of (single element) acts.
for sentence in trainlist:
    trainutterances.append(sentence[0])
    trainacts.append(sentence[1])
testlist = splittext("Test set/testdata.txt")
for sentence in testlist:
    testutterances.append(sentence[0])
    testacts.append(sentence[1])

# create tokenizer
tokenizer = Tokenizer(oov_token=999)
tokenizer.fit_on_texts(trainutterances)  # train tokenizer on speech utterances
vocab_size = len(tokenizer.word_index)  # store vocabulary size for model input
sequences_train = tokenizer.texts_to_sequences(trainutterances)  # convert words to vocabulary integers matrix
sequences_test = tokenizer.texts_to_sequences(testutterances)

# apply padding
padded_text_train = pad_sequences(sequences_train, padding='post', maxlen=10, truncating='post')
padded_text_test = pad_sequences(sequences_test, padding='post', maxlen=10, truncating='post')
print(tokenizer.word_index)

# create LSTM
model = Sequential()
model.add(Embedding(input_dim=vocab_size + 1, mask_zero=True, output_dim=100, input_length=10))  # outputs 3D tensor
model.add(LSTM(10, activation='relu'))
#model.add(Dropout(0.25))
model.add(Dense(units=16, activation='softmax'))

# train model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
trainacts_binary = to_categorical(trainacts)
testacts_binary = to_categorical(testacts)
model.fit(padded_text_train, trainacts_binary, epochs=10)

# test model
score = model.evaluate(padded_text_test, testacts_binary)
print(score)
