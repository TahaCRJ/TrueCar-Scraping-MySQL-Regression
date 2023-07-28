from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import mysql.connector
import re 

def sanitize_table_name(name):
    sanitized_name = re.sub('[^a-zA-Z0-9_]', '', name)
    return sanitized_name

def condition_binarize(condition):
    if "No accidents" in condition:
        return 0
    else:
        return 1

def price_int(price):
    return int(str.join("",price.strip('$').split(',')))

def mile_int(mile):
    return int(str.join("",mile.split(" ")[0].split(",")))

cnx = mysql.connector.connect(user=input("database user: "), password=input("database password: "),
                              host=input("database host: "),
                              database=input("database name: "))

car_name = input("Enter a car name(for example bmw x5): ")
sanitized_car_name = sanitize_table_name(car_name)


driver = webdriver.Chrome()
driver.get('https://www.truecar.com/')

search_bar = driver.find_element(By.ID, 'homePageSearchBarLgOmnisearchSearchField')
search_bar.clear()
search_bar.send_keys(car_name[:5])
time.sleep(1)
search_bar.send_keys(car_name[5:])
time.sleep(1)
search_bar.send_keys(Keys.ENTER)

time.sleep(5)
driver.implicitly_wait(3)



car = {"miles":[],"price":[],"condition":[]}
for page in range(5):
    prices = driver.find_elements(By.CSS_SELECTOR, '[data-test="vehicleCardPricingBlockPrice"]')
    miles = driver.find_elements(By.CSS_SELECTOR,'[data-test="vehicleMileage"]')
    car_conditions = driver.find_elements(By.CSS_SELECTOR,'[data-test="vehicleCardCondition"]')

    for price in prices:
        p = price.text
        try:
            car["price"].append(p.split('\n')[-1])
        except:
            car['price'].append(p)


    
    for mile in miles:
        car["miles"].append(mile.text)

    for condition in car_conditions:
        car["condition"].append(condition.text)


    try:
        next_page = driver.find_element(By.CSS_SELECTOR,'[data-test="Pagination-directional-next"]')
        next_page.click()
        time.sleep(5)
        driver.implicitly_wait(3)
    except:
           break



car_df = pd.DataFrame(car) 



car_df['condition'] = car_df['condition'].apply(condition_binarize)
car_df['price'] = car_df['price'].apply(price_int)
car_df['miles'] = car_df['miles'].apply(mile_int)

cursor = cnx.cursor()

create_table = f"""
    CREATE TABLE IF NOT EXISTS {sanitized_car_name} (
        miles INT,
        price INT,
        `condition` INT
    )
"""
cursor.execute(create_table)

for i, row in car_df.iterrows():
    sql = f"INSERT INTO {sanitized_car_name} (miles, price, `condition`) VALUES (%s, %s, %s)"
    values = (int(row['miles']), int(row['price']), int(row['condition']))
    cursor.execute(sql, values)
    
cnx.commit()
cursor.close()
cnx.close()
driver.quit()