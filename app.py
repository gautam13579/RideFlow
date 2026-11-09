import math
import streamlit as st
import threading
import sqlite3
from pathlib import Path
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

# =====================================================
# RIDEFLOW PDF RENTAL INVOICE GENERATOR
# =====================================================

def generate_rental_invoice_pdf(invoice):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "RideFlowTitle",
        parent=styles["Title"],
        fontSize=26,
        textColor=colors.HexColor("#126B70"),
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "RideFlowSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#60748A"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    story = []

    # Company heading
    story.append(Paragraph("RIDEFLOW", title_style))

    story.append(Paragraph(
        "SMART BICYCLE & ELECTRIC SCOOTER RENTAL SYSTEM",
        subtitle_style
    ))

    story.append(Paragraph(
        "RENTAL INVOICE",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 12))

    # Invoice information
    invoice_data = [
        ["Invoice ID", str(invoice["Invoice ID"])],
        ["Customer Name", str(invoice["Customer"])],
        ["Vehicle ID", str(invoice["Vehicle ID"])],
        ["Vehicle Category", str(invoice["Type"])],
        ["Rental Start Time", str(invoice["Rental Time"])],
        ["Return Time", str(invoice["Return Time"])]
    ]

    details_table = Table(
        invoice_data,
        colWidths=[160, 290]
    )

    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#E8F3F5")),

        ("TEXTCOLOR", (0, 0), (-1, -1),
         colors.HexColor("#173653")),

        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),

        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#D6E2EF")),

        ("PADDING", (0, 0), (-1, -1), 10),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(details_table)

    story.append(Spacer(1, 25))

    story.append(Paragraph(
        "PAYMENT SUMMARY",
        styles["Heading2"]
    ))

    # Billing information
    billing_data = [
        ["Description", "Amount"],
        ["Rental Duration",
         f'{invoice["Rental Hours"]} hour(s)'],

        ["Hourly Rate",
         f'Rs. {invoice["Hourly Rate (₹)"]}'],

        ["Total Amount",
         f'Rs. {invoice["Total Amount (₹)"]}']
    ]

    billing_table = Table(
        billing_data,
        colWidths=[300, 150]
    )

    billing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#126B70")),

        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),

        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),

        ("BACKGROUND", (0, 1), (-1, -2),
         colors.HexColor("#F3F7FC")),

        ("BACKGROUND", (0, -1), (-1, -1),
         colors.HexColor("#DDF3EB")),

        ("TEXTCOLOR", (0, -1), (-1, -1),
         colors.HexColor("#087F5B")),

        ("FONTNAME", (0, -1), (-1, -1),
         "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#D6E2EF")),

        ("PADDING", (0, 0), (-1, -1), 12)
    ]))

    story.append(billing_table)

    story.append(Spacer(1, 35))

    story.append(Paragraph(
        "Thank you for choosing RideFlow!",
        ParagraphStyle(
            "FooterMessage",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#126B70"),
            fontSize=12
        )
    ))

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================


# RIDEFLOW GLOBAL THEME
st.markdown("""
<style>
.stApp {
    background-color: #F3F7FC;
}

/* Premium top navigation bar */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg,#10243A,#125B68,#147D78) !important;
}

/* Toolbar transparency */
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: transparent !important;
}

/* Main content headings */
h1, h2, h3 {
    color: #173653;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: #10243A;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 2. PROFESSIONAL UI DESIGN
# =====================================================

st.markdown("""

<style>
/* ===== GLOBAL THEME ===== */

.stApp,
[data-testid="stAppViewContainer"] {
    background: #F3F6FA !important;
    color: #172B45 !important;
}

.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1500px;
}

/* ===== MAIN PAGE TYPOGRAPHY ===== */

h1, h2, h3, h4, h5, h6 {
    color: #172B45 !important;
    font-weight: 700 !important;
}

.stMarkdown p,
.stMarkdown li {
    color: #40536A !important;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #60748A !important;
    opacity: 1 !important;
}

/* ===== SIDEBAR ===== */

[data-testid="stSidebar"] {
    background: #10243A !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Fix faint sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #D5E2EF !important;
    opacity: 1 !important;
}

/* Sidebar navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #FFFFFF !important;
}

/* ===== HERO HEADER ===== */

