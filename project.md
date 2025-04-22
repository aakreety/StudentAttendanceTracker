# Student Attendance Tracker System

## GitHub Repository
[GitHub Link](https://github.com/aakreety/StudentAttendanceTracker)

## Demo Video
[YouTube Link] ( https://youtu.be/2ISd1dJqcO4 )

## Project Summary

This is a GUI-based **Student Attendance Tracker** system built using **Python (Tkinter)** and **SQLite**.

### Database Overview
- **Database**: SQLite (`attendance.db`)
- **Tables**:
  - `students`: Holds student ID and names.
  - `attendance`: Tracks attendance status (`Present`, `Absent`) for each student and date.
- Uses **foreign key-like logic** by storing `student_id` in attendance.
- Prevents duplicate attendance records using `UNIQUE(student_id, date)`.

### App Features
- Add, delete, and search students.
- Mark **Present** / **Absent** with auto or custom date.
- View all attendance records.
- Filter records by specific date.
- Summary report of total Present/Absent counts.
- Export attendance to CSV.
- Predefined SQL joins are shown via summary and filtering buttons.

### Technologies
- Python 3
- SQLite
- Tkinter
- ttk Treeview and modern custom styling
