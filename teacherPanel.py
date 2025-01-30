import tkinter as tk
from tkinter import messagebox, ttk


class TeacherPanel:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Teacher Panel", font=("Arial", 16)).pack(pady=10)

        login_frame = ttk.Frame(self.frame)
        login_frame.pack(pady=10)

        ttk.Label(login_frame, text="Username:").pack()
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.pack()

        ttk.Label(login_frame, text="Password:").pack()
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", self.login)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.db.cursor.execute("SELECT * FROM teachers WHERE username = ? AND password = ?", (username, password))
        teacher = self.db.cursor.fetchone()

        if teacher:
            messagebox.showinfo("Login Successful", f"Welcome, {teacher[1]}!")
            self.teacher_id = teacher[0]
            self.teacher_actions_window()
        else:
            messagebox.showerror("Login Failed", "No such username or password!")

    def teacher_actions_window(self):
        teacher_window = tk.Toplevel(self.frame)
        teacher_window.title("Teacher Actions")
        teacher_window.geometry("1280x720")

        ttk.Label(teacher_window, text="Courses", font=("Arial", 16)).pack(pady=10)

        self.course_tree = ttk.Treeview(teacher_window, columns=("ID", "Course Name"), show="headings")
        self.course_tree.heading("ID", text="Course ID")
        self.course_tree.heading("Course Name", text="Course Name")

        self.course_tree.column("ID", anchor="center", width=200)
        self.course_tree.column("Course Name", anchor="center", width=300)

        self.db.cursor.execute("SELECT id, name FROM courses WHERE teacher_id = ?", (self.teacher_id,))
        courses = self.db.cursor.fetchall()

        for course in courses:
            self.course_tree.insert("", "end", values=(course[0], course[1]))

        self.course_tree.pack(pady=10, expand=True, fill="both")

        ttk.Button(teacher_window, text="Show Students",
                   command=self.show_students).pack(pady=10)

    def show_students(self):
        selected_item = self.course_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a course first!")
            return

        try:
            course_id, course_name = self.course_tree.item(selected_item[0], "values")
            print(f"Selected Course ID: {course_id}, Course Name: {course_name}")
        except IndexError:
            messagebox.showerror("Error", "Unable to retrieve the selected course. Please try again.")
            return

        self.db.cursor.execute("SELECT * FROM grades WHERE course_id = ?", (course_id,))
        grades = self.db.cursor.fetchall()
        print(f"Enrollments for Course ID {course_id}: {grades}")

        if not grades:
            messagebox.showinfo("No Students", "No students are enrolled in this course.")
            return

        self.db.cursor.execute("""
            SELECT s.id, s.name
            FROM students s
            INNER JOIN grades g ON s.id = g.student_id
            WHERE g.course_id = ?
        """, (course_id,))
        students = self.db.cursor.fetchall()
        print(f"Students for Course ID {course_id}: {students}")

        if not students:
            messagebox.showinfo("No Students", "No students are enrolled in this course.")
            return

        student_window = tk.Toplevel(self.frame)
        student_window.title(f"Students in {course_name}")
        student_window.geometry("800x600")

        ttk.Label(student_window, text=f"Course: {course_name}", font=("Arial", 16)).pack(pady=10)

        student_tree = ttk.Treeview(student_window, columns=("Student ID", "Student Name"), show="headings")
        student_tree.heading("Student ID", text="Student ID")
        student_tree.heading("Student Name", text="Student Name")

        student_tree.column("Student ID", anchor="center", width=200)
        student_tree.column("Student Name", anchor="center", width=300)

        for student in students:
            student_tree.insert("", "end", values=(student[0], student[1]))

        student_tree.pack(pady=10, expand=True, fill="both")
        ttk.Button(student_window, text="Close", command=student_window.destroy).pack(pady=10)
