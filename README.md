# Secure Attendance System – Phase 1

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Prototype-green)](https://github.com/liyan-nk/Attendance-System)

---

## Overview

The **Secure Attendance System (Phase 1)** is a Python-based tool to simplify classroom attendance. Teachers generate a unique code each session, and students mark their attendance by entering it. Snapshots are captured for verification, and all records are stored in CSV for easy tracking.

---

## Features

* **Teacher Code Generation:** Quickly generate unique codes for each class session.
* **Student Attendance Marking:** Enter code to mark presence.
* **Snapshot Verification:** Automatic photo capture for record verification.
* **CSV Records:** Attendance saved in `attendance.csv`.
* **Lightweight & File-Based:** Uses JSON to manage active and historical codes.

---

## Folder Structure

```
SECUREATTENDACEPHASE1/
│
├── teacher.py            # Teacher interface
├── student.py            # Student interface
├── view_attendance.py    # View attendance records
├── active_code.json      # Stores current active code
├── codes_history.json    # Stores previously generated codes
└── attendance.csv        # Attendance records
```

---

## Requirements

* Python 3.10+
* OpenCV (`cv2`) for snapshots
* Built-in Python libraries: `os`, `csv`, `json`, `datetime`

Install OpenCV:

```
pip install opencv-python
```

---

## Quick Usage

### Teacher

```
python teacher.py
```

1. Generate a unique code for the class hour.
2. Share the code with students.

---

### Student

```
python student.py
```

1. Enter **Roll Number**, **Name**, and **Class Code**.
2. Snapshot will be taken automatically.
3. Attendance recorded in `attendance.csv`.

---

### View Attendance

```
python view_attendance.py
```

* Displays all attendance records in a readable table.

---

## Notes

* Each code is **session-specific**.
* Snapshots help detect discrepancies.
* Students should avoid code sharing.

---

## Future Improvements (Phase 2)

* Location verification using GPS.
* Mobile/web app interface.
* Automatic face recognition for attendance.
* Push notifications for reminders.

---

## Author

**Liyan Nechikaden (LNK)** – Phase 1 prototype built to streamline classroom attendance.

---
