import sqlite3
from datetime import datetime

# Connect to DB
def connect():
    return sqlite3.connect(r"C:\Users\aakri\OneDrive\Desktop\SQL Files\student_attendance.db")

# Insert student
def insert_student(name, email, phone, department):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (Name, Email, Phone, Major) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, department))
        conn.commit()
        conn.close()
        print("✅ Student inserted successfully.")
        return True
    except sqlite3.Error as e:
        print("Database Error:", e)
        return False

# Insert attendance (date auto)
def insert_attendance(student_id, course_id, status):
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Attendance (StudentID, CourseID, Date, Status) VALUES (?, ?, ?, ?)",
                       (student_id, course_id, date, status))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Database Error:", e)
        return False

# Fetch attendance by course and date
def fetch_attendance(course_id, date):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        SELECT Students.Name, Attendance.Status
        FROM Attendance
        JOIN Students ON Attendance.StudentID = Students.StudentID
        WHERE Attendance.CourseID = ? AND Attendance.Date = ?
        """
        cursor.execute(query, (course_id, date))
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print("Error:", e)
        return []

# Get all courses
def fetch_courses():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Courses")
        courses = cursor.fetchall()
        conn.close()
        return courses
    except sqlite3.Error as e:
        print("Error:", e)
        return []

# Get all students
def fetch_all_students():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT StudentID, Name FROM Students")
        students = cursor.fetchall()
        conn.close()
        return students
    except sqlite3.Error as e:
        print("Error:", e)
        return []
