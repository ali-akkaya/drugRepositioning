import numpy as np
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.layers.core import Dense
from keras.layers import LSTM, RNN, GRU
import tensorflow_addons as tfa
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Sequential
from keras.metrics import Precision, Recall

seed = 10
np.random.seed(seed)
tf.random.set_seed(seed)

initializer = tf.keras.initializers.GlorotUniform(seed=10)
initializer2 = tf.keras.initializers.GlorotUniform(seed=20)
initializer3 = tf.keras.initializers.GlorotUniform(seed=30)
initializer4 = tf.keras.initializers.GlorotUniform(seed=40)
initializer5 = tf.keras.initializers.GlorotUniform(seed=50)

model = Sequential()
model.add(keras.layers.Masking(mask_value=0, input_shape=(None, train_X.shape[2])))
#model.add(GRU(64, kernel_initializer=initializer, return_sequences = True))
#model.add(keras.layers.BatchNormalization())
#model.add(keras.layers.Dropout(0.05))
model.add(LSTM(32, kernel_initializer=initializer, return_sequences = True))
#model.add(keras.layers.BatchNormalization())
#model.add(keras.layers.Dropout(0.05))
model.add(LSTM(16, kernel_initializer=initializer2, return_sequences = True))
#model.add(keras.layers.BatchNormalization())
#model.add(keras.layers.Dropout(0.1))
model.add(LSTM(8, kernel_initializer=initializer3))
#model.add(keras.layers.BatchNormalization())
#model.add(keras.layers.Dropout(0.1))
model.add(layers.Dense(3, activation='softmax'))

opt = keras.optimizers.Adam(learning_rate=0.0001)
callbacks = [ModelCheckpoint('save_at_LSTM{epoch}.h5')]

#model.compile(optimizer=opt, loss=tfa.losses.SigmoidFocalCrossEntropy(), metrics=['accuracy', f1_m, precision_m, recall_m])

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['acc', Precision(), Recall()])

history = model.fit(train_X, encoded_train_y, epochs=200, validation_data=(validation_X, encoded_validation_y), batch_size=16, callbacks=callbacks)
#history = model.fit(train_X, encoded_train_y, epochs=200, batch_size=16, callbacks=callbacks)

#early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, verbose=0, restore_best_weights=True)
#history = model.fit(train_X, encoded_train_y, epochs=100, validation_split = 0.3, batch_size=20, callbacks=[early_stop])




#----------------------------------------
rom sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

y_pred = model.predict(test_X, batch_size=1)
y_perd_LSTM_ratio = y_pred
y_pred = np.argmax(y_pred, axis=1)
y_pred_LSTM = y_pred

accuracy = accuracy_score(integer_encoded_test_y, y_pred)
precision_score = precision_score(integer_encoded_test_y, y_pred, average='weighted')
recall_score = recall_score(integer_encoded_test_y, y_pred, average='macro')
f1_score = f1_score(integer_encoded_test_y, y_pred, average='weighted')

print("Accuracy : " + str(accuracy))
print("Precision : " + str(precision_score))
print("Recall : " + str(recall_score))
print("f1_score : " + str(f1_score))

matrix = confusion_matrix(integer_encoded_test_y, y_pred)

plt.clf()
fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(matrix)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1, 2), ticklabels=('P-0s', 'P-1s','P-2s'))
ax.yaxis.set(ticks=(0, 1, 2), ticklabels=('A-0s', 'A-1s','A-2s'))
ax.set_ylim(2.5, -0.5)
for i in range(3):
    for j in range(3):
        ax.text(j, i, matrix[i, j], ha='center', va='center', color='red')

plt.savefig('CM_LR_Predicted_class3.png')
plt.show()