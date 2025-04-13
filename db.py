import sqlite3

# Function to connect to the database
def connect():
    return sqlite3.connect(r'C:\Users\aakri\OneDrive\Desktop\SQL Files\student_attendance.db')

# Function to insert a student
def insert_student(name, email, phone, department):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO Students (Name, Email, Phone, Major)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (name, email, phone, department))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

# Function to insert attendance
def insert_attendance(student_id, course_id, date, status):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO Attendance (StudentID, CourseID, Date, Status)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (student_id, course_id, date, status))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

# Function to fetch attendance for a specific course and date
def fetch_attendance(course_id, date):
    """Fetch attendance records for a specific course and date."""
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
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to get all courses
def fetch_courses():
    """Fetch all courses from the database."""
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "SELECT * FROM Courses"
        cursor.execute(query)
        courses = cursor.fetchall()
        conn.close()
        return courses
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to get students enrolled in a specific course
def fetch_students_in_course(course_id):
    """Fetch all students in a specific course."""
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        SELECT Students.Name
        FROM Attendance
        JOIN Students ON Attendance.StudentID = Students.StudentID
        WHERE Attendance.CourseID = ?
        """
        cursor.execute(query, (course_id,))
        students = cursor.fetchall()
        conn.close()
        return students
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
