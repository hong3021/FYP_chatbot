import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
from keras.models import load_model


lemmatizer = WordNetLemmatizer()

# for testing
# intents = json.loads(open("src/intents.json").read())
# words = pickle.load(open('src/words.pk1', 'rb'))
# classes = pickle.load(open('src/classes.pk1', 'rb'))
# model = load_model('src/chatbot_model.h5')

#for website
intents = json.loads(open("website/src/intents.json").read())
words = pickle.load(open('website/src/words.pk1', 'rb'))
classes = pickle.load(open('website/src/classes.pk1', 'rb'))
model = load_model('website/src/chatbot_model.h5')


def claen_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

    return sentence_words


def bag_of_words(sentece):
    sentece_words = claen_up_sentence(sentece)
    bag = [0] * len(words)
    for w in sentece_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.30
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):

    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    except IndexError:
        # create tag for low probebility
        return "I dont really understad that"


def response_message(user_input):
    ints = predict_class(user_input.lower())
    res = get_response(ints, intents)
    return res

# print('Bot is RUNNING')
#
# while True:
#     massage = input("")
#     ints = predict_class(massage.lower())
#     res = get_response(ints, intents)
#     print(ints)
#     print(res)

