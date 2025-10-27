# Using csv to save data to ensure the data keep after program exits.

import csv
import os

#File names
USER_FILE = 'users.csv'
CLASS_FILE = 'classes.csv'
ATTENDANCE_FILE = 'attendance.csv'

#Default users
default_users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'lecturer1': {'password': 'lecturer123', 'role': 'lecturer'},
    'student1': {'password': 'student123', 'role': 'student'},
    'student2': {'password': 'student234', 'role': 'student'},
}

#Default classes
default_classes = ['PYT101 - Introduction to Python', 'DS201 - Data Structures', 'DB301 - Database Systems']

#default attendance
default_attendance = {
    'PYT101 - Introduction to Python': {
        'student1': 'Present',
    },
    'DS201 - Data Structures': {},
    'DB301 - Database Systems': {
        'student2': 'Present'
    }
}

#Load users from CSV
def load_users():
    if not os.path.exists(USER_FILE):
        #If user file does not exist, create it with default users
        save_users(default_users)

    users = {}
    students = []
    lecturers = []

    try:
        with open(USER_FILE, mode='r') as file:
            reader = csv.reader(file)
            #Read users from CSV
            next(reader, None)  #Skip header
            for row in reader:
                if not row:
                    continue  #Skip empty rows
                username, password, role = row
                users[username] = {'password': password, 'role': role}
                if role == 'student':
                    students.append(username)
                elif role == 'lecturer':
                    lecturers.append(username)
    except Exception as e:
        print(f"Error loading users: {e}")
        return {},[],[]
    return users, students, lecturers

def load_classes_and_attendance():
    #load classes and attendance from CSV (classes.csv and attendance.csv)
    if not os.path.exists(CLASS_FILE):
        save_classes(default_classes)

    classes = []
    try:
        with open(CLASS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  #Skip header
            for row in reader:
                if row:
                    classes.append(row[0])  #Skip empty rows
    except Exception as e:
        print(f"Error loading classes: {e}")
        classes = []

    #Load attendance
    attendance = {class_name: {} for class_name in classes}

    if not os.path.exists(ATTENDANCE_FILE):
        save_attendance(default_attendance)
        #merge default data into empty dict for the first run.
        for class_name, records in default_attendance.items():
            if class_name in attendance:
                attendance[class_name].update(records)

    try:
        with open(ATTENDANCE_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  #Skip header
            for row in reader:
                if not row : continue
                class_name, student_username, status = row
                if class_name in attendance:
                    attendance[class_name][student_username] = status
                else:
                    print(f"Attendance for {class_name} found but class does not exist.")
                    #Occurs when attendance.csv has data for a class not in classes.csv

    except Exception as e:
        print(f"Error loading attendance: {e}")

    return classes, attendance

#Save users to CSV
def save_users(users):
    #saves the user data to users.csv
    try:
        with open(USER_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'role'])  #Header
            for username, details in users.items():
                writer.writerow([username, details['password'], details['role']])
    except Exception as e:
        print(f"Error saving users: {e}")

#Save classes to CSV
def save_classes(classes):
    #saves the class data to classes.csv
    try:
        with open(CLASS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['class_name'])  #Header
            for class_name in classes:
                writer.writerow([class_name])
    except Exception as e:
        print(f"Error saving classes: {e}")

#Save attendance to CSV
def save_attendance(attendance):
    #saves the attendance data to attendance.csv
    try:
        with open(ATTENDANCE_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['class_name', 'student_username', 'status'])  #Header
            for class_name, records in attendance.items():
                for student_username, status in records.items():
                    writer.writerow([class_name, student_username, status])
    except Exception as e:
        print(f"Error saving attendance: {e}")


