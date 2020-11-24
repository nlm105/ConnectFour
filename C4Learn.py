import logging
import os

# | 0 DEBUG | 1 INFO | 2 WARNING | 3 ERROR |
# This is what it will stop. So 3 will stop all messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.WARNING)  # sets log for other tensorflow things outside std out

import pickle as p
import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
from keras import models
from keras import layers
from sklearn.model_selection import train_test_split

with open("X.pkl", "rb") as f:
    data = p.load(f)
    f.close()

# with open("O.pkl", "rb") as f:
#     temp = p.load(f)
#     data = data + temp
#     f.close()

# Holy shit this all worked
boards = [arr[0] for arr in data]
boards = np.array([np.array(xi) for xi in boards])

labels = np.array([i[1] for i in data])

X_train, X_test, y_train, y_test = train_test_split(boards, labels, test_size=0.33, random_state=42)

y_test = y_test/10
y_train = y_train/10
# print(np.shape(data))
# print((X_train, "\n", X_test))

network = models.Sequential()

network.add(layers.Dense(1000, activation="relu"))
network.add(layers.Dense(500, activation="relu"))
network.add(layers.Dense(1))

network.compile(loss="mse", metrics="mse")
network.fit(X_train, y_train, epochs=5, batch_size=15)
network.summary()

# predicts = network.predict()

network.evaluate(X_train, y_train)
network.evaluate(X_test, y_test)

print(X_train[0])
print(type(X_train[0]))

for i in range(len(X_train)):
    predict = network.predict(np.array([X_train[i]]))
    print(predict, ":", y_train[i])

print(network.predict(np.array([X_train[0]])))