.hero {
    background: linear-gradient(120deg, #10243A, #126B70);
    padding: 36px;
    border-radius: 20px;
    color: #FFFFFF !important;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(16,36,58,.13);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px !important;
}

.hero p {
    color: #E2F1F2 !important;
    opacity: 1 !important;
    font-size: 16px;
}

/* ===== METRIC CARDS ===== */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2EAF2;
    border-radius: 16px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 5px 16px rgba(25,45,70,.05);
}

.metric-label {
    color: #60748A !important;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #142A43 !important;
    font-size: 34px;
    font-weight: 750;
    margin-top: 8px;
}

/* ===== VEHICLE CARDS ===== */

.vehicle-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E1E9F1;
    box-shadow: 0 5px 18px rgba(25,45,70,.05);
}

.vehicle-card h3 {
    color: #172B45 !important;
}

.vehicle-card p {
    color: #60748A !important;
}

/* ===== BUTTONS ===== */

.stButton > button,
.stFormSubmitButton > button {
    background: #126B70 !important;
    color: #FFFFFF !important;
    border: 1px solid #126B70 !important;
    border-radius: 10px !important;
    min-height: 45px;
    font-weight: 650 !important;
}

.stButton > button *,
.stFormSubmitButton > button * {
    color: #FFFFFF !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #0D5358 !important;
    border-color: #0D5358 !important;
    color: #FFFFFF !important;
}

/* ===== FORMS AND INPUTS ===== */

[data-testid="stForm"] {
    background: #FFFFFF !important;
    padding: 22px;
    border: 1px solid #E2EAF2;
    border-radius: 16px;
}

[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: #172B45 !important;
}

[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172B45 !important;
}

/* ===== DATA TABLE ===== */

[data-testid="stDataFrame"] {
    border: 1px solid #E2EAF2;
    border-radius: 12px;
    overflow: hidden;
}

/* ===== FOOTER ===== */

.footer {
    text-align: center;
    color: #60748A !important;
    padding: 20px;
    font-size: 13px;
}

.footer b {
    color: #126B70 !important;
}
</style>

