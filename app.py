# Importing necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import re
import sqlite3
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#Function for feature extraction and db storage
def store_indb_feature(prompt,image):
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # # Generate the response from the model
    response = model.generate_content([prompt, image])
    response=response.text
    response=response.strip()
    response=response[1:-1]


    #res=response(1:-2)

    
    # Parse the response string
    # Example format: "Apple, freshness: 8, days left: 3, spoiled: no"




    # lines = text.split("\n")
    # brand = None
    # product_name = None

    # for line in lines:
    #     if "**Brand:**" in line:
    #         brand = line.split("**Brand:**")[1].strip()
    #     elif "**Product Name:**" in line:
    #         product_name = line.split("**Product Name:**")[1].strip()
    # response=brand+" "+product_name
    
    # print(response)
    
    




    # Current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Database setup (SQLite example)
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductQuantity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            brand TEXT,
            count INTEGER,
            expirydate TEXT DEFAULT NULL,
            expired TEXT DEFAULT 'NA',
            expected_lifespan_days TEXT DEFAULT 'NA'
    )
    ''')
    
    # Insert data into the table
    cursor.execute('''
    INSERT INTO ProductQuantity (brand, count, timestamp)
    VALUES (?, ?, ?)
''', (response, 1, current_time))


    # Commit and close connection
    conn.commit()
    conn.close()

    print("Data stored successfully!")
    return response





#function for Freshness level and db storage

def store_indb_freshness(prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Generate the response from the model
        response = model.generate_content([prompt, image])
        response = response.text  # Ensure no leading/trailing spaces
        
        # Parse the response string
        # Example format: "Apple, freshness: 8, days left: 3, spoiled: no"
        response=response[1:-1]
        parts = response.split(",")
        if len(parts) < 4:
            raise ValueError("Unexpected response format. Expected at least 4 parts.")
        
        name = parts[0].strip()
        freshness = parts[1].strip()
        days_left = parts[2].strip()
        spoiled = parts[3].strip()
        
        # Current date and time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Database setup (SQLite example)
        conn = sqlite3.connect('freshness_data.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FreshnessData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                name TEXT,
                freshness TEXT,
                days_left TEXT,
                spoiled TEXT
            )
        ''')
        
        # Insert data into the table
        cursor.execute('''
            INSERT INTO FreshnessData (name, freshness, days_left, spoiled, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, freshness, days_left, spoiled, current_time))
        
        # Commit and close connection
        conn.commit()
        conn.close()
        
        print("Data stored successfully!")
        res = f"""- Produce: {name}
- Freshness: {freshness}
- Days left: {days_left}
- Spoiled: {spoiled}"""
        return res
        #return res
    except Exception as e:
        print(f"An error occurred: {e}")




#Function for Expiry date and db storage

def store_indb_expiry(prompt,image):
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # Generate the response from the model
    response = model.generate_content([prompt, image])
    response=response.text
    response=response[1:-1]
    #res=response(1:-2)

    
    # Parse the response string
    # Example format: "Apple, freshness: 8, days left: 3, spoiled: no"
    parts = response.split(",")
    name = parts[0]
    useby = parts[1]
    expired1 = parts[2]
    daysleft = parts[3]
    
    # Current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Database setup (SQLite example)
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductQuantity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            brand TEXT,
            count INTEGER,
            expirydate TEXT DEFAULT NULL,
            expired TEXT DEFAULT 'NA',
            expected_lifespan_days TEXT DEFAULT 'NA'
    )
    ''')
    
    # Insert data into the table
    cursor.execute('''
    INSERT INTO ProductQuantity (brand, count, timestamp, expirydate, expired, expected_lifespan_days)
    VALUES (?, ?, ?, ?, ?, ?)
''', (name, 1, current_time, useby, expired1, daysleft))
    



    # Commit and close connection
    conn.commit()
    conn.close()

    print("Data stored successfully!")

    res = f"""- Brand/Product: {name}
- Expiry Date: {useby}
- Expired: {expired1}
- Days Left: {daysleft}
"""
        
    return res



