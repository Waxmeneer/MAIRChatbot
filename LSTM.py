import keras
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM
from keras.preprocessing.text import Tokenizer
import numpy
from keras.preprocessing.sequence import pad_sequences

#Y_train (TODO: convert strings to ints)
speech_acts = [0, 1, 2]
#X_train
speech_utterances= ['hallo dit is',
                     'ook een regel',
                     'hallo en nog een regel hallo hallo hallo i j k l m']

#create tokenizer
tokenizer = Tokenizer(oov_token=999)
tokenizer.fit_on_texts(speech_utterances)   #train tokenizer on speech utterances
vocab_size = len(tokenizer.word_index)  #store vocabulary size for model input
sequences = tokenizer.texts_to_sequences(speech_utterances) #convert words to vocabulary integers matrix

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
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics='accuracy')

model.fit(padded_text, speech_acts, epochs=2)

#test model
score = model.evaluate()
print(score)
#train model compile() >  categorical cross-entropy as loss function and accuracy as evaluation measure.
