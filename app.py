# gui/app.py

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Student Attendance Tracker")
    root.geometry("600x400")
     # Top Frame
    top_frame = tk.Frame(root, height=60, bg="#4CAF50")
    top_frame.pack(fill="x")

    title = tk.Label(top_frame, text="Student Attendance Tracker", font=("Helvetica", 18), bg="#4CAF50", fg="white")
    title.pack(pady=10)

    # Main Frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