""", unsafe_allow_html=True)


# =====================================================
# 3. RENTAL MANAGEMENT SYSTEM
# =====================================================


class RentalSystem:

    def __init__(self):

        # Database file will be created beside app.py
        self.db_path = Path(__file__).resolve().parent / "rideflow.db"

        # Thread synchronization
        self.mutex = threading.Lock()

        # Connect to SQLite
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        # Create database tables
        self.create_tables()

        # Add default fleet only on first run
        self.initialize_vehicles()

        # Restore semaphore counts from saved database
        with self.mutex:
            available_bikes = self.conn.execute("""
                SELECT COUNT(*) FROM vehicles
                WHERE vehicle_type = 'Bicycle'
                AND status != 'Rented'
            """).fetchone()[0]

            available_scooters = self.conn.execute("""
                SELECT COUNT(*) FROM vehicles
                WHERE vehicle_type = 'Electric Scooter'
                AND status != 'Rented'
            """).fetchone()[0]

        self.bicycle_semaphore = threading.Semaphore(
            available_bikes
        )

        self.scooter_semaphore = threading.Semaphore(
            available_scooters
        )

    # --------------------------------
    # DATABASE TABLE CREATION
    # --------------------------------
    def create_tables(self):

        with self.mutex:

            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                vehicle_id TEXT PRIMARY KEY,
                vehicle_type TEXT NOT NULL,
                status TEXT NOT NULL,
                customer TEXT
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS rental_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id TEXT NOT NULL,
                customer TEXT,
                vehicle_type TEXT NOT NULL,
                action TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """)

        # Add pricing columns to existing database safely
        existing_columns = [
            column["name"]
            for column in self.conn.execute(
                "PRAGMA table_info(rental_history)"
            ).fetchall()
        ]

        new_columns = {
            "return_time": "TEXT",
            "rental_hours": "REAL",
            "hourly_rate": "INTEGER",
            "total_amount": "REAL"
        }

        for column_name, column_type in new_columns.items():

            if column_name not in existing_columns:

                self.conn.execute(
                    f"ALTER TABLE rental_history ADD COLUMN "
                    f"{column_name} {column_type}"
                )

        self.conn.commit()

    # --------------------------------
    # INITIALIZE DEFAULT VEHICLES
    # --------------------------------

    def initialize_vehicles(self):

        with self.mutex:

            count = self.conn.execute(
                "SELECT COUNT(*) FROM vehicles"
            ).fetchone()[0]

            if count == 0:

                for i in range(1, 11):
                    self.conn.execute("""
                        INSERT INTO vehicles
                        VALUES (?, ?, ?, ?)
                    """, (
                        f"BIKE-{i:03}",
                        "Bicycle",
                        "Available",
                        None
                    ))

                for i in range(1, 9):
                    self.conn.execute("""
                        INSERT INTO vehicles
                        VALUES (?, ?, ?, ?)
                    """, (
                        f"SCOOTER-{i:03}",
                        "Electric Scooter",
                        "Available",
                        None
                    ))

                self.conn.commit()

    # --------------------------------
    # GET SEMAPHORE
    # --------------------------------

    def get_semaphore(self, vehicle_type):

        if vehicle_type == "Bicycle":
            return self.bicycle_semaphore

        return self.scooter_semaphore

    # --------------------------------
    # RENT VEHICLE
    # --------------------------------

    def rent_vehicle(self, customer, vehicle_type):

        semaphore = self.get_semaphore(vehicle_type)

        if not semaphore.acquire(blocking=False):
            return False, "No vehicles available!"

        with self.mutex:

            vehicle = self.conn.execute("""
                SELECT vehicle_id
                FROM vehicles
                WHERE vehicle_type = ?
                AND status != 'Rented'
                LIMIT 1
            """, (vehicle_type,)).fetchone()

            if vehicle:

                vehicle_id = vehicle["vehicle_id"]

                try:
                    self.conn.execute("""
                        UPDATE vehicles
                        SET status = 'Rented',
                            customer = ?
                        WHERE vehicle_id = ?
                    """, (customer, vehicle_id))

                    self.conn.execute("""
                        INSERT INTO rental_history
                        (vehicle_id, customer, vehicle_type, action, time)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        vehicle_id,
                        customer,
                        vehicle_type,
                        "Rented",
                        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    ))

                    self.conn.commit()

                    return True, (
                        f"{vehicle_id} rented successfully!"
                    )

                except sqlite3.Error as error:
                    self.conn.rollback()
                    semaphore.release()
                    return False, f"Database error: {error}"

            semaphore.release()
            return False, "Vehicle allocation failed!"

    # --------------------------------
    # RETURN VEHICLE
    # --------------------------------


    # --------------------------------
    # RETURN VEHICLE
    # --------------------------------

    def return_vehicle(self, vehicle_id):

        with self.mutex:

            vehicle = self.conn.execute("""
                SELECT vehicle_type, customer
                FROM vehicles
                WHERE vehicle_id = ?
                AND status = 'Rented'
            """, (vehicle_id,)).fetchone()

            if not vehicle:
                return False, "Vehicle is not currently rented!"

            try:
                vehicle_type = vehicle["vehicle_type"]
                customer = vehicle["customer"]

                booking = self.conn.execute("""
                    SELECT id, time
                    FROM rental_history
                    WHERE vehicle_id = ?
                    AND action = 'Rented'
                    AND return_time IS NULL
                    ORDER BY id DESC
                    LIMIT 1
                """, (vehicle_id,)).fetchone()

                if not booking:
                    return False, "Original booking record not found!"

                booking_time = datetime.strptime(
                    booking["time"],
                    "%d-%m-%Y %H:%M:%S"
                )

                return_datetime = datetime.now()

                elapsed_seconds = (
                    return_datetime - booking_time
                ).total_seconds()

                if elapsed_seconds < 0:
                    return False, "Invalid rental time!"

                rental_hours = max(
                    1,
                    math.ceil(elapsed_seconds / 3600)
                )

                hourly_rate = (
                    20 if vehicle_type == "Bicycle" else 50
                )

                total_amount = rental_hours * hourly_rate

                return_time = return_datetime.strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

                self.conn.execute("""
                    UPDATE vehicles
                    SET status = 'Returned',
                        customer = NULL
                    WHERE vehicle_id = ?
                """, (vehicle_id,))

                self.conn.execute("""
                    UPDATE rental_history
                    SET return_time = ?,
                        rental_hours = ?,
                        hourly_rate = ?,
                        total_amount = ?
                    WHERE id = ?
                """, (
                    return_time,
                    rental_hours,
                    hourly_rate,
                    total_amount,
                    booking["id"]
                ))

                self.conn.execute("""
                    INSERT INTO rental_history
                    (
                        vehicle_id,
                        customer,
                        vehicle_type,
                        action,
                        time,
                        return_time,
                        rental_hours,
                        hourly_rate,
                        total_amount
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    vehicle_id,
                    customer,
                    vehicle_type,
                    "Returned",
                    return_time,
                    return_time,
                    rental_hours,
                    hourly_rate,
                    total_amount
                ))

                self.conn.commit()

            except (sqlite3.Error, ValueError) as error:
                self.conn.rollback()
                return False, f"Return error: {error}"

            self.get_semaphore(vehicle_type).release()

            return True, (
                f"{vehicle_id} returned successfully! "
                f"Duration: {rental_hours} hour(s) | "
                f"Rate: ₹{hourly_rate}/hour | "
                f"Total Amount: ₹{total_amount}"
            )



    # --------------------------------
    # GET VEHICLES AND HISTORY
    # --------------------------------

    def get_data(self):

        with self.mutex:

            vehicle_rows = self.conn.execute("""
                SELECT
                    vehicle_id AS 'Vehicle ID',
                    vehicle_type AS 'Vehicle Type',
                    status AS 'Status',
                    customer AS 'Customer'
                FROM vehicles
                ORDER BY vehicle_id
            """).fetchall()

            history_rows = self.conn.execute("""
                SELECT
                    vehicle_id AS 'Vehicle ID',
                    customer AS 'Customer',
                     vehicle_type AS 'Type',
                    action AS 'Action',
                    time AS 'Rental Time',
                    return_time AS 'Return Time',
                    rental_hours AS 'Rental Hours',
                    hourly_rate AS 'Hourly Rate (₹)',
                    total_amount AS 'Total Amount (₹)'
                FROM rental_history
                ORDER BY id
            """).fetchall()

            return (
                [dict(row) for row in vehicle_rows],
                [dict(row) for row in history_rows]
            )

    # --------------------------------
    # COUNT AVAILABLE VEHICLES
    # --------------------------------

    def count_available(self, vehicle_type):

        with self.mutex:

            count = self.conn.execute("""
                SELECT COUNT(*)
                FROM vehicles
                WHERE vehicle_type = ?
                AND status != 'Rented'
            """, (vehicle_type,)).fetchone()[0]

            return count


