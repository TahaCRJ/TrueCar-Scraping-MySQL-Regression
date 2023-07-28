This project, called TrueCar-Scraping-MySQL-Regression, utilizes Selenium for web scraping to extract data on cars from TrueCar. The data is then stored in MySQL and used to predict car prices through regression analysis. This project is helpful for car dealerships, buyers, and sellers alike.

## Data Scraping
To extract the desired data on a car model provided by the user, I use Selenium. The data I gather includes mileage, price, and the car's condition (including accidents). I collect data from up to 5 pages of the website, if available.

## MySQL
The data I gather is transferred to a database and stored in a table with the name of the car model.

## Model Training
Once the data is stored in the database, it can be read and preprocessed for use in training a regression model. I train a regression model on the preprocessed data.

### Overview
For an overview of the project, please refer to the project's documentation.(project_overview.ipynb)
