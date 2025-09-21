import csv

ATTENDANCE_FILE = "attendance.csv"

def view_attendance():
    try:
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print("\t".join(row))
    except FileNotFoundError:
        print("❌ No attendance records found.")


if __name__ == "__main__":
    print("📌 Attendance Records:\n")
    view_attendance()
