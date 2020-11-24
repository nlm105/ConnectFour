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

#Trying to turn the 2D array into a 3D array
bds = []

for i in boards:
    temp = [[] for _ in range(8)]
    for j in range(len(temp)):
        temp[j] = i[(j*8):(j*8+8)]
    bds.append(temp)

labels = np.array([i[1] for i in data])

lbls = []
for i in range(len(labels)):
    temp = [[labels[i]]]
    lbls.append(temp)

X_train, X_test, y_train, y_test = train_test_split(bds, lbls, test_size=0.33, random_state=42)

X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

y_test = y_test/10
y_train = y_train/10

# print(np.shape(data))
# print((X_train, "\n", X_test))

opt = keras.optimizers.Adam(learning_rate = 0.01)
network = models.Sequential()

# network.add(layers.Conv1D(16, 1, activation='relu'))
# network.add(layers.Conv1D(32, 1, activation='relu'))
# network.add(layers.Conv1D(32, 3, activation='relu'))
# network.add(layers.Conv1D(64, 3, activation='relu'))
# network.add(layers.Conv1D(128, 3, activation='relu'))
# # network.add(layers.Dense(64, activation='relu'))
# network.add(layers.Dense(1, activation='sigmoid'))
#
# network.compile(loss="mse", metrics="mse")

network.add(layers.Conv2D(8, (4, 4), activation='relu', input_shape=(8,8,1)))
#network.add(layers.MaxPooling2D(4,4))
network.add(layers.Conv2D(16, (2, 2), activation='relu'))
#network.add(layers.MaxPooling2D(2,2))
network.add(layers.Conv2D(16, (2, 2), activation='relu'))
network.add(layers.Flatten())
network.add(layers.Dense(16))
network.add(layers.Dense(1))


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# create a model using the training data
# note the reshaping line (11) - modify if you change the amount of training
#   observations
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
network.compile(optimizer=opt, loss='mse', metrics='mse')
X_train = X_train.reshape((int(X_train.size/64), 8, 8, 1))
network.fit(X_train, y_train, epochs=5, batch_size=1, verbose=0)
X_test = X_test.reshape((int(X_test.size/64)), 8, 8, 1)

network.summary()

# predicts = network.predict()

network.evaluate(X_train, y_train)
network.evaluate(X_test, y_test)

# print(X_train[0])
# print(type(X_train[0]))

for i in range(len(X_train)):
    predict = network.predict(np.array([X_train[i]]))
    print(predict, ":", y_train[i])

# print(network.predict(np.array([X_train[0]])))
