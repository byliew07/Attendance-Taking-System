# CheckMeIN: The Swinburne GUI Attendance Tracker 📝
Welcome to **CheckMeIN**! 👋 This is a lightweight and powerful attendance-tracking system that runs entirely as a Python file.

It was built as a **Foundation in Programming project at Swinburne Sarawak** and is perfect for learning about data persistence (using *CSVs*), user roles, and modular programming.

## ✨ Features

### V1.0: The Original CLI 💻

* A robust, command-line interface for all operations.

* Add, edit, and remove students and classes.

* Take attendance directly from your terminal.

* Saves all data to .csv files.

### V2.0: The New GUI ✨

* A full-featured Graphical User Interface (GUI) for a user-friendly experience.

* All the features of V1, but now with buttons, forms, and visual feedback!

* Easily manage your database without touching the command line.


## 🏫 3 Distinct User Roles

### 🚀 The Admin (login: `admin` / `admin123`)
The all-powerful administrator who sets up the system.
* ➕ **Add New Students**: Register new students with a username and password.
* ➕ **Add New Lecturers**: Register new lecturers to the system.
* ➕ **Create New Classes**: Build the class catalog for everyone.

### 👩‍🏫 The Lecturer (login: `lec1` / `lec123`)
The "*eyes*" of the operation.
* 👀 **View Class Roster**: Select any class to see a full attendance report.
* 📊 **Formatted Table**: See who's "Present" and who's "Absent" in a clean, beautiful table format.

### 🎓 The Student (login: `stu1` / `stu123`)
The most important user!
* ✋ **Mark Attendance**: Students can log in, pick a class, and mark themselves as 'Present'.
* ✅ **Prevents Double-Marking**: The system is smart! It won't let a student mark attendance more than once.

## 🚀 How to Run
Getting started is as easy as 1-2-3!
### 1. **Clone or Download**
* Download the ZIP or clone the repository:
```
git clone https://github.com/byliew07/CheckMeIN.git
```
### 2. **Navigate to the Folder**
* Make sure you have Python 3 installed.
* Run the `main_gui.py` file from your terminal:
```
python main_gui.py
```
**That's it!** The very first time you run it, the program will automatically generate three new files for you to store all your data:
* `users.csv` 🧑‍🤝‍🧑
* `classes.csv` 📚
* `attendance.csv` 📈

## 🛠️ Project Structure
This project is split into three clean modules to keep things organized:
* `main_gui.py`: **The heart of the program!** ❤️ This file handles the main login logic, loads all the interface and data at startup, and directs users to the correct menu.
* `database.py`: **The "brains" 🧠 behind the data.** This module contains all the functions for reading from and writing to the `.csv` files.

## 💻 Tech Stack
* **Python 3** 🐍
* **Python** `csv` **Module** (built-in) 🗃️
* **Python** `tkinter` **Module** (for the v2.0 GUI) 🖥️
  
Built with simplicity in mind. No external libraries needed!

## 🤝 Contributing
This was a fun project! Feel free to fork it, improve it, or suggest new features. Pull requests are always welcome!
