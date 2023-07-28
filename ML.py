import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
  host=input("localhost db: "),
  user=input("user db: "),
  password=input('password db: '),
  database=input('name of db: ')
)

cursor = mydb.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print("Available tables:")
for table in tables:
  print(table[0])

table_name = input("Enter the name of the table to retrieve: ")

cursor.execute(f"SELECT * FROM {table_name}")
results = cursor.fetchall()

df = pd.DataFrame(results, columns=[i[0] for i in cursor.description])

cursor.close()
mydb.close()

X_train, X_test, y_train, y_test = train_test_split(df[['miles', 'condition']], df['price'], test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print('Root Mean Squared Error():  $%.2f'%(rmse))

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
axs[0].scatter(y_train, y_train_pred)
axs[0].set_xlabel('Actual Price')
axs[0].set_ylabel('Predicted Price')
axs[0].set_title('Actual vs. Predicted Prices (Training Data)')
xmin, xmax = axs[0].get_xlim()
ymin, ymax = axs[0].get_ylim()
slope, intercept, = np.polyfit(y_train, y_train_pred, 1)
x = np.linspace(xmin, xmax, 100)
y = slope * x + intercept
axs[0].plot(x, y, color='r')

axs[1].scatter(y_test, y_test_pred)
axs[1].set_xlabel('Actual Price')
axs[1].set_ylabel('Predicted Price')
axs[1].set_title('Actual vs. Predicted Prices (Test Data)')
xmin, xmax = axs[1].get_xlim()
ymin, ymax = axs[1].get_ylim()
slope, intercept, = np.polyfit(y_test, y_test_pred, 1)
x = np.linspace(xmin, xmax, 100)
y = slope * x + intercept
axs[1].plot(x, y, color='r')

plt.show()
