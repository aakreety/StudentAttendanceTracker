import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

# === Database Setup ===
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)''')
conn.commit()

class StylishAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Student Attendance Tracker")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # === Load and set background image ===
        self.bg_img = Image.open("background.jpg")  # Use a modern light theme image here
        self.bg_img = self.bg_img.resize((900, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Top Header ===
        self.header_frame = tk.Frame(self.root, bg="#003366", height=60)
        self.header_frame.pack(fill="x")
        self.title = tk.Label(self.header_frame, text="📚  Attendance Tracker", fg="white", bg="#003366",
                              font=("Helvetica", 18, "bold"))
        self.title.pack(pady=10, padx=20, anchor="w")

        # === Menu ===
        self.menu_frame = tk.Frame(self.root, bg="#f7f7f7", width=180)
        self.menu_frame.pack(side="left", fill="y")

        self.btn_style = {"font": ("Segoe UI", 10, "bold"), "bg": "#ffffff", "fg": "#003366", "bd": 0, "activebackground": "#e6f0ff"}

        tk.Button(self.menu_frame, text="➕ Add Student", command=self.add_student, **self.btn_style).pack(fill="x", pady=5, padx=10)
        tk.Button(self.menu_frame, text="✅ Mark Present", command=lambda: self.mark_attendance("Present"), **self.btn_style).pack(fill="x", pady=5, padx=10)
        tk.Button(self.menu_frame, text="❌ Mark Absent", command=lambda: self.mark_attendance("Absent"), **self.btn_style).pack(fill="x", pady=5, padx=10)
        tk.Button(self.menu_frame, text="📄 View Attendance", command=self.view_attendance, **self.btn_style).pack(fill="x", pady=5, padx=10)

        # === Student list ===
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.place(x=200, y=80, width=680, height=480)

        self.student_listbox = tk.Listbox(self.content_frame, width=40, height=20, font=("Segoe UI", 12))
        self.student_listbox.pack(side="left", padx=20, pady=20)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.student_listbox.yview)
        self.scrollbar.pack(side="left", fill="y", pady=20)
        self.student_listbox.config(yscrollcommand=self.scrollbar.set)

        self.load_students()

        # === Footer ===
        self.footer = tk.Label(self.root, text="© 2025 Akriti Neupane | All rights reserved", bg="#003366", fg="white", font=("Segoe UI", 9))
        self.footer.pack(side="bottom", fill="x")

    def load_students(self):
        self.student_listbox.delete(0, tk.END)
        cursor.execute("SELECT name FROM students ORDER BY name")
        for student in cursor.fetchall():
            self.student_listbox.insert(tk.END, student[0])

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter student name:")
        if name:
            try:
                cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
                conn.commit()
                self.load_students()
                messagebox.showinfo("Success", f"{name} added.")
            except sqlite3.IntegrityError:
                messagebox.showwarning("Duplicate", f"{name} already exists.")

    def mark_attendance(self, status):
        selected = self.student_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student.")
            return
        name = self.student_listbox.get(selected)
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT id FROM students WHERE name = ?", (name,))
        student_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, date))
        if cursor.fetchone():
            messagebox.showinfo("Already Marked", f"Attendance already marked today.")
        else:
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
            conn.commit()
            messagebox.showinfo("Marked", f"{status} marked for {name}.")

    def view_attendance(self):
        top = tk.Toplevel(self.root)
        top.title("📄 Attendance Records")
        top.geometry("600x400")

        tree = ttk.Treeview(top, columns=("name", "date", "status"), show="headings")
        tree.heading("name", text="Name")
        tree.heading("date", text="Date")
        tree.heading("status", text="Status")
        tree.pack(fill="both", expand=True)

        cursor.execute('''
            SELECT students.name, attendance.date, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
            ORDER BY attendance.date DESC
        ''')
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = StylishAttendanceApp(root)
    root.mainloop()