# =====================================================
# 4. SHARED SYSTEM INSTANCE
# =====================================================

# New function name ensures fresh inventory for this upgrade.
@st.cache_resource
def get_system_v3():
    return RentalSystem()


system = get_system_v3()

# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown("# 🚲 RideFlow")
st.sidebar.caption("SMART RENTAL MANAGEMENT")

st.sidebar.divider()

pages = [
    "Dashboard",
    "Rent a Vehicle",
    "Return a Vehicle",
    "Fleet Management",
    "Rental History"
]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def navigate_to(target):
    st.session_state.page = target


page = st.sidebar.radio(
    "NAVIGATION",
    pages,
    key="page"
)


st.sidebar.divider()

st.sidebar.markdown("### SYSTEM STATUS")
st.sidebar.success("● System Online")
st.sidebar.caption("Counting Semaphore Active")
st.sidebar.caption("Mutex Protection Active")

st.sidebar.divider()


# ==========================================
# ABOUT RIDEFLOW - FIXED HTML RENDERING
# ==========================================


# PREMIUM RIDEFLOW HERO BANNER
st.html("""
<div style="background:linear-gradient(120deg,#10243A,#125B68,#147D78);padding:42px 38px;border-radius:22px;border:1px solid #287E86;box-shadow:0 12px 30px rgba(16,36,58,0.18);margin-bottom:10px;">
<div style="color:#63E6D0;font-size:13px;font-weight:800;letter-spacing:3px;">
SMART MOBILITY MANAGEMENT
</div>
<h1 style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-size:40px;font-weight:800;margin:18px 0;">
🚲 Welcome to RideFlow
</h1>
<h3 style="color:#D6F5F1 !important;-webkit-text-fill-color:#D6F5F1 !important;font-size:22px;">
Your Smart Bicycle & Electric Scooter Rental Platform
</h3>
<p style="color:#FFFFFF !important;font-size:16px;line-height:1.9;">
Experience smarter vehicle rental management. Manage your fleet,
allocate vehicles, monitor availability and track customer rentals
through one intelligent platform.
</p>
<div style="margin-top:22px;line-height:3;">
<span style="background:#FFFFFF25;color:#FFFFFF;padding:10px;border-radius:8px;">🚲 Smart Fleet</span>
<span style="background:#FFFFFF25;color:#FFFFFF;padding:10px;border-radius:8px;">⚡ Electric Mobility</span>
<span style="background:#FFFFFF25;color:#FFFFFF;padding:10px;border-radius:8px;">🔒 Secure Allocation</span>
<span style="background:#FFFFFF25;color:#FFFFFF;padding:10px;border-radius:8px;">📊 Live Monitoring</span>
</div>
</div>
""")