#Function for IR counting and db storage
def store_product_quantity(prompt, image):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Generate the response from the model
        response = model.generate_content([prompt, image])
        response = response.text.strip()
        response = response[1:-1]  # Remove leading/trailing brackets
        print(f"Response: {response}")
        
        # Extract product entries in the format: "name, quantity"
        product_entries = re.findall(r'([a-zA-Z0-9\s\+\-\&\(\)]+)\s*,\s*(\d+)', response)
        
        if not product_entries:
            raise ValueError("No valid product entries found in the response.")
        
        # Current date and time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Database setup (SQLite example)
        conn = sqlite3.connect('product.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductQuantity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                brand TEXT,
                count INTEGER,
                expirydate TEXT DEFAULT NULL,
                expired TEXT DEFAULT 'NA',
                expected_lifespan_days TEXT DEFAULT 'NA'
            )
        ''')
        
        # Insert data into the table and prepare the formatted response
        res_lines = []  # To hold formatted lines for the result
        sum=0
        for name, quantity in product_entries:
            name = name.strip()
            name=name[1:]
            quantity = int(quantity.strip())
            sum+=quantity
            
            # Insert data into the database
            cursor.execute('''
                INSERT INTO ProductQuantity (brand, count, timestamp)
                VALUES (?, ?, ?)
            ''', (name, quantity, current_time))
            
            # Append formatted product info
            res_lines.append(f"- {name} : {quantity}N")
        res_lines.append(f"- Total : {sum}N")
        # Commit and close connection
        conn.commit()
        conn.close()
        
        print("Product quantities stored successfully!")
        
        # Create the formatted response
        res = "\n".join(res_lines)
        return res
    except Exception as e:
        print(f"An error occurred: {e}")



# Function to load the Gemini model and get responses
def get_gemini_response(prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content([prompt])
    response=response.text
    response=response[1:-1]
    return response


# Initialize Streamlit app
st.set_page_config(page_title="Flipkart Smart Vision System")
st.header("Flipkart Smart Vision System")

# File uploader for the image
uploaded_file = st.file_uploader("Take/Upload Image", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Display the image with custom width (e.g., 400 pixels)
    st.image(image, caption="Image", width=75)  # Adjust width as needed


#previous prompts before DB implementation
prompts1= {
    "Feature Extraction": "give details such as brand name,product name, and other key features from the packaging material visible in the image. and give output as brand - maggi and so on for all features give every output in bullet points",
    "Expiry Date": "give expiry date/use by/best before as expiry date-(if not mentioned calculate by Manufacture date and best before months), give Manufacture date as Mfg date-, give expired -Yes/No ,give months left as months left-(calculate from expiry or best before date ) give all outputs in bullet points",
    "Counting and Brand Recognition": "give brand and product name and quantity of that product give it in an list for eg 1) maggi noodles - 2N and so on , and in the last give the total number of products in format total quantity - 5N and if there is fruit/vegetable just replace brand name by fruit name give output in bullet points",
    "Freshness Level": "give name and the freshness level of the fruit/vegetable in the image give a name to freshness level eg. banana - ripe , give percentage level of freshness eg Freshness Percentage - 40 percentsign , give edible/not edible give all output in bullet points"
}  

# prompts after DB implementation
prompts = {
    "Freshness_db":"you will be given image of Fruit/vegetable you have ot give output as (name,freshness out of 10,days left before spoiled,spoiled-yes/no) you output should look like this(apple,8,10,no)",
    "ircount_db":"you will be give an image containing different products/fruits/vegetables give output as (brand_and_product_name or item_name,count of the product/item) your output should look like ((oreo,1),(maggi,1))",
    "expiry_db":"i will give you an image of product you have to give me its expirydate it can be either useby/expirydate/bestbefore give output as(brand_and_product_name,useby/expirydate/bestbefore,expired yes/no,expectedlife in days) your output should look like (maggi,dd/mm/yy,No,20) if expiry date not visible or you cant determine expiry date your output should be(maggi,NA,NA,NA)",
    "feature_db":"i will give you an image of the product give me the brand name and product name your output should look like (oreo biscuits)"
}   

# Initialize a variable to store the response
response = None

# Create columns to place buttons in a single line
col1, col2, col3, col4 = st.columns(4)

# Handle button clicks within each column
with col1:
    if st.button("Extract Features"):
        
        prompt2=prompts["feature_db"]
        response=store_indb_feature(prompt2,image)


with col2:
    if st.button("Expiry Date"):
        
        prompt2= prompts["expiry_db"]
        
        response=store_indb_expiry(prompt2,image)

with col3:
    if st.button("IR Counting"):
        
        prompt2 = prompts["ircount_db"]
        
        response=store_product_quantity(prompt2,image)


with col4:
    if st.button("Freshness Level"):
        
        prompt2=prompts["Freshness_db"]
        
        response=store_indb_freshness(prompt2,image)

# Display the response below all the buttons
if response:
    st.subheader("Response")
    st.write(response)

