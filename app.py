import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db
from tkcalendar import Calendar  # Import the Calendar module

# Define theme colors
BG_COLOR = "#f0f4f7"
HEADER_COLOR = "#007acc"
BUTTON_COLOR = "#00b894"
TEXT_COLOR = "#2d3436"
FONT = ("Segoe UI", 11)

root = tk.Tk()
root.title("Student Attendance Tracker")
root.geometry("800x600")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# -------------------------- Add Student Tab --------------------------
add_tab = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(add_tab, text="Add Student")

header = tk.Label(add_tab, text="Add New Student", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 14, "bold"))
header.pack(pady=10, fill="x")

form_frame = tk.Frame(add_tab, bg=BG_COLOR)
form_frame.pack(pady=20)

labels = ["Name", "Email", "Phone", "Department"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=i, column=0, padx=10, pady=10, sticky="w")
    entry = tk.Entry(form_frame, font=FONT, width=40)
    entry.grid(row=i, column=1, padx=10, pady=10)
    entries[label.lower()] = entry

def submit_student():
    name = entries["name"].get().strip()
    email = entries["email"].get().strip()
    phone = entries["phone"].get().strip()
    dept = entries["department"].get().strip()

    if not all([name, email, phone, dept]):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    success = db.insert_student(name, email, phone, dept)
    if success:
        messagebox.showinfo("Success", "Student added successfully.")
        for entry in entries.values():
            entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Failed to add student.")

submit_btn = tk.Button(add_tab, text="Add Student", bg=BUTTON_COLOR, fg="white", font=FONT, command=submit_student)
submit_btn.pack(pady=10)

# -------------------------- Record Attendance Tab --------------------------
attendance_tab = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(attendance_tab, text="Record Attendance")

att_header = tk.Label(attendance_tab, text="Record Attendance", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 14, "bold"))
att_header.pack(pady=10, fill="x")

att_form = tk.Frame(attendance_tab, bg=BG_COLOR)
att_form.pack(pady=20)

students = db.fetch_all_students()
courses = db.fetch_courses()

student_ids = {s[1]: s[0] for s in students}
course_ids = {c[1]: c[0] for c in courses}

student_names = list(student_ids.keys())
course_names = list(course_ids.keys())

tk.Label(att_form, text="Student", font=FONT, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
student_var = tk.StringVar()
student_dropdown = ttk.Combobox(att_form, textvariable=student_var, values=student_names, font=FONT, width=30)
student_dropdown.grid(row=0, column=1, padx=10, pady=10)

tk.Label(att_form, text="Course", font=FONT, bg=BG_COLOR).grid(row=1, column=0, padx=10, pady=10)
course_var = tk.StringVar()
course_dropdown = ttk.Combobox(att_form, textvariable=course_var, values=course_names, font=FONT, width=30)
course_dropdown.grid(row=1, column=1, padx=10, pady=10)

tk.Label(att_form, text="Status", font=FONT, bg=BG_COLOR).grid(row=2, column=0, padx=10, pady=10)
status_var = tk.StringVar()
status_dropdown = ttk.Combobox(att_form, textvariable=status_var, values=["Present", "Absent"], font=FONT, width=30)
status_dropdown.grid(row=2, column=1, padx=10, pady=10)

def submit_attendance():
    student = student_var.get()
    course = course_var.get()
    status = status_var.get()

    if not all([student, course, status]):
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    success = db.insert_attendance(student_ids[student], course_ids[course], status)
    if success:
        messagebox.showinfo("Success", "Attendance recorded.")
    else:
        messagebox.showerror("Error", "Failed to record attendance.")

att_btn = tk.Button(attendance_tab, text="Record Attendance", bg=BUTTON_COLOR, fg="white", font=FONT, command=submit_attendance)
att_btn.pack(pady=10)

# -------------------------- View Attendance Tab --------------------------
view_tab = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(view_tab, text="View Attendance")

view_header = tk.Label(view_tab, text="View Attendance Records", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 14, "bold"))
view_header.pack(pady=10, fill="x")

view_frame = tk.Frame(view_tab, bg=BG_COLOR)
view_frame.pack(pady=20)

tk.Label(view_frame, text="Course", font=FONT, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
course_view_var = tk.StringVar()
course_dropdown = ttk.Combobox(view_frame, textvariable=course_view_var, values=course_names, font=FONT, width=30)
course_dropdown.grid(row=0, column=1, padx=10, pady=10)

# Calendar widget for date selection
tk.Label(view_frame, text="Select Date", font=FONT, bg=BG_COLOR).grid(row=1, column=0, padx=10, pady=10)
cal = Calendar(view_frame, selectmode="day", date_pattern="yyyy-mm-dd", font=FONT)
cal.grid(row=1, column=1, padx=10, pady=10)

def view_attendance():
    course = course_view_var.get()
    date = cal.get_date()  # Get the selected date from the calendar

    if not course or not date:
        messagebox.showerror("Input Error", "Please provide course and date.")
        return

    records = db.fetch_attendance(course_ids[course], date)
    for row in tree.get_children():
        tree.delete(row)
    for record in records:
        tree.insert("", tk.END, values=record)

tree = ttk.Treeview(view_tab, columns=("Name", "Status"), show="headings")
tree.heading("Name", text="Student Name")
tree.heading("Status", text="Status")
tree.pack(pady=20)

view_btn = tk.Button(view_tab, text="Fetch Records", bg=BUTTON_COLOR, fg="white", font=FONT, command=view_attendance)
view_btn.pack()

root.mainloop()
