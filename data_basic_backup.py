# This program only saves data using in-memory data structures. All data will be lost when the program exits.

# User database like {username: {'password': '...', 'role': '...'}}
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'lecturer1': {'password': 'lecturer123', 'role': 'lecturer'},
    'student1': {'password': 'student123', 'role': 'student'},
    'student2': {'password': 'student234', 'role': 'student'},
}

#Classes database like ['class-id' - 'class-name']
classes = ['PYT101 - Introduction to Python', 'DS201 - Data Structures', 'DB301 - Database Systems']

#List to track all lecturers and students
students = ['student1', 'student2']
lecturers = ['lecturer1']

#Main attendance record (For default/ first time use)
attendance = {
    'PYT101 - Introduction to Python': {
        'student1': 'Present',
    },
    'DS201 - Data Structures': {},
    'DB301 - Database Systems': {
        'student2': 'Present'
    }
}

#hello,hello,hello