from dotenv import load_dotenv
import sqlite3, os
import streamlit as st
import google.generativeai as genai


# load all env variables
load_dotenv()

# Configure google api key
genai.configure(api_key=os.getenv("GEMINI_APY_KEY"))

# database name
db_name = "Database.db"

# call Gemini Pro model
def get_gemini_response(prompt, question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt, question])
    return response.text

# Fetch query from SQL database
def retrieve_from_sql(query):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        results = None
    # Commit changes & close connection
    connection.commit()
    connection.close()
    
    return results

# Main prompt for model
prompt = """
    You're an expert in translating plain English questions into SQL queries. You'll be working with an sql  database which includes a table named PLAYER with the following columns: id, name, position, nationality, and age. \n\nFor example questions could be: \nExample 1: 'Could you list all player names in the database?' The associated SQL query for this question would be: SELECT name FROM Players \nExample 2: 'What are the names and nationalities of players aged 30 or younger?' In response, your SQL query would be: SELECT name, nationality FROM Players WHERE age <= 30. \nYour responses should provide the requested information without including ``` in the beginning or the sql keyword at the end.
    """


# Create Basic streamlit web page
st.title("SQL Retriever Using Gemini Pro")
st.subheader("Enter your question below:")
user_input = st.text_input(label="Question")
button_clicked = st.button("Submit")

if button_clicked:
    query = get_gemini_response(prompt=prompt, question=user_input)
    results = retrieve_from_sql(query)
    st.subheader("Query Results:")
    st.table(results)