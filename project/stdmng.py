
from tkinter import ttk4
from database import Database
from teacherPanel import TeacherPanel
from studentPanel import StudentPanel
from adminPanel import AdminPanel

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System (SMS)")
        self.root.geometry("1280x720")
        self.db = Database()

        self.tab_control = ttk.Notebook(self.root)

        self.admin_tab = AdminPanel(self.tab_control, self.db)
        self.teacher_tab = TeacherPanel(self.tab_control, self.db)
        self.student_tab = StudentPanel(self.tab_control, self.db)

        self.tab_control.add(self.admin_tab.frame, text="Admin")
        self.tab_control.add(self.teacher_tab.frame, text="Teacher")
        self.tab_control.add(self.student_tab.frame, text="Student")

        self.tab_control.pack(expand=1, fill="both")

        self.exit_button = ttk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

    def exit_program(self):
        self.db.close()
        self.root.quit()