-- STUDENTS table
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Phone TEXT,
    Major TEXT
    -- Functional Dependency: StudentID → Name, Email, Phone, Major
);

-- FACULTY table
CREATE TABLE IF NOT EXISTS Faculty (
    FacultyID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Department TEXT
    -- Functional Dependency: FacultyID → Name, Email, Department
);

-- COURSES table
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL,
    Department TEXT,
    FacultyID INTEGER,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
    -- Functional Dependency: CourseID → CourseName, Department, FacultyID
);

-- ATTENDANCE table
CREATE TABLE IF NOT EXISTS Attendance (
    AttendanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER,
    CourseID INTEGER,
    Date TEXT NOT NULL,
    Status TEXT CHECK(Status IN ('Present', 'Absent', 'Late')) NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
    -- Functional Dependency: AttendanceID → StudentID, CourseID, Date, Status
);
