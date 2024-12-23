import streamlit as st
import pandas as pd
import mysql.connector

# Setting the title of the PMR App in web browser
st.set_page_config(page_title='Bolts Goal or GA Tagging App')


connection = mysql.connector.connect(
    host="bostonbolts.cviw8wc8czxn.us-east-2.rds.amazonaws.com",
    user="bostonbolts",
    password="Naveen2!",
    database="bostonbolts_db",
    port=3306
)

if connection.is_connected():
    print("Successfully connected to the database")

try:
    # Fetch all rows from the table
    query = "SELECT * FROM actions_report;"
    df = pd.read_sql(query, connection)
    
    cursor = connection.cursor()
    
finally:
    connection.close()

#st.write(df)

df.columns = df.columns.str.replace('_', ' ', regex=True)
df = df[df['Team'].str.contains('MLS Next', case=False, na=False)]

actions_wanted = ['Goal', 'Goal Against']

df = df[df['Action'].isin(actions_wanted)]


df.rename(columns={'Name': 'Player',
                                  'Video Link': 'Link'}, inplace=True)

df["Video Link"] = df["Link"].apply(lambda url: f'<a href="{url}" target="_blank">Link</a>')
df.drop(columns = {'Match Date', 'Period', 'Link'}, inplace=True)

df = df.sort_values('Team', ascending=True).reset_index(drop=True)

st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: 20px; /* Adjust the font size to make it smaller */
        font-weight: bold;
        margin-bottom: 0px; /* Optional: Add spacing below the title */
    }
    </style>
    <div class="centered-title">Table of Goals and Goals Against</div>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .scrollable-table {
        max-height: 400px; /* Adjust the height to make it easier to view */
        max-width: 100%; /* Use 100% to ensure it adjusts to the container width */
        overflow: auto; /* Enable both vertical and horizontal scrolling */
        display: block;
        border: 1px solid #ddd; /* Optional: Add a border for better visualization */
    }
    .scrollable-table table {
        width: 100%; /* Make the table fill the div width */
        border-collapse: collapse; /* Ensure table borders look neat */
    }
    .scrollable-table th, .scrollable-table td {
        padding: 8px;
        text-align: left; /* Adjust alignment as needed */
        border: 1px solid #ddd; /* Optional: Add borders to cells */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="scrollable-table">
    {df.to_html(escape=False, index=False)}
    </div>
""", unsafe_allow_html=True)
