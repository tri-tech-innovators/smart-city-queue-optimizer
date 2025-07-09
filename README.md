# smart-city-queue-optimizer

A Streamlit-based intelligent queue optimizer for vehicle parking that enables efficient slot allocation, real-time slot tracking, reservation handling, and accessibility services — built using Python, Streamlit, MySQL, and Plotly.

---

## Features

- Admin login system with secure SHA-256 password hashing.
- Real-time slot availability visualization (green for available, blue for reserved, red for occupied).
- Automatic queue-based slot allocation for both entries and reservations.
- Vehicle entry form including customer details, vehicle type, and automatic slot assignment.
- Bill generation with dynamic calculation of parking amount (₹2 per minute), services amount, and total amount.
- Accessibility services: EV charging, annual maintenance, vehicle washing, valet parking — with real-time service booking and amount tracking.
- Reservation system with reservation period and dynamic reservation amount calculation (₹10 per day).
- Manage data section with:
  - Total summary (total vehicles, total parking amount, total service amount, total reservation amount).
  - View all parked vehicles with detailed records (including services taken and service amounts).
  - View all reserved vehicles.
  - Vehicle type distribution pie chart.
- Interactive UI built using Streamlit and animated Lottie visuals.
- Integrated data persistence using MySQL.

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|-------------|--------------------------|
| **Frontend** | Streamlit (Python)       |
| **Backend**  | Python (Queue logic, data processing) |
| **Database** | MySQL                    |
| **Visualization** | Plotly, Streamlit DataFrames |
| **Animations** | Lottie animations      |

---

##  Project Structure

```
queue-optimizer-vehicle-parking/
├── vip.py         # Main Streamlit application file
├── README.md      # Project documentation
├── MySQL Tables   # vehicles, reservations
├── Images/GIFs    # Local service images used in UI
```

---

## Setup Instructions

### 1️⃣ Install Dependencies

Install the required Python modules:

```bash
pip install streamlit mysql-connector-python pandas plotly streamlit-lottie pillow
```

---

### 2️⃣ MySQL Database Setup

1. Start MySQL server.
2. Create a database (e.g., `registration`).
3. Create the `vehicles` table:

```sql
CREATE TABLE vehicles (
    customer_name VARCHAR(50),
    vehicle_number VARCHAR(20) PRIMARY KEY,
    vehicle_color VARCHAR(20),
    vehicle_type VARCHAR(20),
    slot_number INT,
    arrival_time DATETIME,
    departure_time DATETIME,
    services_taken TEXT,
    service_amount DECIMAL(10,2),
    parking_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_method VARCHAR(20)
);
```

4. Create the `reservations` table:

```sql
CREATE TABLE reservations (
    customer_name VARCHAR(50),
    vehicle_number VARCHAR(20) PRIMARY KEY,
    vehicle_color VARCHAR(20),
    vehicle_type VARCHAR(20),
    slot_number INT,
    reservation_period INT,
    reservation_amount DECIMAL(10,2)
);
```

---

### 3️⃣ Configure Database Connection

In `vip.py`, update your MySQL credentials:

```python
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='YOUR_PASSWORD',
    database='registration'
)
```

Replace `YOUR_PASSWORD` with your actual MySQL password.

---

### 4️⃣ Update Image Paths

In `vip.py`, update paths for local GIFs used in accessibility services:

```python
gif_path1 = r"C:\path\to\valet_parking.gif"
gif_path2 = r"C:\path\to\ev_charging.gif"
gif_path3 = r"C:\path\to\annual_maintenance.gif"
gif_path4 = r"C:\path\to\car_washing.gif"
```

---

### 5️⃣ Run the Application

Start Streamlit app:

```bash
streamlit run vip.py
```

---

### 6️⃣ Admin Login

- **Username**: `admin`
- **Password**: `vip@03`

---

## 💡 Highlights

- Queue-based optimized slot assignment with separate logic for entries and reservations.
- Support for additional vehicle services with individual billing.
- Integrated real-time dashboard showing all parked and reserved vehicles.
- Reservation slots visually distinguished to avoid double booking.
- Vehicle type distribution analytics.

---

## 📄 Notes

- Tested on local MySQL setup — ensure your MySQL server is running before starting the app.
- Image paths must be updated according to your local system before running.
- Password stored using SHA-256 hashing for demonstration; consider environment variables or secure vaults for production.
- The vehicle number acts as the primary key and unique identifier.

---

## 💬 Questions or Contributions

Feel free to open issues or pull requests if you'd like to improve or contribute!

---

## ✅ License

This project is for educational and academic use.

---