# ==========================================
# PREMIUM SIDEBAR - ABOUT APPLICATION
# ==========================================



# ABOUT RIDEFLOW - CLEAN SIDEBAR
with st.sidebar:
    st.html("""
    <div style="background:linear-gradient(145deg,#173B57,#10243A);padding:18px;border-radius:14px;border:1px solid #31516B;">
    <h3 style="color:#FFFFFF !important;">✨ About RideFlow</h3>
    <p style="color:#FFFFFF !important;line-height:1.7;">RideFlow is an intelligent bicycle and electric scooter rental management platform designed for efficient fleet operations.</p>
    <h4 style="color:#48D6C2 !important;">🚀 Key Features</h4>
    <ul style="color:#FFFFFF !important;line-height:2;">
    <li>Bicycle Rental Management</li>
    <li>Electric Scooter Management</li>
    <li>Real-Time Fleet Availability</li>
    <li>Customer Booking & Returns</li>
    <li>Rental History Tracking</li>
    <li>Thread Synchronization</li>
    </ul>
    <h4 style="color:#48D6C2 !important;">💻 Technology Stack</h4>
    <p style="color:#FFFFFF !important;line-height:1.9;">Python • Streamlit • SQLite<br>Threading • Semaphore • Mutex</p>
    <hr style="border-color:#42627A;">
    <p style="color:#FFFFFF !important;font-size:12px;">Smart Mobility • Efficient Management</p>
    <p style="color:#48D6C2 !important;font-size:12px;">Version 2.0</p>
    </div>
    """)



# =====================================================
# 6. LIVE INVENTORY DATA
# =====================================================

vehicles, history = system.get_data()

bikes = [
    v for v in vehicles
    if v["Vehicle Type"] == "Bicycle"
]

scooters = [
    v for v in vehicles
    if v["Vehicle Type"] == "Electric Scooter"
]

available_bikes = system.count_available("Bicycle")

available_scooters = system.count_available(
    "Electric Scooter"
)

rented_count = sum(
    1 for v in vehicles
    if v["Status"] == "Rented"
)

total_vehicles = len(vehicles)



