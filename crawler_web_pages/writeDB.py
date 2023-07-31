
#Json檔寫進MySQL資料庫
import json
import mysql.connector

# Opening JSON file
filename = r'/Users/chiachenwu/crawler_adoptWeb/crawler_web_pages/pet_data.json'
f = open(filename, encoding="utf-8")

# returns JSON object as a dictionary
data = json.load(f)

# Create a list to hold the attractions data
Attractions = []

# Process each item in the results list and append it to Attractions
for item in data:
    # Extract the attributes from the '名字' field
    parts = item.get('名字', '').split(',')
    name = parts[0].strip()
    species = parts[1].strip().replace('品種：', '') if len(parts) > 1 else ''
    type = parts[2].strip().replace('種類：', '') if len(parts) > 2 else ''
    gender = parts[3].strip().replace('性別：', '') if len(parts) > 3 else ''
    size = parts[4].strip().replace('體型：', '') if len(parts) > 4 else ''
    coat_color = parts[5].strip().replace('毛色：', '') if len(parts) > 5 else ''
    age = parts[6].strip().replace('年紀：', '') if len(parts) > 6 else ''
    sterilization = parts[7].strip().replace('結紮：', '') if len(parts) > 7 else ''
    address = parts[8].strip().replace('所在地：', '') if len(parts) > 8 else ''

    Attraction = {
        'name': name,
        'location': address,
        'url': item.get('網址', ''),
        'image_url': item.get('照片', ''),
        'species': species,
        'type': type,
        'gender': gender,
        'size': size,
        'coat_color': coat_color,
        'age': age,
        'sterilization': sterilization,
    }

    Attractions.append(Attraction)

# Close the file
f.close()

# Create a database connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tn00817411',
    database='myadoption'
)

# Check if the connection is successful
if mydb.is_connected():
    db_Info = mydb.get_server_info()
    print("Connected to MySQL Server version", db_Info)
    cursor = mydb.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    print("You're connected to database:", record)
else:
    print("Error while connecting to MySQL")

# Drop the table if it exists
query = "DROP TABLE IF EXISTS catsData"
cursor.execute(query)
mydb.commit()

# Create a Table
query = """
CREATE TABLE catsData (
    id bigint PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    species varchar(255),
    type varchar(255),
    gender varchar(255),
    size varchar(255),
    coat_color varchar(255),
    age varchar(255),
    sterilization varchar(255),
    address varchar(255),
    url varchar(255) NOT NULL,
    image_url varchar(255) NOT NULL,
    location varchar(255)  -- Add the 'location' column
)
"""
cursor.execute(query)
mydb.commit()

# Import the data into the table
query = """
INSERT INTO catsData (
    name,species, type, gender, size, coat_color, age, sterilization, address, url, image_url, location
) VALUES (
    %(name)s, %(species)s, %(type)s, %(gender)s, %(size)s, %(coat_color)s, %(age)s, %(sterilization)s, %(location)s, %(url)s, %(image_url)s, %(location)s
)
"""

for attraction in Attractions:
    cursor.execute(query, attraction)  # Use 'attraction' dictionary directly as values

mydb.commit()
cursor.close()
mydb.close()