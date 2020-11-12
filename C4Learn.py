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


# Holy shit this all worked
boards = [arr[0] for arr in data]
boards = np.array([np.array(xi) for xi in boards])

labels = np.array([i[1] for i in data])

X_train, X_test, y_train, y_test = train_test_split(boards, labels, test_size=0.33, random_state=42)

print(np.shape(data))
print((X_train, "\n", X_test))
