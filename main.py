from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Database setup ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "timetable.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Models ---
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)  # mon, tue, wed, thu, fri
    time_slot = db.Column(db.String(10), nullable=False)  # 9, 10, 11, 2, 3
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("day", "time_slot", name="unique_day_time"),
    )

# --- Create DB if not exists ---
with app.app_context():
    db.create_all()

    # Seed sample data if empty
    if Timetable.query.count() == 0:
        sample_data = [
           # Monday
    {"day": "mon", "time_slot": "9", "subject": "Math", "teacher": "Prof. Smith"},
    {"day": "mon", "time_slot": "10", "subject": "English", "teacher": "Dr. Johnson"},
    {"day": "mon", "time_slot": "11", "subject": "Science", "teacher": "Dr. Brown"},
    {"day": "mon", "time_slot": "2", "subject": "Computer", "teacher": "Mr. Davis"},
    {"day": "mon", "time_slot": "3", "subject": "Sports", "teacher": "Coach Wilson"},
    
    # Tuesday
    {"day": "tue", "time_slot": "9", "subject": "History", "teacher": "Ms. Anderson"},
    {"day": "tue", "time_slot": "10", "subject": "Math", "teacher": "Prof. Smith"},
    {"day": "tue", "time_slot": "11", "subject": "English", "teacher": "Dr. Johnson"},
    {"day": "tue", "time_slot": "2", "subject": "Science", "teacher": "Dr. Brown"},
    {"day": "tue", "time_slot": "3", "subject": "Library", "teacher": "Mrs. Clark"},

    # Wednesday
    {"day": "wed", "time_slot": "9", "subject": "Computer", "teacher": "Mr. Davis"},
    {"day": "wed", "time_slot": "10", "subject": "Math", "teacher": "Prof. Smith"},
    {"day": "wed", "time_slot": "11", "subject": "English", "teacher": "Dr. Johnson"},
    {"day": "wed", "time_slot": "2", "subject": "Science", "teacher": "Dr. Brown"},
    {"day": "wed", "time_slot": "3", "subject": "Sports", "teacher": "Coach Wilson"},

    # Thursday
    {"day": "thu", "time_slot": "9", "subject": "English", "teacher": "Dr. Johnson"},
    {"day": "thu", "time_slot": "10", "subject": "History", "teacher": "Ms. Anderson"},
    {"day": "thu", "time_slot": "11", "subject": "Science", "teacher": "Dr. Brown"},
    {"day": "thu", "time_slot": "2", "subject": "Computer", "teacher": "Mr. Davis"},
    {"day": "thu", "time_slot": "3", "subject": "Arts", "teacher": "Ms. Taylor"},

    # Friday
    {"day": "fri", "time_slot": "9", "subject": "Math", "teacher": "Prof. Smith"},
    {"day": "fri", "time_slot": "10", "subject": "English", "teacher": "Dr. Johnson"},
    {"day": "fri", "time_slot": "11", "subject": "Science", "teacher": "Dr. Brown"},
    {"day": "fri", "time_slot": "2", "subject": "Computer", "teacher": "Mr. Davis"},
    {"day": "fri", "time_slot": "3", "subject": "Sports", "teacher": "Coach Wilson"},
]
        for row in sample_data:
            db.session.add(Timetable(**row))
        db.session.commit()

# --- Routes ---
@app.route("/")
def index():
    return render_template("admin.html")

@app.route("/api/timetable")
def get_timetable():
    records = Timetable.query.all()
    data = [
        {"day": r.day, "time": r.time_slot, "subject": r.subject, "teacher": r.teacher}
        for r in records
    ]
    return jsonify(data)

@app.route("/api/update", methods=["POST"])
def update_timetable():
    data = request.get_json()
    day = data.get("day")
    time_slot = data.get("time")
    teacher = data.get("teacher")

    record = Timetable.query.filter_by(day=day, time_slot=time_slot).first()
    if record:
        record.teacher = teacher
        db.session.commit()
        return jsonify({"status": "success", "message": f"Updated {day} {time_slot}"})
    return jsonify({"status": "error", "message": "Record not found"}), 404

# --- New Routes ---
@app.route("/login")
def login():
    # This will render login.html (you need to create it in templates/)
    return render_template("login.html")

@app.route("/student")
def student_page():
    # Fetch timetable for students (you can filter if needed)
    records = Timetable.query.all()
    timetable = [
        {"day": r.day, "time": r.time_slot, "subject": r.subject, "teacher": r.teacher}
        for r in records
    ]
    # student.html can loop through timetable
    return render_template("student.html", timetable=timetable)

if __name__ == "__main__":
    app.run(debug=True)
