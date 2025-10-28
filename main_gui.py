# import tkinter so got GUI now
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox #for showing pop-up


#same database from v1.0.0
import database


#main GUI class
class AttendanceApp(tkinter.Tk):

    #runs once when program starts
    def __init__(self):
        #runs parent class (tk.Tk) init method also the window
        super().__init__()

        #app setup
        self.title("CheckMeIN Attendance Management System")
        self.geometry("600x400") #default window size

        #styleee
        self.style = ttk.Style(self)
        self.style.theme_use('clam') #use clam theme, maybe nicer i guess

        #load data from database.py
        print("Loading data from database... This may take a century...")
        self.users, self.students, self.lecturers = database.load_users()
        self.classes, self.attendance = database.load_classes_and_attendance()
        print("Yes! Data loaded successfully! Congratulations!")

        #store current user info
        self.current_user = None

        #create container for pages
        #we will have multiple pages in the app
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #dict to hold pages
        self.frames = {}

        #create/add page to frames dict
        for F in (LoginPage, AdminPage, LecturerPage, StudentPage):
            #create instance of page
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            #place frame in grid btw stack on top of each other
            frame.grid(row=0, column=0, sticky="nsew")

        #show login page first
        self.show_frame(LoginPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        #line that bring the frame to the front
        frame.tkraise()
        # Call on_show method if it exists
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def login(self,username, password):
        #check if username exists
        if username in self.users and self.users[username]['password'] == password:
            #check password
            self.current_user = username
            role = self.users[username]['role']

            #show menu based on role
            if role == 'admin':
                self.show_frame(AdminPage)
            elif role == 'lecturer':
                self.show_frame(LecturerPage)
            elif role == 'student':
                self.show_frame(StudentPage)

            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def logout(self):
        #log out current user and return to login page
        self.current_user = None
        self.show_frame(LoginPage)

#login page
class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        #give access to all methods and attributes of AttendanceApp
        self.controller = controller

        #login layout
        login_frame = ttk.Frame(self, padding="20")
        login_frame.pack(expand=True) #this for centers the frame

        #widgets
        title = ttk.Label(login_frame, text="Login", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        #username box
        user_label = ttk.Label(login_frame, text="Username")
        user_label.pack(pady=5)
        self.user_entry = ttk.Entry(login_frame, width=30)
        self.user_entry.pack(pady=5, padx=20)

        #password box
        pass_label = ttk.Label(login_frame, text="Password")
        pass_label.pack(pady=5)
        self.pass_entry = ttk.Entry(login_frame, width=30, show="*")
        self.pass_entry.pack(pady=5, padx=20)

        #bind enter key to login
        self.pass_entry.bind("<Return>", self.on_login_click)

        #Login button
        login_button = ttk.Button(
            login_frame,
            text="Login",
            command=self.on_login_click
        )
        login_button.pack(pady=20, padx=10)

    def on_login_click(self, event=None): #event=None to allow both button click and enter key
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        #call login method from controller (AttendanceApp)
        self.controller.login(username, password)

        #clear password field after login attempt
        self.pass_entry.delete(0, 'end')


#admin page
class AdminPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #layout
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both") #centers the frame

        title = ttk.Label(main_frame, text="Admin Menu", font=("Arial", 20, "bold"))
        title.pack(pady=10, anchor="w")

        #widget
        #use "notebook" for tabs view for different admin functions
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill="both", pady=10)

        #tab 1: add student
        student_tab = ttk.Frame(notebook, padding="10")
        notebook.add(student_tab, text="Add Students")

        ttk.Label(student_tab, text="New Student Username").pack(pady=5, anchor="w")
        self.student_user_entry = ttk.Entry(student_tab, width=40)
        self.student_user_entry.pack(pady=5, fill="x")

        ttk.Label(student_tab, text="New Student Password").pack(pady=5, anchor="w")
        self.student_pass_entry = ttk.Entry(student_tab, width=40)
        self.student_pass_entry.pack(pady=5, fill="x")

        add_student_btn = ttk.Button(student_tab, text="Add Student", command=self.add_student)
        add_student_btn.pack(pady=10)

        #tab 2: add lecturer
        lecturer_tab = ttk.Frame(notebook, padding="10")
        notebook.add(lecturer_tab, text="Add Lecturer")

        ttk.Label(lecturer_tab, text="Lecturer Username").pack(pady=5, anchor="w")
        self.lecturer_user_entry = ttk.Entry(lecturer_tab, width=40)
        self.lecturer_user_entry.pack(pady=5, fill="x")

        ttk.Label(lecturer_tab, text="Lecturer Password").pack(pady=5, anchor="w")
        self.lecturer_pass_entry = ttk.Entry(lecturer_tab, width=40, show="*")
        self.lecturer_pass_entry.pack(pady=5, fill="x")

        add_lecturer_btn = ttk.Button(lecturer_tab, text="Add Lecturer", command=self.add_lecturer)
        add_lecturer_btn.pack(pady=10)

        #tab 3: add class
        class_tab = ttk.Frame(notebook, padding="10")
        notebook.add(class_tab, text="Add Class")

        ttk.Label(class_tab, text="New Class Name (e.g., 'SWE3001')").pack(pady=5, anchor="w")
        self.class_name_entry = ttk.Entry(class_tab, width=40)
        self.class_name_entry.pack(pady=5, fill="x")

        add_class_btn = ttk.Button(class_tab, text="Add Class", command=self.add_class)
        add_class_btn.pack(pady=10)

        #tab 4: logout button (button)
        logout_button = ttk.Button(main_frame, text="Logout", command=self.controller.logout)
        logout_button.pack(pady=10, anchor="e", side="bottom")

    #admin functions
    def add_student(self):
        username = self.student_user_entry.get()
        password = self.student_pass_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

        elif username in self.controller.users:
            messagebox.showerror("Error", "This username already exists.")
        else:
            #update data to memory
            self.controller.users[username] = {'password': password, 'role': 'student'}
            self.controller.students.append(username)
            #save to database (.csv file)
            database.save_users(self.controller.users)
            #show success message
            messagebox.showinfo("Success", f"Student '{username}' added successfully.")
            self.student_user_entry.delete(0, 'end')
            self.student_pass_entry.delete(0, 'end')

    def add_lecturer(self):
        username = self.lecturer_user_entry.get()
        password = self.lecturer_pass_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

        if username in self.controller.users:
            messagebox.showerror("Error", "This username already exists.")
        else:
            #update data to memory
            self.controller.users[username] = {'password': password, 'role': 'lecturer'}
            self.controller.lecturers.append(username)
            #save to database (.csv file)
            database.save_users(self.controller.users)
            #show success message
            messagebox.showinfo("Success", f"Lecturer '{username}' added successfully.")
            self.lecturer_user_entry.delete(0, 'end')
            self.lecturer_pass_entry.delete(0, 'end')

    def add_class(self):
        class_name = self.class_name_entry.get()

        if not class_name:
            messagebox.showwarning("Input Error", "Class name cannot be empty.")
            return

        if class_name in self.controller.classes:
            messagebox.showerror("Error", "This class already exists.")
        else:
            #update data to memory
            self.controller.classes.append(class_name)
            self.controller.attendance[class_name] = {}
            #save to database (.csv file)
            database.save_classes(self.controller.classes)
            database.save_attendance(self.controller.attendance)
            #show success message
            messagebox.showinfo("Success", f"Class '{class_name}' added successfully.")
            self.class_name_entry.delete(0, 'end')
            #update dropdowns
            self.controller.frames[LecturerPage].update_class_list()
            self.controller.frames[StudentPage].update_class_list()

#lecturer menu
class LecturerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #layout
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both") #centers the frame

        title = ttk.Label(main_frame, text="Lecturer Menu", font=("Arial", 20, "bold"))
        title.pack(pady=10, anchor="w")

        #widget
        #top selection part
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=5)

        ttk.Label(top_frame, text="Select Class:").pack(side="left", padx=5)

        #dropdown menu (combobox)
        self.class_combobox = ttk.Combobox(
            top_frame,
            values=self.controller.classes,
            state="readonly"
        )

        self.class_combobox.pack(side="left", padx=5, fill="x", expand=True)

        view_button = ttk.Button(top_frame, text="View Attendance", command=self.view_attendance)
        view_button.pack(side="left", padx=10)

        #attendance display area
        #show in table format

        #create frame for treeview
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        #column
        columns = ("student", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        #heading
        self.tree.heading("student", text="Student Username")
        self.tree.heading("status", text="Attendance Status")

        #scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        #pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        #tags for coloring rows
        self.tree.tag_configure('Present', background='lightgreen')
        self.tree.tag_configure('Absent', background='lightcoral')

        #logout button
        logout_button = ttk.Button(main_frame, text="Logout", command=self.controller.logout)
        logout_button.pack(pady=10, anchor="e", side="bottom")

    def view_attendance(self):
        #get selected class from dropdown (combobox)
        selected_class = self.class_combobox.get()
        if not selected_class:
            messagebox.showwarning("Input Error", "Please select a class.")
            return

        #clear old data from table (treeview)
        for item in self.tree.get_children():
            self.tree.delete(item)

        #load attendance data for selected class
        class_records = self.controller.attendance.get(selected_class, {})

        #populate table with all students
        present_count = 0
        absent_count = 0

        if not self.controller.students:
            self.tree.insert('', 'end', values=("No students found.", ""), tags=())
            return

        for student in self.controller.students:
            #check if student is in record for this class
            if student in class_records:
                status = class_records[student]
                tag = "Present"
                present_count += 1
            else:
                status = "Absent"
                tag = "Absent"
                absent_count += 1

            #insert row into table with correct tag
            self.tree.insert('', 'end', values=(student, status), tags=(tag,))

        #show summary message
        self.tree.insert('', 'end', values=("", ""), tags=())  # Blank line spacer
        self.tree.insert('', 'end', values=("Total Present:", present_count), tags=())
        self.tree.insert('', 'end', values=("Total Absent:", absent_count), tags=())

    def on_show(self):
        #update class list in combobox when page is shown
        self.update_class_list()
        #clear table when page is shown
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.class_combobox.set('') # clear selection

    def update_class_list(self):
        #refresh class list in combobox
        self.class_combobox['values'] = self.controller.classes

#student menu
class StudentPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #layout
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both") #centers the frame

        self.title_label = ttk.Label(main_frame, text="Student Menu", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        #widget
        ttk.Label(main_frame, text="Select Class:").pack(padx=10)

        #dropdown menu (combobox)
        self.class_combobox = ttk.Combobox(
            main_frame,
            state="readonly",
            width=40,
            values=self.controller.classes,
        )
        self.class_combobox.pack(pady=5)

        mark_button = ttk.Button(
            main_frame,
            text="Mark As Present",
            command=self.mark_attendance
        )

        mark_button.pack(pady=20, ipadx=10)

        #logout button
        logout_button = ttk.Button(main_frame, text="Logout", command=self.controller.logout)
        logout_button.pack(pady=10, side="bottom", anchor="e")

    def mark_attendance(self):
        student_name = self.controller.current_user
        selected_class = self.class_combobox.get()

        if not selected_class:
            messagebox.showwarning("No Class", "Please select a class.")
            return

        if student_name in self.controller.attendance[selected_class]:
            messagebox.showinfo("Already Marked", f"You have already marked attendance for {selected_class}.")
        else:
            #mark attendance
            self.controller.attendance[selected_class][student_name] = "Present"
            #save to database
            database.save_attendance(self.controller.attendance)
            messagebox.showinfo("Success", f"Attendance marked as Present for {selected_class}.")

    def update_class_list(self):
        #refresh class list in combobox
        self.class_combobox['values'] = self.controller.classes

    def on_show(self):
        # Update welcome message
        if self.controller.current_user:
            self.title_label.config(text=f"Welcome, {self.controller.current_user}!")
        # Update class list in combobox
        self.update_class_list()
        # Clear selection
        self.class_combobox.set('')

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()



















