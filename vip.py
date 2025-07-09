import requests
from PIL import Image
import streamlit as st
from streamlit_lottie import st_lottie
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from collections import deque
import hashlib
from decimal import Decimal


st.set_page_config(page_title="QUEUE OPTIMIZER", page_icon=":tada:", layout="wide")

# Define admin credentials (in practice, use a more secure method of storing credentials)
ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("vip@03".encode()).hexdigest()
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    hashed_password = hash_password(password)
    return ADMIN_CREDENTIALS.get(username) == hashed_password

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def login_page():
    st.markdown("<h1 style='text-align: center; font-style: italic;'>Queue Optimizer For Vehicle Parking System</h1>", unsafe_allow_html=True)
    st.title("Admin Login :wave:")

    # Load the Lottie animation for the login page
    lottie_login = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

    st.markdown("""
    <style>
    .login-form {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .login-form input {
        width: 100%;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .login-form button {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 19px;
    }
    .login-form button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display the Lottie animation on the login page
    st_lottie(lottie_login, height=300, key="login_animation")

    # Create a form for login
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.experimental_rerun()  # Reload the app
            else:
                st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.pop('logged_in', None)  # Clear the session state
    st.success("Logged out successfully!")
    st.experimental_rerun()  # Reload the app

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Define the total number of slots
TOTAL_SLOTS = 10

# MySQL database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Isha@210',
            database='registration'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None
def get_slot_queue(connection):
    try:
        cursor = connection.cursor()
        
        # Fetch occupied slots from vehicles table
        query = """
        SELECT slot_number FROM vehicles
        WHERE departure_time IS NULL
        """
        cursor.execute(query)
        vehicles_occupied_slots = set(slot[0] for slot in cursor.fetchall())
        
        # Fetch occupied slots from reservations table
        reservations_query = """
        SELECT slot_number FROM reservations
        WHERE reservation_period > 0
        """
        cursor.execute(reservations_query)
        reservations_occupied_slots = set(slot[0] for slot in cursor.fetchall())
        
        # Combine both sets of occupied slots
        occupied_slots = vehicles_occupied_slots.union(reservations_occupied_slots)
        
        # Create a queue of all slots
        slot_queue = deque(range(1, TOTAL_SLOTS + 1))
        
        # Remove occupied slots from the queue
        for slot in occupied_slots:
            if slot in slot_queue:
                slot_queue.remove(slot)
        
        return slot_queue
    
    except Error as e:
        st.error(f"Error fetching slot queue: {e}")
        return deque()
    
    finally:
        if cursor:
            cursor.close()




def update_service_details(connection, customer_name, vehicle_number, service_name, service_amount):
    try:
        cursor = connection.cursor()
        
        # Check if the vehicle entry exists
        query = """
        SELECT COUNT(*) FROM vehicles
        WHERE customer_name = %s AND vehicle_number = %s
        """
        cursor.execute(query, (customer_name, vehicle_number))
        vehicle_exists = cursor.fetchone()[0]
        
        if vehicle_exists:
            # Update the service details
            update_query = """
            UPDATE vehicles
            SET services_taken = CONCAT(IFNULL(services_taken, ''), %s, ', '),
                service_amount = IFNULL(service_amount, 0) + %s
            WHERE customer_name = %s AND vehicle_number = %s
            """
            cursor.execute(update_query, (service_name, service_amount, customer_name, vehicle_number))
            connection.commit()
            st.success(f"Service '{service_name}' booked successfully for vehicle {vehicle_number}.")
        else:
            st.error("Vehicle not found. Please ensure the vehicle number and customer name are correct.")

    except Error as e:
        st.error(f"Error updating service details: {e}")


def accessibility_services_page():
    st.header("Accessibility Services")

    customer_name = st.text_input("Customer Name:")
    vehicle_number = st.text_input("Vehicle Number:")

    if customer_name and vehicle_number:
    

        st.write("EV Charging")
        st.image(gif_path2, caption="EV Charging Station : ₹250", use_column_width=False)
        EV_charging_price = 250
        if st.button("Book EV Charging"):
            update_service_details(connection, customer_name, vehicle_number, "EV Charging", EV_charging_price)

        st.write("Annual Maintenance")
        st.image(gif_path3, caption="Annual Maintenance Service : ₹200", use_column_width=False)
        maintenance_price = 200  
        if st.button("Book Annual Maintenance"):
            update_service_details(connection, customer_name, vehicle_number, "Annual Maintenance", maintenance_price)

        st.write("Car Washing")
        st.image(gif_path4, caption="Vehicle Washing Service : ₹100", use_column_width=False)
        vehicle_washing_price = 100  
        if st.button("Book Vehicle Washing"):
            update_service_details(connection, customer_name, vehicle_number, "Vehicle Washing", vehicle_washing_price)


        st.write("Valet Parking")
        st.image(gif_path1, caption="Valet Parking Service : ₹50", use_column_width=False)
        valet_parking_price = 50
        if st.button("Book Valet Parking"):
            update_service_details(connection, customer_name, vehicle_number, "Valet Parking", valet_parking_price)


    else:
        st.warning("Please provide both customer name and vehicle number.")
    


def insert_reservation(connection, customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period ):
    try:
        cursor = connection.cursor()
        slot_queue = get_slot_queue(connection)

        if not slot_queue:
            st.error("Parking is full. No available slots.")
            return

        # Attempt to find an available slot
        slot_number = None
        while slot_queue:
            slot_number = slot_queue.popleft()  # Get the next slot from the queue

            # Check if the slot is occupied or reserved
            query = """
            SELECT slot_number FROM reservations
            WHERE slot_number = %s AND reservation_period > 0
            UNION
            SELECT slot_number FROM vehicles
            WHERE slot_number = %s AND departure_time IS NULL
            """
            cursor.execute(query, (slot_number, slot_number))
            result = cursor.fetchone()

            if not result:
                break  # Slot is available, exit the loop

        if not slot_number:
            st.error("No available slots found after checking the queue.")
            return
            
        
        query = """
        INSERT INTO reservations (customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period))
        connection.commit()
        st.success(f"Reservation created successfully for Slot Number: {slot_number}")
    except Error as e:
        st.error(f"Error inserting reservation data into MySQL table: {e}")