# =====================================================
# 8. DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("## Dashboard Overview")
    st.caption("Your fleet performance at a glance.")

    columns = st.columns(4)

    metrics = [
        ("TOTAL FLEET", total_vehicles, "🚲"),
        ("AVAILABLE BICYCLES", available_bikes, "🚴"),
        ("AVAILABLE SCOOTERS", available_scooters, "🛵"),
        ("CURRENTLY RENTED", rented_count, "🔑")
    ]

    for col, (label, value, emoji) in zip(
        columns, metrics
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">
                    <span class="metric-icon">{emoji}</span>
                    {label}
                </div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    st.markdown("## Fleet Availability")

    left, right = st.columns(2)

    with left:

        st.markdown("### 🚴 Bicycles")

        st.progress(available_bikes / 10)

        st.caption(
            f"{available_bikes} of 10 bicycles available"
        )

    with right:

        st.markdown("### 🛵 Electric Scooters")

        st.progress(available_scooters / 8)

        st.caption(
            f"{available_scooters} of 8 scooters available"
        )

    st.divider()

    st.markdown("## Recent Activity")

    if history:

        st.dataframe(
            history[-5:][::-1],
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No rental activity recorded yet.")


  
    st.divider()

    st.markdown("## Quick Actions")

    a, b = st.columns(2)

    with a:
        st.button(
            "🚲 Rent a Vehicle",
            width="stretch",
            on_click=navigate_to,
            args=("Rent a Vehicle",)
        )

    with b:
        st.button(
            "↩️ Return a Vehicle",
            width="stretch",
            on_click=navigate_to,
            args=("Return a Vehicle",)
        )


# =====================================================
# 9. RENTAL BOOKING
# =====================================================

# =====================================================
# 9. RENTAL BOOKING
# =====================================================

elif page == "Rent a Vehicle":

    st.markdown("## 🛵 Vehicle Booking")
    st.caption("Choose your preferred vehicle and confirm rental.")

    # VEHICLE CATEGORY SELECTION

    vehicle_type = st.selectbox(
        "Select Vehicle Category",
        ["Bicycle", "Electric Scooter"],
        key="rental_vehicle_type"
    )

    current_available = system.count_available(vehicle_type)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            CURRENTLY AVAILABLE {vehicle_type.upper()}S
        </div>
        <div class="metric-value">{current_available}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # --------------------------------
    # RENTAL BOOKING FORM
    # --------------------------------

    with st.form("rental_booking_form"):

        customer = st.text_input(
            "Customer Full Name",
            placeholder="Enter customer name"
        )

        submitted = st.form_submit_button(
            "Confirm Vehicle Booking",
            width="stretch"
        )

    # --------------------------------
    # PROCESS BOOKING
    # --------------------------------

    if submitted:

        if not customer.strip():

            st.error("Please enter customer name.")

        else:

            success, message = system.rent_vehicle(
                customer.strip(),
                vehicle_type
            )

            if success:

                vehicle_id = message.split()[0]

                _, saved_history = system.get_data()

                booking = next(
                    (
                        item for item in reversed(saved_history)
                        if item["Vehicle ID"] == vehicle_id
                        and item["Action"] == "Rented"
                    ),
                    None
                )

                if booking:

                    receipt_id = (
                        f"RF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    )

                    st.session_state["last_receipt"] = {
                        "Receipt ID": receipt_id,
                        **booking
                    }

                st.success(message)

            else:

                st.warning(message)

            st.rerun()

    # --------------------------------
    # DISPLAY RENTAL RECEIPT
    # --------------------------------

    if st.session_state.get("last_receipt"):

        receipt = st.session_state["last_receipt"]

        st.divider()

        st.markdown("## 🧾 Rental Receipt")

        st.success("Your vehicle booking is confirmed!")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("**Receipt ID**")
            st.write(receipt["Receipt ID"])

            st.markdown("**Customer Name**")
            st.write(receipt["Customer"])

            st.markdown("**Vehicle ID**")
            st.write(receipt["Vehicle ID"])

        with c2:

            st.markdown("**Vehicle Category**")
            st.write(receipt["Type"])

            st.markdown("**Booking Date & Time**")
            st.write(receipt["Rental Time"])

            st.markdown("**Booking Status**")
            st.write("Confirmed")

        receipt_text = f"""
========================================
             RIDEFLOW
          RENTAL RECEIPT
========================================

Receipt ID:       {receipt["Receipt ID"]}
Customer Name:    {receipt["Customer"]}
Vehicle ID:       {receipt["Vehicle ID"]}
Vehicle Category: {receipt["Type"]}
Booking Date:     {receipt["Rental Time"]}
Booking Status:   Confirmed

========================================
       Thank you for choosing RideFlow!
========================================
"""

        st.download_button(
            "📥 Download Rental Receipt",
            data=receipt_text,
            file_name=f"RideFlow_{receipt['Receipt ID']}.txt",
            mime="text/plain",
            width="stretch"
        )

        if st.button("Clear Receipt"):

            del st.session_state["last_receipt"]

            st.rerun()



# =====================================================
# 10. VEHICLE RETURN
# =====================================================

# =====================================================
# 10. VEHICLE RETURN
# =====================================================

elif page == "Return a Vehicle":

    st.markdown("## ↩️ Vehicle Return")
    st.caption("Select a rented vehicle to complete its return.")

    vehicles, history = system.get_data()

    rented_vehicles = [
        v for v in vehicles
        if v["Status"] == "Rented"
    ]

    if rented_vehicles:

        options = [
            f"{v['Vehicle ID']} | {v['Customer']}"
            for v in rented_vehicles
        ]

        selected = st.selectbox(
            "Select Vehicle",
            options,
            key="return_vehicle_select"
        )

        if st.button(
            "Confirm Return",
            width="stretch"
        ):

            vehicle_id = selected.split(" | ")[0]

            success, message = system.return_vehicle(
                vehicle_id
            )

            if success:

                st.session_state["last_bill"] = message

                _, updated_history = system.get_data()

                completed_booking = next(
                    (
                        item for item in reversed(updated_history)
                        if item["Vehicle ID"] == vehicle_id
                        and item["Action"] == "Rented"
                        and item["Return Time"]
                        and item["Total Amount (₹)"] is not None
                    ),
                    None
                )

                if completed_booking:

                    invoice_id = (
                        f"RF-INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    )

                    st.session_state["last_invoice"] = {
                        "Invoice ID": invoice_id,
                        **completed_booking
                    }

            else:

                st.error(message)

            st.rerun()

    else:

        st.info("No vehicles are currently rented.")

    # --------------------------------
    # DISPLAY FINAL RENTAL BILL
    # --------------------------------

    if st.session_state.get("last_bill"):

        st.divider()

        st.markdown("## 🧾 Final Rental Bill")

        st.success(st.session_state["last_bill"])

        invoice = st.session_state.get("last_invoice")

        if invoice:

            st.markdown("### 📄 Professional Rental Invoice")

            pdf_data = generate_rental_invoice_pdf(invoice)

            st.download_button(
                label="📥 Download PDF Invoice",
                data=pdf_data,
                file_name=f"RideFlow_{invoice['Invoice ID']}.pdf",
                mime="application/pdf",
                width="stretch"
            )

        if st.button("Clear Bill"):

            st.session_state.pop("last_bill", None)
            st.session_state.pop("last_invoice", None)

            st.rerun()

# =====================================================
# 11. FLEET MANAGEMENT
# =====================================================

elif page == "Fleet Management":

    st.markdown("## 🚲 Fleet Management")
    st.caption("Search, filter and monitor your complete fleet.")

    vehicles, history = system.get_data()

    search = st.text_input(
        "🔍 Search Vehicle ID or Customer"
    )

    category = st.selectbox(
        "Filter by Category",
        ["All", "Bicycle", "Electric Scooter"]
    )

    status = st.selectbox(
        "Filter by Status",
        ["All", "Available", "Rented", "Returned"]
    )

    filtered = vehicles

    if category != "All":

        filtered = [
            v for v in filtered
            if v["Vehicle Type"] == category
        ]

    if status != "All":

        filtered = [
            v for v in filtered
            if v["Status"] == status
        ]

    if search.strip():

        filtered = [
            v for v in filtered
            if search.lower() in (
                v["Vehicle ID"] + " " +
                str(v["Customer"] or "")
            ).lower()
        ]

    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )

    st.caption(f"Displaying {len(filtered)} vehicles.")


# =====================================================
# 12. RENTAL HISTORY
# =====================================================

elif page == "Rental History":

    st.markdown("## 📜 Rental History")
    st.caption("Complete record of rental transactions.")

    vehicles, history = system.get_data()

    if history:

        total_rentals = sum(
            1 for h in history
            if h["Action"] == "Rented"
        )

        total_returns = sum(
            1 for h in history
            if h["Action"] == "Returned"
        )

        # Two metric columns
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg,#FFFFFF,#E8F3FF);
                padding: 24px;
                border-radius: 15px;
                border: 1px solid #B8D5F0;
            ">
                <p style="
                    color: #173653 !important;
                    font-size: 18px;
                    font-weight: 800;
                    margin: 0 0 12px 0;
                ">📋 Total Rentals</p>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<h1 style='color:#125B9A !important;"
                f"font-size:38px;margin:0;font-weight:800;'>"
                f"{total_rentals}</h1>",
                unsafe_allow_html=True
            )

            st.markdown("""
                <p style="color:#52677D !important;
                font-size:13px;">Total booking transactions</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg,#FFFFFF,#E5F8F2);
                padding: 24px;
                border-radius: 15px;
                border: 1px solid #B5E3D2;
            ">
                <p style="
                    color: #173653 !important;
                    font-size: 18px;
                    font-weight: 800;
                    margin: 0 0 12px 0;
                ">📦 Total Returns</p>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<h1 style='color:#087F5B !important;"
                f"font-size:38px;margin:0;font-weight:800;'>"
                f"{total_returns}</h1>",
                unsafe_allow_html=True
            )

            st.markdown("""
                <p style="color:#52677D !important;
                font-size:13px;">Successfully returned vehicles</p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Rental transaction table
        st.dataframe(
            history[::-1],
            width="stretch",
            hide_index=True
        )

    else:
        st.info("No transactions available.")

# =====================================================
# 13. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    <b>RideFlow v2.0</b><br>
    Smart Bicycle & Electric Scooter Rental System<br>
    Built with Python • Streamlit • Counting Semaphore • Mutex
</div>
""", unsafe_allow_html=True)


# ==========================================
# RIDEFLOW - FORM VISIBILITY & CONTRAST FIX
# ==========================================

st.markdown("""
<style>

/* FORM LABELS */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stDateInput label,
.stTextArea label,
.stMultiSelect label {
    color: #173653 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* LABEL TEXT */
.stTextInput label p,
.stSelectbox label p,
.stNumberInput label p,
.stDateInput label p,
.stTextArea label p,
.stMultiSelect label p {
    color: #173653 !important;
}

/* TEXT INPUT BACKGROUND */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
    border: 1.5px solid #B8C9DC !important;
    border-radius: 9px !important;
    font-size: 15px !important;
}

/* PLACEHOLDER TEXT */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* SELECTBOX BACKGROUND */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
    border: 1.5px solid #B8C9DC !important;
    border-radius: 9px !important;
}

/* SELECTED VALUE */
.stSelectbox div[data-baseweb="select"] span,
.stMultiSelect div[data-baseweb="select"] span {
    color: #172B4D !important;
}

/* DROPDOWN OPTIONS */
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

div[data-baseweb="popover"] li {
    color: #172B4D !important;
}

/* INPUT FOCUS EFFECT */
.stTextInput input:focus,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #0D9488 !important;
    box-shadow: 0 0 0 2px rgba(13,148,136,0.15) !important;
}

/* FORM CONTAINERS */
div[data-testid="stForm"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE5EF !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* FORM BUTTONS */
.stFormSubmitButton button {
    background: linear-gradient(90deg,#125B68,#147D78) !important;
    color: #FFFFFF !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# RENTAL HISTORY - METRIC VISIBILITY FIX
# ==========================================


# ==========================================
# RENTAL HISTORY - LABEL VISIBILITY FIX
# ==========================================

st.markdown("""
<style>

/* Metric Cards */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E2EF !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* FORCE METRIC LABEL VISIBILITY */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] span {
    color: #10243A !important;
    -webkit-text-fill-color: #10243A !important;
    opacity: 1 !important;
    visibility: visible !important;
    font-size: 16px !important;
    font-weight: 800 !important;
}

/* Metric Numerical Values */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #10243A !important;
    -webkit-text-fill-color: #10243A !important;
    opacity: 1 !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

/* Metric Card Layout */
div[data-testid="stMetric"] {
    min-height: 110px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* RENTAL RECEIPT DOWNLOAD BUTTON */

.stDownloadButton > button {
    background: linear-gradient(90deg, #125B68, #147D78) !important;
    color: #FFFFFF !important;
    border: 1px solid #125B68 !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
}

/* FORCE DOWNLOAD BUTTON TEXT VISIBILITY */

.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* HOVER EFFECT */

.stDownloadButton > button:hover {
    background: #0D5358 !important;
    border-color: #0D5358 !important;
}

</style>
""", unsafe_allow_html=True)
