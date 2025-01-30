import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class AdminPanel:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Admin Login", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.frame, text="Username:").pack()
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack()

        ttk.Label(self.frame, text="Password:").pack()
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.frame.bind("<Return>", self.login)
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", self.login)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.db.cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        admin = self.db.cursor.fetchone()

        if admin:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.admin_actions_window()
        else:
            messagebox.showerror("Login Failed", "No such username or password!")

    def admin_actions_window(self):
        self.frame.winfo_toplevel().withdraw()

        admin_window = tk.Toplevel(self.frame)
        admin_window.title("Admin Actions")
        admin_window.geometry("1280x720")

        ttk.Label(admin_window, text="---------- Teachers Functions ----------", font=("Arial", 16)).pack(pady=10)

        ttk.Button(admin_window, text="Show Teachers", command=self.show_teachers).pack(pady=6)
        ttk.Button(admin_window, text="Add Teacher", command=self.add_teacher).pack(pady=6)
        ttk.Button(admin_window, text="Remove Teacher", command=self.remove_teacher).pack(pady=6)

        ttk.Label(admin_window, text="---------- Courses Functions ----------", font=("Arial", 16)).pack(pady=10)

        ttk.Button(admin_window, text="Show Courses", command=self.show_courses).pack(pady=6)
        ttk.Button(admin_window, text="Add Course", command=self.add_course).pack(pady=6)
        ttk.Button(admin_window, text="Remove Course", command=self.remove_course).pack(pady=6)

        ttk.Label(admin_window, text="---------- Students Functions ----------", font=("Arial", 16)).pack(pady=10)

        ttk.Button(admin_window, text="Show Students", command=self.show_students).pack(pady=6)
        ttk.Button(admin_window, text="Add Student", command=self.add_student).pack(pady=6)
        ttk.Button(admin_window, text="Remove Student", command=self.remove_student).pack(pady=6)

        ttk.Label(admin_window, text="-------------------------------------------------", font=("Arial", 16)).pack(pady=10)

        ttk.Button(admin_window, text="Back", command=lambda: self.return_to_parent(admin_window)).pack(pady=5)

    def add_teacher(self):
        teacher_window = tk.Toplevel(self.frame)
        self.frame.winfo_toplevel().withdraw()

        teacher_window.title("Add Teacher")
        teacher_window.geometry("600x600")

        ttk.Label(teacher_window, text="Teacher Name:").pack(pady=5)
        name_entry = ttk.Entry(teacher_window)
        name_entry.pack(pady=5)

        ttk.Label(teacher_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(teacher_window)
        username_entry.pack(pady=5)

        ttk.Label(teacher_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(teacher_window, show="*")
        password_entry.pack(pady=5)

        ttk.Label(teacher_window, text="Assign Courses (Comma-separated Course IDs):").pack(pady=5)
        courses_entry = ttk.Entry(teacher_window)
        courses_entry.pack(pady=5)

        def save_teacher():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            course_ids = courses_entry.get().split(",")

            if not name or not username or not password:
                messagebox.showerror("Error", "All fields are needed!")
                return

            try:

                self.db.cursor.execute(
                    "INSERT INTO teachers (name, username, password) VALUES (?, ?, ?)",
                    (name, username, password)
                )
                teacher_id = self.db.cursor.lastrowid

                for course_id in course_ids:
                    course_id = course_id.strip()
                    if course_id.isdigit():
                        self.db.cursor.execute(
                            "UPDATE courses SET teacher_id = ? WHERE id = ?",
                            (teacher_id, course_id)
                        )

                self.db.conn.commit()
                messagebox.showinfo("Success", "Teacher added successfully!")
                teacher_window.destroy()
                self.frame.winfo_toplevel().deiconify()  # Return to parent window
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username must be unique!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        ttk.Button(teacher_window, text="Save", command=save_teacher).pack(pady=10)

        ttk.Button(teacher_window, text="Back", command=lambda: self.return_to_parent(teacher_window)).pack(pady=5)

    def add_course(self):
        course_window = tk.Toplevel(self.frame)
        self.frame.winfo_toplevel().withdraw()

        course_window.title("Add Course")
        course_window.geometry("600x600")

        ttk.Label(course_window, text="Course Name:").pack(pady=5)
        course_name_entry = ttk.Entry(course_window)
        course_name_entry.pack(pady=5)

        ttk.Label(course_window, text="Assign to Teacher (separate by commas IDs):").pack(pady=5)
        teacher_id_entry = ttk.Entry(course_window)
        teacher_id_entry.pack(pady=5)

        ttk.Label(course_window, text="Assign to Students (separate by commas IDs):").pack(pady=5)
        student_ids_entry = ttk.Entry(course_window)
        student_ids_entry.pack(pady=5)

        def save_course():
            course_name = course_name_entry.get()
            teacher_id = teacher_id_entry.get()
            student_ids = student_ids_entry.get().split(",")

            if not course_name or not teacher_id:
                messagebox.showerror("Error", "Both Course name and teacher ID are needed!")
                return

            try:
                self.db.cursor.execute(
                    "INSERT INTO courses (name, teacher_id) VALUES (?, ?)",
                    (course_name, teacher_id)
                )
                course_id = self.db.cursor.lastrowid

                for student_id in student_ids:
                    student_id = student_id.strip()
                    if student_id.isdigit():
                        self.db.cursor.execute(
                            "INSERT INTO grades (student_id, course_id) VALUES (?, ?)",
                            (student_id, course_id)
                        )

                self.db.conn.commit()
                messagebox.showinfo("Success", "Course added successfully with students assigned!")
                course_window.destroy()
                self.frame.winfo_toplevel().deiconify()  # Return to parent window
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Course name must be unique!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        save_button = ttk.Button(course_window, text="Save", command=save_course)
        save_button.pack(pady=10)

        ttk.Button(course_window, text="Back", command=lambda: self.return_to_parent(course_window)).pack(pady=5)

    def add_student(self):
        student_window = tk.Toplevel(self.frame)
        self.frame.winfo_toplevel().withdraw()

        student_window.title("Add Student")
        student_window.geometry("600x600")

        ttk.Label(student_window, text="Student Name:").pack(pady=5)
        name_entry = ttk.Entry(student_window)
        name_entry.pack(pady=5)

        ttk.Label(student_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(student_window)
        username_entry.pack(pady=5)

        ttk.Label(student_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(student_window, show="*")
        password_entry.pack(pady=5)

        ttk.Label(student_window, text="Assign Courses (separate using commas IDs):").pack(pady=5)
        courses_entry = ttk.Entry(student_window)
        courses_entry.pack(pady=5)

        def save_student():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            course_ids = courses_entry.get().split(",")

            if not name or not username or not password:
                messagebox.showerror("Error", "All fields are needed!")
                return

            try:
                self.db.cursor.execute(
                    "INSERT INTO students (name, username, password) VALUES (?, ?, ?)",
                    (name, username, password)
                )
                student_id = self.db.cursor.lastrowid

                for course_id in course_ids:
                    course_id = course_id.strip()
                    if course_id.isdigit():
                        self.db.cursor.execute(
                            "INSERT INTO grades (student_id, course_id) VALUES (?, ?)",
                            (student_id, course_id)
                        )

                self.db.conn.commit()
                messagebox.showinfo("Success", "Student added successfully!")
                student_window.destroمy()
                self.frame.winfo_toplevel().deiconify()  # Return to parent window
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username must be unique!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        ttk.Button(student_window, text="Save", command=save_student).pack(pady=10)
        ttk.Button(student_window, text="Back", command=lambda: self.return_to_parent(student_window)).pack(pady=5)

    def remove_teacher(self):
        def delete_teacher():
            teacher_id = teacher_id_entry.get()
            if not teacher_id.isdigit():
                messagebox.showerror("Error", "No such Teacher ID!")
                return

            self.db.cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Teacher removed successfully!")
            teacher_window.destroy()

        teacher_window = tk.Toplevel(self.frame)
        teacher_window.title("Remove Teacher")
        teacher_window.geometry("400x400")

        ttk.Label(teacher_window, text="Teacher ID:").pack(pady=10)
        teacher_id_entry = ttk.Entry(teacher_window)
        teacher_id_entry.pack(pady=5)

        ttk.Button(teacher_window, text="Delete Teacher", command=delete_teacher).pack(pady=10)
        ttk.Button(teacher_window, text="Back", command=lambda: self.return_to_parent(teacher_window)).pack(pady=5)

    def remove_course(self):
        def delete_course():
            course_id = course_id_entry.get()
            if not course_id.isdigit():
                messagebox.showerror("Error", "No such Course ID!")
                return

            self.db.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Course removed successfully!")
            course_window.destroy()

        course_window = tk.Toplevel(self.frame)
        course_window.title("Remove Course")
        course_window.geometry("400x400")

        ttk.Label(course_window, text="Course ID:").pack(pady=10)
        course_id_entry = ttk.Entry(course_window)
        course_id_entry.pack(pady=5)

        ttk.Button(course_window, text="Delete Course", command=delete_course).pack(pady=10)
        ttk.Button(course_window, text="Back", command=lambda: self.return_to_parent(course_window)).pack(pady=5)

    def remove_student(self):
        def delete_student():
            student_id = student_id_entry.get()
            if not student_id.isdigit():
                messagebox.showerror("Error", "No such Student ID!")
                return

            self.db.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Student removed successfully!")
            student_window.destroy()

        student_window = tk.Toplevel(self.frame)
        student_window.title("Remove Student")
        student_window.geometry("400x400")

        ttk.Label(student_window, text="Student ID:").pack(pady=10)
        student_id_entry = ttk.Entry(student_window)
        student_id_entry.pack(pady=5)

        ttk.Button(student_window, text="Delete Student", command=delete_student).pack(pady=10)
        ttk.Button(student_window, text="Back", command=lambda: self.return_to_parent(student_window)).pack(pady=5)

    def show_teachers(self):
        self.display_table("Teachers", "SELECT id, name FROM teachers", ["ID", "Name"])

    def show_courses(self):
        self.display_table("Courses", "SELECT id, name FROM courses", ["ID", "Name"])

    def show_students(self):
        self.display_table("Students", "SELECT id, name FROM students", ["ID", "Name"])

    def display_table(self, title, query, columns):
        table_window = tk.Toplevel(self.frame)
        table_window.title(title)
        table_window.geometry("1280x720")

        ttk.Label(table_window, text=f"{title} Table", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both")

        ttk.Button(table_window, text="Back", command=lambda: self.return_to_parent(table_window)).pack(pady=5)

    def return_to_parent(self, child_window):
        child_window.destroy()
        self.frame.winfo_toplevel().deiconify()