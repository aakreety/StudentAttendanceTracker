import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import db  # Assuming db.py contains the required DB connection and functions

def mark_attendance(student_id, course_id, date, status):
    """Handles marking the attendance for a student."""
    if student_id and course_id and date and status:
        result = db.insert_attendance(student_id, course_id, date, status)
        if result:
            messagebox.showinfo("Success", "Attendance marked successfully!")
        else:
            messagebox.showerror("Error", "Failed to mark attendance.")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def get_students():
    """Fetches all students from the database."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT StudentID, Name FROM Students")
    students = cursor.fetchall()
    conn.close()
    return students

def get_courses():
    """Fetches all courses from the database."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseID, CourseName FROM Courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def display_attendance(course_id, date):
    """Fetches attendance records and displays them in a Treeview."""
    records = db.fetch_attendance(course_id, date)
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)  # Clear previous entries
    
    for record in records:
        attendance_tree.insert("", "end", values=(record[0], record[1]))

def main():
    """Main Tkinter function to set up the UI."""
    root = tk.Tk()
    root.title("Student Attendance Tracker")
    root.geometry("800x600")
    root.configure(bg="white")

    # Top Frame
    top_frame = tk.Frame(root, height=60, bg="#4CAF50")
    top_frame.pack(fill="x")

    title = tk.Label(top_frame, text="Student Attendance Tracker", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white")
    title.pack(pady=10)

    # Main Frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    # Attendance Form Section
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(pady=20)

    # Student Dropdown
    tk.Label(form_frame, text="Select Student:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    students = get_students()
    student_names = [student[1] for student in students]
    student_id_map = {student[1]: student[0] for student in students}
    student_dropdown = ttk.Combobox(form_frame, values=student_names, width=30)
    student_dropdown.grid(row=0, column=1, padx=10, pady=5)

    # Course Dropdown
    tk.Label(form_frame, text="Select Course:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    courses = get_courses()
    course_names = [course[1] for course in courses]
    course_id_map = {course[1]: course[0] for course in courses}
    course_dropdown = ttk.Combobox(form_frame, values=course_names, width=30)
    course_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Date Entry
    tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    date_entry = tk.Entry(form_frame, width=30)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    # Attendance Status Dropdown
    tk.Label(form_frame, text="Attendance Status:", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    status_dropdown = ttk.Combobox(form_frame, values=["Present", "Absent", "Late"], width=30)
    status_dropdown.grid(row=3, column=1, padx=10, pady=5)

    # Submit Button
    submit_btn = tk.Button(main_frame, text="Mark Attendance", bg="#4CAF50", fg="white", font=("Arial", 12),
                           command=lambda: mark_attendance(
                               student_id_map.get(student_dropdown.get()),
                               course_id_map.get(course_dropdown.get()),
                               date_entry.get(),
                               status_dropdown.get()))
    submit_btn.pack(pady=10)

    # Attendance View Section
    view_frame = tk.Frame(main_frame, bg="white")
    view_frame.pack(pady=20)

    # Course Dropdown for Viewing Attendance
    tk.Label(view_frame, text="Select Course for Attendance:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    course_view_dropdown = ttk.Combobox(view_frame, values=course_names, width=30)
    course_view_dropdown.grid(row=0, column=1, padx=10, pady=5)

    # Date Entry for Viewing Attendance
    tk.Label(view_frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    date_view_entry = tk.Entry(view_frame, width=30)
    date_view_entry.grid(row=1, column=1, padx=10, pady=5)

    # View Attendance Button
    view_btn = tk.Button(view_frame, text="View Attendance", bg="#4CAF50", fg="white", font=("Arial", 12),
                         command=lambda: display_attendance(
                             course_id_map.get(course_view_dropdown.get()),
                             date_view_entry.get()))
    view_btn.grid(row=2, column=1, pady=10)

    # Treeview to display attendance
    columns = ("Student Name", "Status")
    attendance_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    attendance_tree.heading("Student Name", text="Student Name")
    attendance_tree.heading("Status", text="Status")
    attendance_tree.pack(fill="both", expand=True, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
