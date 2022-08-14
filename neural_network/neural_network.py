from nltk.tokenize import sent_tokenize, word_tokenize
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from nltk.tokenize import RegexpTokenizer
from keras.models import Sequential
from nltk.corpus import stopwords
from keras.utils import np_utils
import numpy
import nltk

nltk.download('stopwords')
nltk.download('punkt')


class NNTGModel:
    def __init__(self, data_file_name: str, text_length: int = 200) -> None:
        self.data_file_name = data_file_name
        self.text_length = text_length
        self.path = '' if __name__ == '__main__' else 'neural_network/'

    def tokenizer(self, input: str) -> str:
        input = input.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(input)
        # tokens = word_tokenize(input, language="russian")
        print(tokens)
        return " ".join(tokens)

    def get_model(self):
        data_file_path = "{}data/{}_data.txt" \
            .format(self.path, self.data_file_name)
        data_file = open(data_file_path).read()

        processed_inputs = self.tokenizer(data_file)
        chars = sorted(list(set(processed_inputs)))
        char_to_num = dict((c, i) for i, c in enumerate(chars))
        input_len = len(processed_inputs)
        vocab_len = len(chars)

        seq_length = self.text_length
        x_data = list()
        y_data = list()

        for i in range(0, input_len - seq_length, 1):
            in_seq = processed_inputs[i:i + seq_length]
            out_seq = processed_inputs[i + seq_length]
            x_data.append([char_to_num[char] for char in in_seq])
            y_data.append(char_to_num[out_seq])

        n_patterns = len(x_data)
        x = numpy.reshape(x_data, (n_patterns, seq_length, 1))
        x = x / float(vocab_len)
        y = np_utils.to_categorical(y_data)

        # create model
        model = Sequential()
        model.add(LSTM(256,
                       input_shape=(x.shape[1], x.shape[2]),
                       return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(256,
                       return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(128))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1],
                        activation='softmax'))
        return model, x_data, chars

    def generator(self) -> str:
        # compile model
        model, x_data, chars = self.get_model()
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam')

        model_file_path = "{}weights/{}_weights.hdf5" \
            .format(self.path, self.data_file_name)
        model.load_weights(model_file_path)
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        num_to_char = dict((i, c) for i, c in enumerate(chars))
        start = numpy.random.randint(0, len(x_data) - 1)
        pattern = x_data[start]

        text = ''.join([num_to_char[value] for value in pattern])

        return text + '...'

    def traning(self) -> None:
        pass

#
# model = NNTGModel('horror_stories', 200)
# print(model.generator())
