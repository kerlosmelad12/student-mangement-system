import tkinter as tk
from tkinter import messagebox, ttk


class StudentPanel:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Student Login", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.frame, text="Username:").pack()
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack()

        ttk.Label(self.frame, text="Password:").pack()
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", self.login)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.db.cursor.execute("SELECT * FROM students WHERE username = ? AND password = ?", (username, password))
        student = self.db.cursor.fetchone()

        if student:
            messagebox.showinfo("Login Successful", f"Welcome, {student[1]}!")
            self.show_student_dashboard(student)
        else:
            messagebox.showerror("Login Failed", "No such username or password!")

    def show_student_dashboard(self, student):
        dashboard_window = tk.Toplevel(self.frame)
        dashboard_window.title("Student Dashboard")
        dashboard_window.geometry("1280x720")

        ttk.Label(dashboard_window, text=f"Student: {student[1]} (ID: {student[0]})", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(dashboard_window, columns=("ID", "Name", "Teacher"), show="headings")
        tree.heading("ID", text="Course ID")
        tree.heading("Name", text="Course Name")
        tree.heading("Teacher", text="Teacher Name")

        tree.column("ID", anchor="center")
        tree.column("Name", anchor="center")
        tree.column("Teacher", anchor="center")

        self.db.cursor.execute("""
            SELECT c.id, c.name, t.name 
            FROM courses c 
            LEFT JOIN teachers t ON c.teacher_id = t.id 
            WHERE c.id IN (SELECT course_id FROM grades WHERE student_id = ?)
        """, (student[0],))
        courses = self.db.cursor.fetchall()

        for course in courses:
            tree.insert("", "end", values=course)

        tree.pack(expand=True, fill="both")

        ttk.Button(dashboard_window, text="Logout", command=dashboard_window.destroy).pack(pady=10)