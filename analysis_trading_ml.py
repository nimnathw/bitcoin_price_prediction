# -*- coding: utf-8 -*-
"""analysis_trading_ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1exZQwZvPofP4SLF4-r93am29lMQmFVTa
"""

import sys
import os
os.chdir('/content/drive/MyDrive/Colab Notebooks')
sys.path.append('/content/drive/MyDrive/Colab Notebooks')
!pwd

from google.colab import files
#uploaded = files.upload()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the cleaned data into a DataFrame
df = pd.read_csv("data.csv")
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] > '2022-01-01']
df.set_index('date', inplace=True)


# view data
df.describe()

from sklearn.model_selection import train_test_split, TimeSeriesSplit

# Get the dependent variable 'prices'
y = df['prices']

# Get the independent variables
X = df.drop(columns=['prices']) 

# Define the number of splits
n_splits = 3

# Create the TimeSeriesSplit object
tscv = TimeSeriesSplit(n_splits=n_splits)

# Split the data into training and test sets
for train_index, test_index in tscv.split(df):
    X_train, X_test = df.iloc[train_index, :], df.iloc[test_index, :]
    y_train, y_test = df.iloc[train_index, -1], df.iloc[test_index, -1]

# Split the data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Define the LSTM model
model = Sequential()
# Add first LSTM layer with 50 units and input shape defined as the number of features in the X_train dataset
model.add(LSTM(units=50, input_shape=(X_train.shape[1],1)))
# Add fully connected Dense layer with one unit to produce the output
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Define early stopping and checkpoint callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, mode='min')
checkpoint = ModelCheckpoint("best_model.h5", save_best_only=True, monitor='val_loss', mode='min')

# Train the model on the training data
history = model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32, callbacks=[early_stopping, checkpoint])

from keras.models import load_model

# Load the best model
model = load_model('best_model.h5')

# Evaluate the model on the test set
test_loss = model.evaluate(X_test, y_test)
print('Test Loss:', test_loss)

import matplotlib.pyplot as plt

# Plot the training, validation, and test loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.plot(test_loss)
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation', 'Test'], loc='upper right')
plt.show()

from sklearn.metrics import mean_absolute_error, mean_squared_error


# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the MAE
mae = mean_absolute_error(y_test, y_pred)
print('Mean Absolute Error:', mae)

# Calculate variance of transformed y_test
y_test_transformed_var = np.var(y_test)
print('Variance of y_test_transformed:', y_test_transformed_var)


# Calculate the RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"rmse: {rmse}")

!pip install pmdarima

from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import pandas as pd
from pmdarima.arima import auto_arima

df = pd.read_csv("data.csv")
X = df.drop("prices", axis=1) # drop prices column to create X
y = df["prices"] # select prices column to create y


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



#stepwise_model = auto_arima(y_train, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)

#print(stepwise_model.order)

# Fit an ARIMA model to the time series data
model = ARIMA(y_train, order=(p, d, q))
model_fit = model.fit()

