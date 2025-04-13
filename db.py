import sqlite3

def connect():
    return sqlite3.connect(r"C:\Users\aakri\OneDrive\Desktop\SQL Files\student_attendance.db")

def insert_student(name, email, phone, department):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "INSERT INTO Students (Name, Email, Phone, Major) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (name, email, phone, department))
        conn.commit()
        conn.close()
        print("✅ Student inserted successfully.")
        return True
    except sqlite3.Error as err:
        print(" DB Error:", err)
        return False
