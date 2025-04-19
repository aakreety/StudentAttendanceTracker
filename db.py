def create_database():
    conn = sqlite3.connect('student_attendance.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist (optional, for fresh setup)
    cursor.execute('DROP TABLE IF EXISTS Students')
    cursor.execute('DROP TABLE IF EXISTS Courses')
    cursor.execute('DROP TABLE IF EXISTS Attendance')
    
    # Create new tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL,
        major TEXT NOT NULL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attendance (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        status TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(id),
        FOREIGN KEY (course_id) REFERENCES Courses(id)
    )''')
    
    conn.commit()
    conn.close()
