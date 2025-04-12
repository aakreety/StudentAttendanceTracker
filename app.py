# gui/app.py

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Student Attendance Tracker")
    root.geometry("600x500")
    root.configure(bg="white")

    # Top Frame
    top_frame = tk.Frame(root, height=60, bg="#4CAF50")
    top_frame.pack(fill="x")

    title = tk.Label(top_frame, text="Student Attendance Tracker", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white")
    title.pack(pady=10)

    # Main Frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    # Student Form Section
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, width=30)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Phone:", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    phone_entry = tk.Entry(form_frame, width=30)
    phone_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Department:", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    dept_entry = tk.Entry(form_frame, width=30)
    dept_entry.grid(row=3, column=1, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
