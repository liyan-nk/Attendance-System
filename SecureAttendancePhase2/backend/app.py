# app.py
from flask import Flask
from database import db
from routes.student_routes import student_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///attendance.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(student_routes, url_prefix="/student")

# Create DB tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
