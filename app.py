# Importing necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini model and get responses
def get_gemini_response(prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content([prompt])
    return response.text

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

# Predefined prompts for each button
prompts = {
    "Feature Extraction": "give details such as brand name,product name, and other key features from the packaging material visible in the image. and give output as brand - maggi and so on for all features give every output in bullet points",
    "Expiry Date": "give expiry date/use by/best before as expiry date-(if not mentioned calculate by Manufacture date and best before months), give Manufacture date as Mfg date-, give expired -Yes/No ,give months left as months left-(calculate from expiry or best before date ) give all outputs in bullet points",
    "Counting and Brand Recognition": "give brand and product name and quantity of that product give it in an list for eg 1) maggi noodles - 2N and so on , and in the last give the total number of products in format total quantity - 5N and if there is fruit/vegetable just replace brand name by fruit name give output in bullet points",
    "Freshness Level": "give name and the freshness level of the fruit/vegetable in the image give a name to freshness level eg. banana - ripe , give percentage level of freshness eg Freshness Percentage - 40 percentsign , give edible/not edible give all output in bullet points"
}

# Initialize a variable to store the response
response = None

# Create columns to place buttons in a single line
col1, col2, col3, col4 = st.columns(4)

# Handle button clicks within each column
with col1:
    if st.button("Extract Features"):
        prompt = prompts["Feature Extraction"]
        response = get_gemini_response(prompt, image)

with col2:
    if st.button("Expiry Date"):
        prompt = prompts["Expiry Date"]
        response = get_gemini_response(prompt, image)

with col3:
    if st.button("IR Counting"):
        prompt = prompts["Counting and Brand Recognition"]
        response = get_gemini_response(prompt, image)

with col4:
    if st.button("Freshness Level"):
        prompt = prompts["Freshness Level"]
        response = get_gemini_response(prompt, image)

# Display the response below all the buttons
if response:
    st.subheader("Response")
    st.write(response)

