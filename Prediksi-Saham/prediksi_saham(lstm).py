# -*- coding: utf-8 -*-
"""Prediksi_Saham(LSTM).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I0dZfqU-dH3Me2-xGRvgorVp02V6j0e2

LINK TUTORIAL DI SINI INI :
https://www.youtube.com/watch?v=QIUxPv5PJOY

[link text](https://www.youtube.com/watch?v=QIUxPv5PJOY)
"""

#from google.colab import drive
#drive.mount('/content/gdrive')

#import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the Stock
df = web.DataReader('ADRO.JK', data_source='yahoo', start='2008-06-17', end='2021-04-30')
#show the data
df

#Get the number of rows and columns in the data set
df.shape

#visualize the closing price history
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
#plt.plot(df['Volume'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price (Rp)', fontsize=18)
plt.show()

#VOLUME
plt.figure(figsize=(16,8))
plt.title('Close Volume History')
plt.plot(df['Volume'])
#plt.plot(df['Volume'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Volume (Rp)', fontsize=18)
plt.show()

#Create a new dataframe with only Close column
data = df.filter(['Close'])
#Convert the dataframe to a numpy array
dataset = data.values
#Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * .8)

training_data_len

#scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

#Creat the training dataset
#Creat the scaled training dataset
train_data = scaled_data[0:training_data_len , :]

#split the data into x_train and y_train data sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<= 61:
    print(x_train)
    print(y_train)
    print()

#convert the x_train and y_train to numpy array
x_train, y_train = np.array(x_train), np.array(y_train)

#Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

#Build the LSTM
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#Compile the model
model.compile(optimizer = 'adam', loss = 'mean_squared_error')

#Train the model
model.fit(x_train, y_train, batch_size=15 , epochs=50)

#Creat the testing data set
#Create a new array containing scaled values from index 1543 to 2003
test_data = scaled_data[training_data_len - 60: , :]
#Creat the data sets x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

#Covert the data to a numpy array
x_test = np.array(x_test)
#Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
#Get the model prediction price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#Get the root mean squared error (RMSE)
rmse = np.sqrt(np.mean(predictions - y_test)**2 )
rmse

#Plot the data
train = data[: training_data_len]
valid = data[training_data_len :]
valid['Predictions'] = predictions
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('ADRO')
plt.xlabel('Data', fontsize=18)
plt.ylabel('Close Price (Rp)', fontsize=18)
#plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend([ 'Actual', 'Predictions'], loc='lower right' ) #'Train',
plt.show()

#Show the valid predicted prices
valid

#Get the quote
apple_quote = web.DataReader('ADRO.JK', data_source='yahoo', start='2012-01-01', end='2021-04-30')
#Creat a new dataframe
new_df = apple_quote.filter(['Close'])
#Get the last 60 days closing price values and convert the dataframe to the array
last_60_days = new_df[-60:].values
#Scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#Creat an empty list
X_test = []
#Append the past 60 days
X_test.append(last_60_days_scaled)
#convert the X_test data set to  a numpy array
X_test = np.array(X_test)
#reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#get the predicted scaled price
pred_price = model.predict(X_test)
#Undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

#membandingkan hasil prediksi
apple_quote2 = web.DataReader('ADRO.JK', data_source='yahoo', start='2021-04-30', end='2021-04-30')
print(apple_quote2['Close'])
print('Prediction =')
print(pred_price)

