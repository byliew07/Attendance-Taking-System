import csv
import os  # To check if files exist

# --- File Names ---
USERS_FILE = 'users.csv'
CLASSES_FILE = 'classes.csv'
ATTENDANCE_FILE = 'attendance.csv'

# --- DEFAULT DATA (for first-time run) ---
DEFAULT_USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'lec1': {'password': 'lec123', 'role': 'lecturer'},
    'stu1': {'password': 'stu123', 'role': 'student'},
    'stu2': {'password': 'stu456', 'role': 'student'},
}

DEFAULT_CLASSES = ['PYT101 - Introduction to Python', 'HI202 - World History', 'DB301 - Database Systems']

DEFAULT_ATTENDANCE = {
    'PYT101 - Introduction to Python': {
        'stu1': 'Present',
    },
    'HI202 - World History': {},
    'DB301 - Database Systems': {
        'stu2': 'Present'
    }
}


# --- Load Functions ---

def load_users():
    """
    Loads all users from users.csv.
    If the file doesn't exist, it creates it with default users.
    Returns:
        - A dict of users: {username: {'password': '...', 'role': '...'}}
        - A list of student usernames
        - A list of lecturer usernames
    """
    if not os.path.exists(USERS_FILE):
        print(f"Creating {USERS_FILE} with default data.")
        save_users(DEFAULT_USERS)

    users = {}
    students = []
    lecturers = []

    try:
        with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:  # Skip empty rows
                    username, password, role = row
                    users[username] = {'password': password, 'role': role}
                    if role == 'student':
                        students.append(username)
                    elif role == 'lecturer':
                        lecturers.append(username)
    except Exception as e:
        print(f"CRITICAL ERROR loading users: {e}")
        return {}, [], []

    return users, students, lecturers


def load_classes_and_attendance():
    """
    Loads all classes from classes.csv and all attendance records
    from attendance.csv. Creates files with default data if they don't exist.
    Returns:
        - A list of class names
        - A dict of attendance data: {class_name: {student_name: 'Status'}}
    """

    # --- Load Classes ---
    if not os.path.exists(CLASSES_FILE):
        print(f"Creating {CLASSES_FILE} with default data.")
        save_classes(DEFAULT_CLASSES)

    classes = []
    try:
        # Use 'r' mode for reading
        with open(CLASSES_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:  # Skip empty rows
                    classes.append(row[0])
    except Exception as e:
        print(f"CRITICAL ERROR loading classes: {e}")
        classes = []  # Start with empty list on error

    # --- Load Attendance ---
    attendance = {class_name: {} for class_name in classes}

    if not os.path.exists(ATTENDANCE_FILE):
        print(f"Creating {ATTENDANCE_FILE} with default data.")
        save_attendance(DEFAULT_ATTENDANCE)
        # Merge default data into our empty dict for the first run
        for class_name, records in DEFAULT_ATTENDANCE.items():
            if class_name in attendance:
                attendance[class_name].update(records)

    try:
        with open(ATTENDANCE_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if not row: continue  # Skip empty rows
                class_name, student_username, status = row
                if class_name in attendance:
                    attendance[class_name][student_username] = status
                else:
                    # This can happen if a class was deleted but attendance data still exists
                    print(f"Warning: Attendance for '{class_name}' found but class does not exist.")
    except Exception as e:
        print(f"CRITICAL ERROR loading attendance: {e}")
        # We already initialized attendance, so we can proceed

    return classes, attendance


# --- Save Functions ---

def save_users(users):
    """Saves the entire users dictionary to users.csv"""
    try:
        with open(USERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'role'])  # Header
            for username, details in users.items():
                writer.writerow([username, details['password'], details['role']])
    except Exception as e:
        print(f"ERROR saving users: {e}")


def save_classes(classes):
    """Saves the entire list of classes to classes.csv"""
    try:
        with open(CLASSES_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['class_name'])  # Header
            for class_name in classes:
                writer.writerow([class_name])
    except Exception as e:
        print(f"ERROR saving classes: {e}")


def save_attendance(attendance):
    """
    Saves the entire attendance dictionary to attendance.csv.
    This rewrites the whole file every time.
    """
    try:
        with open(ATTENDANCE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['class_name', 'student_username', 'status'])  # Header
            # Un-nest the dictionary into rows
            for class_name, records in attendance.items():
                for student_username, status in records.items():
                    writer.writerow([class_name, student_username, status])
    except Exception as e:
        print(f"ERROR saving attendance: {e}")

