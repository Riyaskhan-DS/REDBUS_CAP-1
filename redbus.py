# importing libraries
import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu

# kerala bus
lists_k=[]
df_k=pd.read_csv("c:/Users/USER/Downloads/kearala_links.xls")
for i,r in df_k.iterrows():
    lists_k.append(r["route_name"])

#Andhra bus
lists_A=[]
df_A=pd.read_csv("c:/Users/USER/Downloads/Andhra_links.xls")
for i,r in df_A.iterrows():
    lists_A.append(r["route_name"])

#Telungana bus
lists_T=[]
df_T=pd.read_csv("c:/Users/USER/Downloads/telungana_links.xls")
for i,r in df_T.iterrows():
    lists_T.append(r["route_name"])

#Goa bus
lists_g=[]
df_G=pd.read_csv("c:/Users/USER/Downloads/goa_links.xls")
for i,r in df_G.iterrows():
    lists_g.append(r["route_name"])

#Rajastan bus
lists_R=[]
df_R=pd.read_csv("c:/Users/USER/Downloads/rajastan_links.xls")
for i,r in df_R.iterrows():
    lists_R.append(r["route_name"])


# South bengal bus 
lists_SB=[]
df_SB=pd.read_csv("c:/Users/USER/Downloads/southbengal_links.xls")
for i,r in df_SB.iterrows():
    lists_SB.append(r["route_name"])

# Haryana bus
lists_H=[]
df_H=pd.read_csv("c:/Users/USER/Downloads/haryana_links.xls")
for i,r in df_H.iterrows():
    lists_H.append(r["route_name"])

#Assam bus
lists_AS=[]
df_AS=pd.read_csv("c:/Users/USER/Downloads/assam_links.xls")
for i,r in df_AS.iterrows():
    lists_AS.append(r["route_name"])

#UP bus
lists_UP=[]
df_UP=pd.read_csv("c:/Users/USER/Downloads/uttrapradesh_links.xls")
for i,r in df_UP.iterrows():
    lists_UP.append(r["route_name"])

#West bengal bus
lists_WB=[]
df_WB=pd.read_csv("c:/Users/USER/Downloads/westbengal_links.xls")
for i,r in df_WB.iterrows():
    lists_WB.append(r["route_name"])


#setting up streamlit page
st.set_page_config(layout="wide")
# Define the link text
BOOK_HERE = "Book here"

web=option_menu(menu_title="🚌REDBUS.in",
                options=["Home","📍States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home":
    st.image("c:/Users/USER/Pictures/Saved Pictures/1200px-Redbus_logo.jpg",width=100)
    st.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    st.subheader(":red[Domain:]  Transportation")
    st.subheader(":red[Ojective:] ")
    st.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    st.subheader(":red[Overview:]") 
    st.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data...")
    st.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    st.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    st.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    st.subheader(":red[Skill-take:]")
    st.markdown("Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    st.subheader(":red[Developed-by:]  **S Mohammed RiyasKhan!**")                                               
    st.markdown("Come back and visit us soon !!!")

# States and Routes page setting
st.image("c:/Users/USER/Pictures/Saved Pictures/maxresdefault.jpg", width=200)
# Create a clickable link
st.markdown(f"[{BOOK_HERE}](https://www.redbus.in/)") 

if web == "📍States and Routes":
    S = st.selectbox(":red[**Lists of States**]", ["Kerala", "Andhra Pradesh", "Telungana", "Goa", "Rajastan", 
                                          "South Bengal", "Haryana", "Assam", "Uttra Pradesh", "West Bengal"])
    
    col1, col2 = st.columns(2)
    with col1:
        select_type = st.radio(":red[**Choose bus type**]", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio(":red[**Choose Price range**]", ("50-1000", "1000-2000", "2000 and above")) 
   
    # Kerala bus fare filtering
    if S == "Kerala":
        K = st.selectbox(":red[**List of routes**]", lists_k)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper%'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{K}"
                AND {bus_type_condition}
                ORDER BY price DESC 
            '''
             
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
                 ])
            return df
      
        df_result = type_and_fare(select_type, select_fare,)
        st.dataframe(df_result)

    # Adhra Pradesh bus fare filtering
    if S=="Andhra Pradesh":
        A=st.selectbox("list of routes",lists_A)

        def type_and_fare_A(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
             # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 

            # Define bus_type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{A}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_A(select_type, select_fare)
        st.dataframe(df_result)
          

    # Telungana bus fare filtering
    if S=="Telungana":
        T=st.selectbox("list of routes",lists_T)

        def type_and_fare_T(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 
 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name 
                FROM bus_routes
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{T}"
                AND {bus_type_condition}
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
                     ])
            return df

        df_result = type_and_fare_T(select_type, select_fare)
        st.dataframe(df_result)

    # Goa bus fare filtering
    if S=="Goa":
        G=st.selectbox("list of routes",lists_g)

        def type_and_fare_G(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name 
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{G}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_G(select_type, select_fare)
        st.dataframe(df_result)

    # Rajastan bus fare filtering
    if S=="Rajastan":
        R=st.selectbox("list of routes",lists_R)

        def type_and_fare_R(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{R}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_R(select_type, select_fare)
        st.dataframe(df_result)
          

    # South Bengal bus fare filtering       
    if S=="South Bengal":
        SB=st.selectbox("list of rotes",lists_SB)

        def type_and_fare_SB(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
             # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 
  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{SB}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_SB(select_type, select_fare)
        st.dataframe(df_result)
    
    # Haryana bus fare filtering
    if S=="Haryana":
        H=st.selectbox("list of rotes",lists_H)

        def type_and_fare_H(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{H}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                  "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
             ])
            return df

        df_result = type_and_fare_H(select_type, select_fare)
        st.dataframe(df_result)


    # Assam bus fare filtering
    if S=="Assam":
        AS=st.selectbox("list of rotes",lists_AS)

        def type_and_fare_AS(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  
 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{AS}"
                AND {bus_type_condition}
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                   "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_AS(select_type, select_fare)
        st.dataframe(df_result)

    # Utrra Pradesh bus fare filtering
    if S=="Uttra Pradesh":
        UP=st.selectbox("list of rotes",lists_UP)

        def type_and_fare_UP(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
             # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  
 

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{UP}"
                AND {bus_type_condition}
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                   "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_UP(select_type, select_fare)
        st.dataframe(df_result)

    # West Bengal bus fare filtering
    if S=="West Bengal":
        WB=st.selectbox("list of rotes",lists_WB)

        def type_and_fare_WB(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="redbus_data")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000   

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT ID, Bus_Name, Bus_Type, CAST(Departing_Time as CHAR), CAST(Reaching_Time AS CHAR), Duration,
                Price,Seat_Availability,Star_Ratings,route_link,route_name
                FROM bus_routes 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{WB}"
                AND {bus_type_condition} 
                ORDER BY Price DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                   "ID", "Bus_Name", "Bus_Type", "Departing_Time", "Reaching_Time", "Duration",
                "Price", "Seat_Availability", "Star_Ratings", "route_link", "route_name"
            ])
                                            
            
            return df

        df_result = type_and_fare_WB(select_type, select_fare)
        st.dataframe(df_result)



