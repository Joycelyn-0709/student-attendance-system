from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Connect to database
def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables
def create_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_no TEXT UNIQUE NOT NULL,
            department TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            attendance_date TEXT,
            status TEXT,
            FOREIGN KEY (student_id)
            REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        register_no = request.form["register_no"]
        department = request.form["department"]

        conn = get_db()

        conn.execute(
            "INSERT INTO students (name, register_no, department) VALUES (?, ?, ?)",
            (name, register_no, department)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_student.html")


# Mark attendance
@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    if request.method == "POST":

        student_id = request.form["student_id"]
        subject = request.form["subject"]
        date = request.form["date"]
        status = request.form["status"]

        conn.execute(
            """INSERT INTO attendance
            (student_id, subject, attendance_date, status)
            VALUES (?, ?, ?, ?)""",
            (student_id, subject, date, status)
        )

        conn.commit()
        conn.close()

        return redirect("/view_attendance")

    conn.close()

    return render_template(
        "mark_attendance.html",
        students=students
    )


# View attendance
@app.route("/view_attendance")
def view_attendance():

    conn = get_db()

    records = conn.execute(
        """SELECT
        students.register_no,
        students.name,
        attendance.subject,
        attendance.attendance_date,
        attendance.status

        FROM attendance

        JOIN students
        ON attendance.student_id = students.student_id"""
    ).fetchall()

    conn.close()

    return render_template(
        "view_attendance.html",
        records=records
    )


# Start application
if __name__ == "__main__":

    create_database()

    app.run(debug=True)