def insert_vehicle_entry(connection, customer_name, vehicle_number, vehicle_color, vehicle_type):
    try:
        cursor = connection.cursor()
        slot_queue = get_slot_queue(connection)  # Function to get the queue of available slots
        
        if not slot_queue:
            st.error("Parking is full. No available slots.")
            return

        # Attempt to find an available slot
        slot_number = None
        while slot_queue:
            slot_number = slot_queue.popleft()  # Get the next slot from the queue
            
            # Check if the slot is occupied or reserved
            query = """
            SELECT slot_number FROM vehicles
            WHERE slot_number = %s AND departure_time IS NULL
            UNION
            SELECT slot_number FROM reservations
            WHERE slot_number = %s AND reservation_period > 0
            """
            cursor.execute(query, (slot_number, slot_number))
            result = cursor.fetchone()
            
            if not result:
                break  # Slot is available, exit the loop
        
        if not slot_number:
            st.error("No available slots found after checking the queue.")
            return
        
        # Insert the new vehicle entry into the database
        now = datetime.now()
        query = """
        INSERT INTO vehicles (customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, arrival_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, now))
        connection.commit()
        st.success(f"Vehicle entry added successfully with Slot Number: {slot_number}")
    except Error as e:
        st.error(f"Error inserting data into MySQL table: {e}")

def generate_bill_for_vehicle(connection, customer_name, vehicle_number, payment_method):
    try:
        cursor = connection.cursor()
        
        # Check in vehicles table
        query = """
        SELECT customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, arrival_time, departure_time, service_amount
        FROM vehicles
        WHERE customer_name = %s AND vehicle_number = %s
        """
        cursor.execute(query, (customer_name, vehicle_number))
        vehicle_entry = cursor.fetchone()

        if vehicle_entry:
            customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, arrival_time, departure_time, service_amount = vehicle_entry
            
            # Ensure service_amount is a Decimal
            if service_amount is None:
                service_amount = Decimal(0)
            elif isinstance(service_amount, float):
                service_amount = Decimal(service_amount)
            elif not isinstance(service_amount, Decimal):
                service_amount = Decimal(service_amount)
                
            # Default departure time to now if it's None
            departure_time = departure_time if departure_time else datetime.now()
            
            # Calculate duration in minutes
            if isinstance(arrival_time, str):
                arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
            duration = (departure_time - arrival_time).total_seconds() / 60
            
            # Calculate parking amount (2 rupees per minute)
            parking_amount = Decimal(duration) * Decimal(2)
            
            # Calculate total amount
            total_amount = parking_amount + service_amount

            # Update departure time and parking amount in the database
            update_query = """
            UPDATE vehicles
            SET departure_time = %s, parking_amount = %s, total_amount = %s, payment_method = %s
            WHERE customer_name = %s AND vehicle_number = %s
            """
            cursor.execute(update_query, (departure_time, parking_amount, total_amount, payment_method, customer_name, vehicle_number))
            connection.commit()

            # Format date and time
            formatted_arrival_time = arrival_time.strftime("%Y-%m-%d %H:%M:%S")
            formatted_departure_time = departure_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Display the bill details
            st.write("### Bill Details")
            st.write(f"**Customer Name:** {customer_name}")
            st.write(f"**Vehicle Number:** {vehicle_number}")
            st.write(f"**Vehicle Color:** {vehicle_color}")
            st.write(f"**Vehicle Type:** {vehicle_type}")
            st.write(f"**Slot Number:** {slot_number}")
            st.write(f"**Arrival Time:** {formatted_arrival_time}")
            st.write(f"**Departure Time:** {formatted_departure_time}")
            st.write(f"**Duration:** {duration:.2f} minutes")
            st.write(f"**Parking Amount:** ₹{parking_amount:.2f}")
            st.write(f"**Service Amount:** ₹{service_amount:.2f}")
            st.write(f"**Total Amount:** ₹{total_amount:.2f}")
            st.write(f"**Payment Method:** {payment_method}")

            # Free the slot (if applicable)
            st.success(f"Slot {slot_number} is now free.")
            
        else:
            # Check in reservations table if not found in vehicles
            query = """
            SELECT customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period,reservation_amount
            FROM reservations
            WHERE customer_name = %s AND vehicle_number = %s
            """
            cursor.execute(query, (customer_name, vehicle_number))
            reservation_entry = cursor.fetchone()

            if reservation_entry:
                # Process reservation
                customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period, reservation_amount = reservation_entry
                
                # Calculate the bill amount based on reservation period
                reservation_amount = Decimal(reservation_period * 10)


                update_query = """
                UPDATE reservations
                SET reservation_period = %s, reservation_amount = %s, slot_number = NULL
                WHERE customer_name = %s AND vehicle_number = %s
                """
                cursor.execute(update_query, (reservation_period, reservation_amount,
                                          customer_name, vehicle_number))
                connection.commit()

                st.write("### Bill Details")
                st.write(f"**Customer Name:** {customer_name}")
                st.write(f"**Vehicle Number:** {vehicle_number}")
                st.write(f"**Vehicle Color:** {vehicle_color}")
                st.write(f"**Vehicle Type:** {vehicle_type}")
                st.write(f"**Slot Number:** {slot_number}")
                st.write(f"**Reservation Period:** {reservation_period} days")
                st.write(f"**Reservation Amount:** ₹{reservation_amount:.2f}")
                #st.write(f"**Payment Method:** {payment_method}")

                # Free the slot
                st.success(f"Slot {slot_number} is now free.")
            else:
                st.error("No such vehicle or reservation found.")
    except Error as e:
        st.error(f"Error generating bill: {e}")
        

def view_total_summary(connection):
    try:
        cursor = connection.cursor()
        
        # Total number of vehicles
        vehicles_query = vehicles_query = """SELECT SUM(count) AS total_count
                                                FROM (
                                                        SELECT COUNT(*) AS count FROM vehicles WHERE departure_time IS NULL
                                                        UNION ALL
                                                        SELECT COUNT(*) AS count FROM reservations WHERE slot_number IS NOT NULL
                                                    ) AS combined_counts;
                                            """

        #"SELECT COUNT(*) FROM vehicles WHERE departure_time IS NULL"
        cursor.execute(vehicles_query)
        total_vehicles = cursor.fetchone()[0]

        # Total amount earned
        earnings_query = "SELECT IFNULL(SUM(parking_amount), 0) FROM vehicles WHERE parking_amount IS NOT NULL"
        cursor.execute(earnings_query)
        total_parking_amount = cursor.fetchone()[0]

        earnings_query = "SELECT IFNULL(SUM(service_amount), 0) FROM vehicles WHERE service_amount IS NOT NULL"
        cursor.execute(earnings_query)
        total_service_amount = cursor.fetchone()[0]

        earnings_query = "SELECT IFNULL(SUM(reservation_amount), 0) FROM reservations WHERE reservation_amount IS NOT NULL"
        cursor.execute(earnings_query)
        total_reservation_amount = cursor.fetchone()[0]

        st.write("### Total Summary")
        st.write(f"**Total Number of Vehicles:** {total_vehicles}")
        st.write(f"**Total Parking Amount Earned:** ₹{total_parking_amount:.2f}")
        st.write(f"**Total Services Amount Earned:** ₹{total_service_amount:.2f}")
        st.write(f"**Total Reservation Amount Earned:** ₹{total_reservation_amount:.2f}")

    except Error as e:
        st.error(f"Error fetching total summary: {e}")

def view_all_parked_vehicles(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, arrival_time, departure_time, payment_method, parking_amount, services_taken, service_amount, total_amount
        FROM vehicles
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
                        # Create a DataFrame from the result
            df = pd.DataFrame(result, columns=["Customer Name", "Vehicle Number", "Vehicle Color", "Vehicle Type", "Slot Number", "Arrival Time",
                                               "Departure Time", "Payment method", "Parking amount", "Services taken", "Service amount","Total amount"])
            st.write("### Parked Vehicles")
            st.dataframe(df)  # Use st.dataframe with a DataFrame
        else:
            st.write("No vehicles are currently parked.")
    except Error as e:
        st.error(f"Error fetching parked vehicles: {e}")


def view_reserved_vehicles(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_amount,reservation_period
        FROM reservations
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
                        # Create a DataFrame from the result
            df = pd.DataFrame(result, columns=["Customer Name", "Vehicle Number", "Vehicle Color", "Vehicle Type", "Slot Number",
                                                "Reservation amount","Reservation Periods"])
            st.write("### Parked Vehicles")
            st.dataframe(df)  # Use st.dataframe with a DataFrame
        else:
            st.write("No vehicles are currently parked.")
    except Error as e:
        st.error(f"Error fetching parked vehicles: {e}")




def plot_vehicle_type_pie_chart(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT vehicle_type, COUNT(*) AS count
        FROM vehicles
        GROUP BY vehicle_type
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            # Create a DataFrame from the result
            df = pd.DataFrame(result, columns=["Vehicle Type", "Count"])

            # Plot using Plotly
            fig = px.pie(df, values='Count', names='Vehicle Type', title='Vehicle Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for plotting.")
    except Error as e:
        st.error(f"Error plotting pie chart: {e}")


        


def display_slot_availability(connection):
    try:
        cursor = connection.cursor()
        
        # Query to get occupied slots
        query = """
        SELECT slot_number FROM vehicles
        WHERE departure_time IS NULL
        """
        cursor.execute(query)
        occupied_slots = set(slot[0] for slot in cursor.fetchall())

        # Query to get reserved slots
        query = """
        SELECT slot_number FROM reservations
        WHERE reservation_period > 0
        """
        cursor.execute(query)
        reserved_slots = set(slot[0] for slot in cursor.fetchall())

        # Create a list of slots and their availability status
        slots = list(range(1, TOTAL_SLOTS + 1))
        availability = ['Occupied' if slot in occupied_slots else 'Reserved' if slot in reserved_slots else 'Available' for slot in slots]

        # Generate HTML to display slots as colored boxes
        html = '<div style="display: flex; flex-wrap: wrap; gap: 5px;">'
        for slot, status in zip(slots, availability):
            color = 'red' if status == 'Occupied' else 'blue' if status == 'Reserved' else 'green'
            html += f'<div style="width: 50px; height: 50px; background-color: {color}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{slot}</div>'
        html += '</div>'
        html += '<p style="font-weight: bold;">Available slots are green, reserved slots are blue, occupied slots are red.</p>'

        st.markdown(html, unsafe_allow_html=True)
    except Error as e:
        st.error(f"Error displaying slot availability: {e}")


def reserve_slot_page(connection):
    st.header("Reserve Slot")

    # Display real-time slot availability
    if connection:
        display_slot_availability(connection)

    # Input fields for reservation
    customer_name = st.text_input("Customer Name:")
    vehicle_number = st.text_input("Vehicle Number:")
    vehicle_color = st.text_input("Vehicle Color:")
    vehicle_type = st.selectbox("Vehicle Type:", ["2 Wheeler", "4 Wheeler"])
    
    # Select reservation period 
    reservation_period = st.number_input("Reservation Period:", min_value=1, value=1)

    if st.button("Reserve Slot"):
        if connection and customer_name and vehicle_number:
            # Get available slot
            slot_queue = get_slot_queue(connection)
            
            if slot_queue:
                slot_number = slot_queue.popleft()  # Get the next available slot
                insert_reservation(connection, customer_name, vehicle_number, vehicle_color, vehicle_type, slot_number, reservation_period)
            else:
                st.error("No available slots for reservation.")
        else:
            st.error("Please provide all required information.")







# Main section of your Streamlit app
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if not st.session_state.logged_in:
    login_page()
else:
    # Add logout button to the sidebar
    if st.sidebar.button("Logout"):
        logout()

    # Title of the web app
    st.title("Queue Optimizer For Vehicle Parking System :car:")

    # Sidebar for menu options
    menu = st.sidebar.selectbox("Menu", ["Entry", "Accessibility Services","Reserve Slot","Generate Bill", "Manage Data"])

    # Create a connection to the database
    connection = create_connection()
    # Load the Lottie animation for the entry and bill generation pages
    lottie_animation = load_lottieurl("https://lottie.host/165e75bb-a9d9-49d4-8c11-5bacf5ebf57d/vln5vVt2JM.json")

    gif_path1 =r"C:\Users\user\valet_parking1-ezgif.com-resize.gif"
    gif_path2=r"C:\Users\user\ezgif.com-crop.gif"
    gif_path3=r"C:\Users\user\annual_car_maintenancegif1-ezgif.com-resize.gif"
    gif_path4=r"C:\Users\user\carwashinggif1-ezgif.com-resize.gif"


    left_column, right_column = st.columns(2)
    with left_column:
        st.header("  ")
    with right_column:
        st_lottie(lottie_animation, height=300, key="animation")

    if menu == "Entry":
        # Entry Window
        st.header("Entry Window")

        # Display real-time slot availability
        if connection:
            display_slot_availability(connection)

        # Input fields for entry window
        customer_name = st.text_input("Customer Name:")
        vehicle_number = st.text_input("Vehicle Number:")
        vehicle_color = st.text_input("Vehicle Color:")
        vehicle_type = st.selectbox("Vehicle Type:", ["2 Wheeler", "4 Wheeler"])

        if st.button("Submit Entry"):
            if connection:
                insert_vehicle_entry(connection, customer_name, vehicle_number, vehicle_color, vehicle_type)

    elif menu == "Accessibility Services":
        # Accessibility Services Window
        if connection:
            accessibility_services_page()
            
    elif menu == "Generate Bill":
        # Generate Bill Window
        st.header("Generate Bill")
            
        # Input fields for bill generation
        bill_customer_name = st.text_input("Customer Name (Bill):")
        bill_vehicle_number = st.text_input("Vehicle Number (Bill):")
            
        # Show payment method dropdown
        payment_method = st.selectbox("Payment Method:", ["Cash", "Card"])
            
        if st.button("Generate Bill"):
            if connection and bill_customer_name and bill_vehicle_number:
                generate_bill_for_vehicle(connection, bill_customer_name, bill_vehicle_number, payment_method)
            else:
                st.error("Please provide both customer name and vehicle number.")


            
    elif menu == "Manage Data":
        # Manage Data Window
        st.header("Manage Data")
            
        manage_option = st.selectbox("Manage Options:", ["Total Summary", "View All Parked Vehicles", "View Reserved Vehicles","Vehicle Type Distribution"])

        if manage_option == "Total Summary":
            if connection:
                view_total_summary(connection)

        elif manage_option == "View All Parked Vehicles":
            if connection:
                view_all_parked_vehicles(connection)
                
        elif manage_option == "View Reserved Vehicles":
            if connection:
                view_reserved_vehicles(connection)
        

        elif manage_option == "Vehicle Type Distribution":
            if connection:
                plot_vehicle_type_pie_chart(connection)

    elif menu == "Reserve Slot":
        if connection:
            # Reserve Slot Page
            reserve_slot_page(connection)

    else:
        st.error("Failed to connect to the database.")

    # Close the connection when the app is stopped
    if connection and connection.is_connected():
        connection.close()

