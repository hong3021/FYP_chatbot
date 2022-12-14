import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()


def train():
    # read responds messages form json file
    # intents = json.loads(open('src/intents.json').read())
    # webapp path
    intents = json.loads(open('website/src/intents.json').read())


    words = []
    classes = []
    documents = []
    ignore_latters = ['?', '!', ',', '.']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)

            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_latters]
    words = sorted(set(words))
    classes = sorted(set(classes))

    # store the word into a pickle file for trianing
    # pickle.dump(words, open('src/words.pk1', 'wb'))
    # pickle.dump(classes, open('src/classes.pk1', 'wb'))

    # store the word into a pickle file for trianing (webapp)
    pickle.dump(words, open('website/src/words.pk1', 'wb'))
    pickle.dump(classes, open('website/src/classes.pk1', 'wb'))

    # translate the classes into binary training data
    training = []
    output_empty = [0] * len(classes)

    # translate the words into binary training data

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    # set up and configuration for training model
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

    # save the result into h5 file
    # model.save('src/chatbot_model.h5', hist)

    # save the result into h5 file (webapp)
    model.save('website/src/chatbot_model.h5', hist)

    # done
    print('done')
