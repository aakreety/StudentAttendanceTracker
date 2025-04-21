import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import date
import csv

# Theme colors
PRIMARY = "#3F51B5"
SECONDARY = "#7986CB"
BG_COLOR = "#E8EAF6"
TEXT_COLOR = "#212121"
BTN_COLOR = "#5C6BC0"
BTN_HOVER = "#303F9F"
HIGHLIGHT = "#C5CAE9"

def init_db():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            student_id INTEGER,
            date TEXT,
            status TEXT,
            UNIQUE(student_id, date)
        )
    """)
    conn.commit()
    conn.close()

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📘 Stylish Attendance Tracker")
        self.root.geometry("980x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.name_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.date_var = tk.StringVar()

        title = tk.Label(self.root, text="📘 Student Attendance Tracker", font=("Helvetica Neue", 26, "bold"),
                         bg=BG_COLOR, fg=PRIMARY)
        title.pack(pady=10)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="white", foreground=TEXT_COLOR, rowheight=25, fieldbackground="white")
        self.style.map("Treeview", background=[("selected", BTN_COLOR)])
        self.style.configure("Treeview.Heading", font=("Helvetica Neue", 10, "bold"), background=PRIMARY, foreground="white")
        
        self.setup_frame()
        self.refresh_tree()

    def setup_frame(self):
        frame = tk.Frame(self.root, bg=HIGHLIGHT, bd=1, relief=tk.RIDGE)
        frame.place(x=20, y=60, width=460, height=500)

        tk.Label(frame, text="Student Name:", bg=HIGHLIGHT, fg=TEXT_COLOR, font=("Helvetica Neue", 10)).place(x=10, y=20)
        tk.Entry(frame, textvariable=self.name_var, width=30).place(x=120, y=20)

        self.make_button(frame, "➕ Add", self.add_student, 120, 50)
        self.make_button(frame, "❌ Delete", self.delete_student, 190, 50)

        tk.Label(frame, text="🔍 Search:", bg=HIGHLIGHT, fg=TEXT_COLOR, font=("Helvetica Neue", 10)).place(x=10, y=90)
        tk.Entry(frame, textvariable=self.search_var, width=30).place(x=120, y=90)

        self.make_button(frame, "Search", self.search_student, 120, 120)
        self.make_button(frame, "Reset", self.refresh_tree, 190, 120)

        self.tree = ttk.Treeview(frame, columns=("Name",), show='headings', height=15)
        self.tree.heading("Name", text="Student Name")
        self.tree.column("Name", width=320)
        self.tree.place(x=10, y=160)

    def make_button(self, parent, text, command, x, y):
        btn = tk.Button(parent, text=text, command=command, bg=BTN_COLOR, fg="white",
                        activebackground=BTN_HOVER, activeforeground="white",
                        relief=tk.FLAT, font=("Helvetica Neue", 10, "bold"), width=10)
        btn.place(x=x, y=y)

    def action_frame(self):
        act_frame = tk.Frame(self.root, bg=HIGHLIGHT, bd=1, relief=tk.RIDGE)
        act_frame.place(x=500, y=60, width=460, height=500)

        self.make_button(act_frame, "✅ Present", lambda: self.mark_attendance("Present"), 30, 20)
        self.make_button(act_frame, "❌ Absent", lambda: self.mark_attendance("Absent"), 230, 20)
        self.make_button(act_frame, "📋 View All", self.view_attendance, 30, 60)

        tk.Label(act_frame, text="📅 Date (YYYY-MM-DD):", bg=HIGHLIGHT, fg=TEXT_COLOR, font=("Helvetica Neue", 10)).place(x=30, y=120)
        tk.Entry(act_frame, textvariable=self.date_var, width=30).place(x=30, y=150)
        self.make_button(act_frame, "🔎 Filter", self.filter_by_date, 270, 147)

        self.make_button(act_frame, "📊 Summary", self.view_summary, 30, 200)
        self.make_button(act_frame, "📤 Export", self.export_csv, 230, 200)

    def refresh_tree(self):
        self.action_frame()
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM students")
        for row in c.fetchall():
            self.tree.insert('', 'end', iid=row[0], values=(row[1],))
        conn.close()

    def add_student(self):
        name = self.name_var.get().strip()
        if name:
            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            c.execute("INSERT INTO students (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            self.name_var.set("")
            self.refresh_tree()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name.")

    def delete_student(self):
        selected = self.tree.focus()
        if selected:
            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE id=?", (selected,))
            c.execute("DELETE FROM attendance WHERE student_id=?", (selected,))
            conn.commit()
            conn.close()
            self.refresh_tree()
        else:
            messagebox.showwarning("Selection Error", "Please select a student to delete.")

    def search_student(self):
        query = self.search_var.get().strip().lower()
        if query:
            for row in self.tree.get_children():
                self.tree.delete(row)
            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            c.execute("SELECT id, name FROM students WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
            for row in c.fetchall():
                self.tree.insert('', 'end', iid=row[0], values=(row[1],))
            conn.close()

    def mark_attendance(self, status):
        selected = self.tree.focus()
        if selected:
            student_id = selected
            today = date.today().isoformat()
            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            # Check for duplicate entry
            c.execute("SELECT 1 FROM attendance WHERE student_id=? AND date=?", (student_id, today))
            if c.fetchone():
                messagebox.showwarning("Duplicate", "Attendance already marked for today.")
                conn.close()
                return
            c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (student_id, today, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Marked", f"Marked as {status}")
        else:
            messagebox.showwarning("Selection Error", "Please select a student.")

    def view_attendance(self):
        self.create_table_window("📋 All Attendance", """SELECT s.name, a.date, a.status
                                                           FROM attendance a
                                                           JOIN students s ON a.student_id = s.id""",
                                 ("Name", "Date", "Status"))

    def filter_by_date(self):
        date_input = self.date_var.get().strip()
        if not date_input:
            messagebox.showerror("Missing", "Please enter a date.")
            return
        self.create_table_window(f"Records on {date_input}", """SELECT s.name, a.status FROM attendance a
                                                                 JOIN students s ON a.student_id = s.id
                                                                 WHERE a.date = ?""",
                                 ("Name", "Status"), (date_input,))

    def view_summary(self):
        top = tk.Toplevel(self.root)
        top.title("📊 Attendance Summary")
        top.geometry("600x400")
        tree = ttk.Treeview(top, columns=("Name", "Present", "Absent"), show='headings')
        tree.heading("Name", text="Name")
        tree.heading("Present", text="Present")
        tree.heading("Absent", text="Absent")
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM students")
        students = c.fetchall()

        for student_id, name in students:
            c.execute("""SELECT status FROM attendance WHERE student_id=?""", (student_id,))
            records = c.fetchall()
            present_count = sum(1 for r in records if r[0] == 'Present')
            absent_count = sum(1 for r in records if r[0] == 'Absent')
            tree.insert('', 'end', values=(name, present_count, absent_count))
        conn.close()

    def create_table_window(self, title, query, columns, params=()):
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("650x400")
        tree = ttk.Treeview(top, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute(query, params)
        for row in c.fetchall():
            tree.insert('', 'end', values=row)
        conn.close()

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
        if file_path:
            conn = sqlite3.connect("attendance.db")
            c = conn.cursor()
            c.execute("""SELECT s.name, a.date, a.status FROM attendance a JOIN students s ON a.student_id = s.id""")
            data = c.fetchall()
            conn.close()

            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Status"])
                writer.writerows(data)
            messagebox.showinfo("Exported", "Data exported successfully!")

# MAIN
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
