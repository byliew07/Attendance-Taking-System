from data import load_users, load_classes_and_attendance
from menu import admin_menu, lecturer_menu, student_menu

def login(users):
    #Handles user login process
    print("-------USER LOG IN-------")
    username = input("Username: ")
    password = input("Password: ")

    if username == "" or password == "":
        print("Username or password cannot be empty. Please try again.")
        return username, users[username]['role']  #Prompt user to login again

    elif username in users and users[username]['password'] == password:
        print(f"\nAccess Granted. Welcome, {username}!")
        #Return the username and their role
        return username, users[username]['role']

    else:
        print("Access Denied. Invalid username or password.")

def main():
    #main function of the program
    print("=====================================================")
    print("Welcome to the Swinburne Attendance Management System")
    print("=====================================================")

    #Load data from CSV files
    users, students, lecturers = load_users()
    classes, attendance = load_classes_and_attendance()

    if not users:
        print("No users found in the system. Please contact the administrator to set up user accounts.")
        return #Exit program if no users exist

    #main program loop
    while True:
        username, role = login(users)

        #Direct user to appropriate menu based on role
        if role == 'admin':
            admin_menu(users, students, lecturers, classes, attendance)
        elif role == 'lecturer':
            lecturer_menu(username,students, classes, attendance)
        elif role == 'student':
            student_menu(username,classes, attendance)
        else:
            print("Error: Unknown user role.")

        #After user logs out, ask if they want to exit or log in again
        logout_choice = input("\nDo you want to log in again? (yes/no): ").strip().lower()
        if logout_choice != 'yes':
            print("Exiting the system... See you next time!")
            break #Exit the main while True loop

if __name__ == "__main__":
    main()


