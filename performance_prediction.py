# -*- coding: utf-8 -*-
"""Untitled13.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wo7eIQKFUmQCyC7Q1LBDk44FY7GaHN2O
"""

import numpy as np
from random import randint
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler

# create 2 lists
train_labels = [] # will hold corresponding labels
train_samples = [] # will hold corresponding samples

"""- Final marks were checked ranging from 0 to 100.
- 2100 student marks were used.Some were below 40%, the rest were 40% and above.
- Around 95% of students had 40 or more passed.
- Around 95% of students had below 40 or more failed.
"""

# create our own data set
for i in range(50):
  # The 5% of poor performing individuals who passed.
  failing_student = randint(0, 39)
  train_samples.append(failing_student)
  train_labels.append(1) # 1 represents passing

  # The 5% of high performing individuals who failed.
  passing_student = randint(40, 100)
  train_samples.append(passing_student)
  train_labels.append(0) # 0 represents failing.

for i in range(1000):
  # The 95% of poor performing individuals who failed.
  failing_student = randint(0, 39)
  train_samples.append(failing_student)
  train_labels.append(0)

  # The 95% of high performing individuals who passed.
  passing_student = randint(40, 100)
  train_samples.append(passing_student)
  train_labels.append(1)

for i in train_samples:
  print(i)

# convert data into a numpy array that is expected by the fit
train_labels = np.array(train_labels)
train_samples = np.array(train_samples)
train_labels, train_samples = shuffle(train_labels, train_samples) # gets rid of any impossed order

scaler = MinMaxScaler(feature_range=(0,1))  # create a feature range ranging from 0 to 1
scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))

for i in scaled_train_samples:
  print(i)

"""**Simple tf.keras Sequential Model**"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy

print(tf.__version__)

# linear stack of layers
model = Sequential([
    Dense(units=16, input_shape=(1,), activation='relu'),
    Dense(units=32, activation='relu'),
    Dense(units=2, activation='softmax') # 2 because a patient experienced side effects or a patient didn't experience side effects
    # softmax - probabilities for each output class
])

model.summary()

# prepares the model for training
model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# training occurs when we call the fit function
# validation set (validation_split=0.1 - last 10%) is first taken out, then the shuffling is done
model.fit(x=scaled_train_samples, y=train_labels, validation_split=0.1, batch_size=10, epochs=30, shuffle=True, verbose=2)

# create 2 lists
test_labels = [] # will hold corresponding labels
test_samples = [] # will hold corresponding samples

# create our own data set
for i in range(10):
  # The 5% of poor performing individuals who passed.
  failing_student = randint(0, 39)
  test_samples.append(failing_student)
  test_labels.append(1) # 1 represents passing

  # The 5% of high performing individuals who failed.
  passing_student = randint(40, 100)
  test_samples.append(passing_student)
  test_labels.append(0) # 0 represents failing.

for i in range(200):
  # The 95% of poor performing individuals who failed.
  failing_student = randint(0, 39)
  test_samples.append(failing_student)
  test_labels.append(0)

  # The 95% of high performing individuals who passed.
  passing_student = randint(40, 100)
  test_samples.append(passing_student)
  test_labels.append(1)

# convert data into a numpy array that is expected by the fit function
test_labels = np.array(train_labels)
test_samples = np.array(train_samples)
test_labels, test_samples = shuffle(test_labels, test_samples) # gets rid of any impossed order

scaled_test_samples = scaler.fit_transform(test_samples.reshape(-1,1))

"""## Predict"""

predictions = model.predict(x=scaled_test_samples, batch_size=10, verbose=0)

for i in predictions:
  print(i)

# looks at the most probable prediction in the test set
rounded_predictions = np.argmax(predictions, axis=-1)

for i in rounded_predictions:
  print(i)

"""# **Confusion** **Matrix**"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt

cm = confusion_matrix(y_true=test_labels, y_pred=rounded_predictions)

# function by sklearn to plot the confusion matrix
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
  plt.imshow(cm, interpolation='nearest', cmap=cmap)
  plt.title(title)
  plt.colorbar()
  tick_marks = np.arange(len(classes))
  plt.xticks(tick_marks, classes, rotation=45)
  plt.yticks(tick_marks, classes)

  if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("Normalized confusion matrix")
  else:
    print('Confusion matrix, without normalization')
  print(cm)

  thresh = cm.max() / 2
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, cm[i, j],
              horizontalalignment="center",
              color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm_plot_labels = ['no_side_effects', 'had_side_effects']
plot_confusion_matrix(cm=cm, classes=cm_plot_labels, title='Confusion Matrix')

"""# **Save** **and** **Load** **a** **Model**"""

model.summary()

"""## **1**. **model**.**save**()"""

import os.path
if os.path.isfile('models/medical_trial_model.h5') is False:
  model.save('models/medical_trial_model.h5')

"""This save functions saves:
- The architecture of the model, allowing to re-create the model
- The weights of the model
- The training configuration (loss, optimizer)
- The state of the optimizer, allowing to resume training exactly where you left off.
"""

# How we load the model we previously saved to disk
from tensorflow.keras.models import load_model
new_model = load_model('models/medical_trial_model.h5')

new_model.summary()

new_model.get_weights()

new_model.optimizer
