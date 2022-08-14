import sys

from nltk.tokenize import sent_tokenize, word_tokenize
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from nltk.tokenize import RegexpTokenizer
from keras.models import Sequential
from nltk.corpus import stopwords
from keras.utils import np_utils
import numpy
import nltk
import argparse


def traning_model(text_length: int, data_filename: str, epochs: int = 1) -> None:
    file = open("data/{}_data.txt".format(data_filename)).read()

    def tokenize_words(input: str) -> str:
        input = input.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(input)
        # tokens = word_tokenize(input, language="russian")

        return " ".join(tokens)

    processed_inputs = tokenize_words(file)
    chars = sorted(list(set(processed_inputs)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))
    input_len = len(processed_inputs)
    vocab_len = len(chars)
    # print("Total number of characters:", input_len)
    # print("Total vocab:", vocab_len)

    seq_length = text_length
    x_data = []
    y_data = []

    for i in range(0, input_len - seq_length, 1):
        in_seq = processed_inputs[i:i + seq_length]
        out_seq = processed_inputs[i + seq_length]
        x_data.append([char_to_num[char] for char in in_seq])
        y_data.append(char_to_num[out_seq])

    n_patterns = len(x_data)
    # print("Total Patterns:", n_patterns)

    X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
    X = X / float(vocab_len)
    y = np_utils.to_categorical(y_data)

    # create model
    model = Sequential()
    model.add(LSTM(256,
                   input_shape=(X.shape[1], X.shape[2]),
                   return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256,
                   return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1],
                    activation='softmax'))

    # compile model
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam')

    # save model weights path
    filename = "weights/{}_weights.hdf5".format(data_filename)
    checkpoint = ModelCheckpoint(filename,
                                 monitor='loss',
                                 verbose=1,
                                 save_best_only=True,
                                 mode='min')
    desired_callbacks = [checkpoint]
    # model training
    model.fit(X, y, epochs=epochs,
              batch_size=50,
              callbacks=desired_callbacks)

    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')


args = list(
    map(int,
        sys.argv[1:])
)
traning_model(args[0], 'horror_stories', args[1])
# traning_model(10, 'posts', 50)
# traning_model(10, 'poems', 50)
# traning_model(10, 'jokes', 50)
