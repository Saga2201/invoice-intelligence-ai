import streamlit as st
import requests
from csv_services.csv_generator import json_to_csv

# Streamlit app title
st.title('Intelligent Doc Processor')

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=['jpeg', 'pdf', 'png'])

# Secret key input field
secret_key = st.text_input("Enter your secret key", type="password")


# Function to call the backend API
def call_backend_api(uploaded_file, secret_key):
    # Prepare the files and data to be sent in the API request
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    data = {'secret_key': secret_key}

    # Sending a POST request to your API
    response = requests.post('http://127.0.0.1:5000/upload', files=files, data=data)
    return response


# Button to submit the information and call the API
if st.button('Submit'):
    if uploaded_file is not None and secret_key == "Think@2024":
        # Call the API with the uploaded file and secret key
        response = call_backend_api(uploaded_file, secret_key)

        # Check the response from your API
        if response.status_code == 200:
            st.success("File and Secret Key Submitted Successfully!")
            # Add download button for the CSV file
            with open("api_response.csv", "rb") as file:
                st.download_button(
                    label="Download CSV",
                    data=file,
                    file_name="api_response.csv",
                    mime="text/csv"
                )
            # Display the API response
            api_response = response.json()  # Convert response to JSON
            st.write("API Response:")
            json_to_csv(json_data=api_response, csv_filename="api_response.csv")
            st.json(api_response)  # Nicely display the JSON response
        else:
            st.error("Failed to submit. Please try again.")
            try:
                error_response = response.json()
                st.write("Error Details:")
                st.json(error_response)
            except Exception as e:
                st.write("An error occurred while parsing the error response.")
    else:
        st.error("Please upload a file and enter a secret key.")
