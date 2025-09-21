import json
import csv
import datetime
import os
import cv2
import math
from datetime import datetime, timedelta

# -------------------
# File paths
# -------------------
ACTIVE_FILE = "active_code.json"
ATTENDANCE_FILE = "attendance.csv"
STUDENTS_FILE = "students.json"
SNAPSHOT_DIR = "snapshots"

# -------------------
# Configuration
# -------------------
CODE_VALIDITY_MINUTES = 5  # Code expires after 5 minutes

# Realistic college coordinates for simulation
CLASSROOM_LAT = 11.00314    # KMCT college latitude
CLASSROOM_LON = 76.20058    # KMCT college longitude
ALLOWED_RADIUS = 50         # Allowed radius in meters

# -------------------
# Distance calculation (Haversine formula)
# -------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    meters = R * c
    return meters

def check_location(student_lat, student_lon):
    dist = distance(CLASSROOM_LAT, CLASSROOM_LON, student_lat, student_lon)
    if dist <= ALLOWED_RADIUS:
        return True
    else:
        print(f"❌ You are too far from the classroom! Distance: {int(dist)} meters")
        return False

# -------------------
# Login check
# -------------------
def login_student(roll_no, password):
    try:
        with open(STUDENTS_FILE, "r") as f:
            students = json.load(f)
    except FileNotFoundError:
        print("❌ Student registry not found.")
        return None

    for student in students:
        if student["roll_no"] == roll_no and student["password"] == password:
            return student
    return None

# -------------------
# Validate student exists
# -------------------
def is_valid_student(roll_no, name):
    try:
        with open(STUDENTS_FILE, "r") as f:
            students = json.load(f)
    except FileNotFoundError:
        return False
    for student in students:
        if student["roll_no"] == roll_no and student["name"].lower() == name.lower():
            return True
    return False

# -------------------
# Capture snapshot
# -------------------
def capture_snapshot(roll_no):
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not access the camera.")
        return None

    print("📸 Capturing snapshot. Please look at the camera...")
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Snapshot capture failed.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{roll_no}_{timestamp}.jpg"
    path = os.path.join(SNAPSHOT_DIR, filename)
    cv2.imwrite(path, frame)
    print(f"✅ Snapshot saved: {filename}")
    return filename

# -------------------
# Mark attendance
# -------------------
def mark_attendance(roll_no, name, entered_code):
    if not is_valid_student(roll_no, name):
        print("❌ Invalid Roll No / Name combination.")
        return

    # Load active code
    try:
        with open(ACTIVE_FILE, "r") as f:
            active = json.load(f)
    except FileNotFoundError:
        print("❌ No active code found. Ask your teacher.")
        return

    active_code = active["code"]
    code_time_str = active["time"]
    code_time = datetime.strptime(code_time_str, "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()

    # Check code expiration
    if current_time > code_time + timedelta(minutes=CODE_VALIDITY_MINUTES):
        print("❌ Code has expired. Ask the teacher for a new one.")
        return

    if entered_code != active_code:
        print("❌ Wrong code. Try again.")
        return

    # Capture snapshot
    snapshot_file = capture_snapshot(roll_no)
    if snapshot_file is None:
        print("❌ Attendance not marked due to snapshot error.")
        return

    date_today = current_time.strftime("%Y-%m-%d")

    # Ensure attendance file exists
    if not os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Roll No", "Name", "Code", "Timestamp", "Snapshot"])

    # Check duplicates
    with open(ATTENDANCE_FILE, "r") as f:
        rows = list(csv.reader(f))
        for row in rows:
            if row and row[0] == date_today and row[1] == roll_no and row[3] == active_code:
                print("⚠️ Attendance already marked!")
                return

    # Append attendance
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_today, roll_no, name, active_code, timestamp, snapshot_file])

    print("✅ Attendance marked successfully!")

# -------------------
# Main
# -------------------
if __name__ == "__main__":
    print("🔑 Student Login")
    roll_no = input("Enter Roll No: ").strip()
    password = input("Enter Password: ").strip()

    student = login_student(roll_no, password)
    if not student:
        print("❌ Login failed. Check Roll No or Password.")
        exit()

    print(f"✅ Login successful! Welcome {student['name']}")

    # Simulated classroom location check
    print("🌍 Classroom Location Verification")
    try:
        student_lat = float(input("Enter your current latitude: ").strip())
        student_lon = float(input("Enter your current longitude: ").strip())
    except ValueError:
        print("❌ Invalid coordinates.")
        exit()

    if not check_location(student_lat, student_lon):
        exit()

    # Attendance code
    entered_code = input("Enter Attendance Code: ").strip()
    mark_attendance(student['roll_no'], student['name'], entered_code)
