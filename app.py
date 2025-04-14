import tkinter as tk
from tkinter import messagebox, ttk
import db  # db.py contains DB connection and query functions

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

def add_student(name, email, phone, department):
    if name and email and phone and department:
        result = db.insert_student(name, email, phone, department)
        if result:
            messagebox.showinfo("Success", "Student added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add student.")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def get_students():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT StudentID, Name FROM Students")
    students = cursor.fetchall()
    conn.close()
    return students

def get_courses():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseID, CourseName FROM Courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def display_attendance(course_id, date):
    records = db.fetch_attendance(course_id, date)
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)
    for record in records:
        attendance_tree.insert("", "end", values=(record[0], record[1]))

def main():
    global attendance_tree  # So it can be accessed in display_attendance

    root = tk.Tk()
    root.title("Student Attendance Tracker")
    root.geometry("800x700")
    root.configure(bg="white")

    top_frame = tk.Frame(root, height=60, bg="#4CAF50")
    top_frame.pack(fill="x")

    title = tk.Label(top_frame, text="Student Attendance Tracker", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white")
    title.pack(pady=10)

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    # === Attendance Section ===
    form_frame = tk.LabelFrame(main_frame, text="Mark Attendance", font=("Arial", 12), bg="white", padx=10, pady=10)
    form_frame.pack(pady=10, fill="x")

    students = get_students()
    student_names = [s[1] for s in students]
    student_id_map = {s[1]: s[0] for s in students}

    courses = get_courses()
    course_names = [c[1] for c in courses]
    course_id_map = {c[1]: c[0] for c in courses}

    tk.Label(form_frame, text="Student:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    student_dropdown = ttk.Combobox(form_frame, values=student_names, width=30)
    student_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Course:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    course_dropdown = ttk.Combobox(form_frame, values=course_names, width=30)
    course_dropdown.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    date_entry = tk.Entry(form_frame, width=30)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Status:", bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    status_dropdown = ttk.Combobox(form_frame, values=["Present", "Absent", "Late"], width=30)
    status_dropdown.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(form_frame, text="Mark Attendance", bg="#4CAF50", fg="white",
              command=lambda: mark_attendance(
                  student_id_map.get(student_dropdown.get()),
                  course_id_map.get(course_dropdown.get()),
                  date_entry.get(),
                  status_dropdown.get())).grid(row=4, column=1, pady=10)

    # === Attendance Viewer ===
    view_frame = tk.LabelFrame(main_frame, text="View Attendance", font=("Arial", 12), bg="white", padx=10, pady=10)
    view_frame.pack(pady=10, fill="x")

    tk.Label(view_frame, text="Course:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    course_view_dropdown = ttk.Combobox(view_frame, values=course_names, width=30)
    course_view_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(view_frame, text="Date (YYYY-MM-DD):", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    date_view_entry = tk.Entry(view_frame, width=30)
    date_view_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(view_frame, text="View Attendance", bg="#4CAF50", fg="white",
              command=lambda: display_attendance(
                  course_id_map.get(course_view_dropdown.get()),
                  date_view_entry.get())).grid(row=2, column=1, pady=10)

    columns = ("Student Name", "Status")
    attendance_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    attendance_tree.heading("Student Name", text="Student Name")
    attendance_tree.heading("Status", text="Status")
    attendance_tree.pack(pady=10, fill="x")

    # === Student Form ===
    student_frame = tk.LabelFrame(main_frame, text="Add New Student", font=("Arial", 12), bg="white", padx=10, pady=10)
    student_frame.pack(pady=10, fill="x")

    tk.Label(student_frame, text="Name:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(student_frame, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(student_frame, text="Email:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    email_entry = tk.Entry(student_frame, width=30)
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(student_frame, text="Phone:", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    phone_entry = tk.Entry(student_frame, width=30)
    phone_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(student_frame, text="Department:", bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    dept_entry = tk.Entry(student_frame, width=30)
    dept_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(student_frame, text="Add Student", bg="#4CAF50", fg="white",
              command=lambda: add_student(name_entry.get(), email_entry.get(), phone_entry.get(), dept_entry.get())).grid(row=4, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
