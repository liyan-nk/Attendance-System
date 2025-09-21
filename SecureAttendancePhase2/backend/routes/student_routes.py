# routes/student_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.student import Student
from models.attendance import Attendance
from utils.code_utils import validate_code
from utils.gps import check_distance
import cv2
import os
import datetime

student_routes = Blueprint('student_routes', __name__)

HAAR_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

@student_routes.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    student_roll = data.get("roll_no")
    class_code = data.get("class_code")
    gps_lat = data.get("gps_lat")
    gps_lon = data.get("gps_lon")
    snapshot_b64 = data.get("snapshot")  # Base64 encoded image

    # Validate student
    student = Student.query.filter_by(roll_no=student_roll).first()
    if not student:
        return jsonify({"status": "error", "msg": "Student not found"}), 404

    # Validate attendance code
    if not validate_code(class_code):
        return jsonify({"status": "error", "msg": "Invalid or expired code"}), 400

    # Validate GPS
    if not check_distance(gps_lat, gps_lon):
        return jsonify({"status": "error", "msg": "Not within classroom radius"}), 400

    # Decode snapshot and save temporarily
    import base64
    import numpy as np

    snapshot_data = base64.b64decode(snapshot_b64)
    np_arr = np.frombuffer(snapshot_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Check for face
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return jsonify({"status": "error", "msg": "No face detected in snapshot"}), 400

    # Save snapshot
    snapshot_folder = "snapshots"
    os.makedirs(snapshot_folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_path = os.path.join(snapshot_folder, f"{student_roll}_{timestamp}.jpg")
    cv2.imwrite(snapshot_path, img)

    # Mark attendance
    attendance = Attendance(
        student_id=student.id,
        teacher_id=1,  # Temporary, can replace with actual teacher_id
        class_code=class_code,
        gps_lat=gps_lat,
        gps_lon=gps_lon,
        snapshot_file=snapshot_path
    )
    db.session.add(attendance)
    db.session.commit()

    return jsonify({"status": "success", "msg": "Attendance marked"})
