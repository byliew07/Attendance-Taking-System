from data import save_users, save_classes, save_attendance

def admin_menu(users, students, lecturers, classes, attendance):
    #display menu and action for admin
    print("---------Admin Menu---------")
    while True:
        print("\nWhat would you like to do?")
        print("1. Add student")
        print("2. Add lecturer")
        print("3. Add classes")
        print("4. Remove Student")
        print("5. Remove lecturer")
        print("6. Remove classes")
        print("7. Log Out")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            #Add student to database
            print("\n---Add New Student---")
            username = input("Enter new student's username: ")
            password = input("Enter new student's password: ")
            if username in users:
                print("Username already exists. Please try again.")
            else:
                users[username] = {'password': password, 'role': 'student'}
                students.append(username)
                save_users(users) #Save updated users to CSV
                print(f"Student '{username}' added successfully.")

        elif choice == "2":
            #Add lecturer to database
            print("\n---Add New Lecturer---")
            username = input("Enter new lecturer's username: ")
            password = input("Enter new lecturer's password: ")
            if username in users:
                print("Username already exists. Please try again.")
            else:
                users[username] = {'password': password, 'role': 'lecturer'}
                lecturers.append(username)
                save_users(users) #Save updated users to CSV
                print(f"Lecturer '{username}' added successfully.")

        elif choice == "3":
            #Add class to database
            print("\n---Add New Class---")
            class_name = input("Enter new class name (e.g., 'PYT101 - Introduction to Python'): ")
            if class_name in classes:
                print("Class already exists. Please try again.")
            else:
                classes.append(class_name)
                attendance[class_name] = {} # Initialize empty attendance record for the new class
                save_classes(classes)
                save_attendance(attendance) #Save updated attendance to CSV
                print(f"Class '{class_name}' added successfully.")

        elif choice == "4":
            #Remove student
            print("\n---Remove Student---")
            if not students:
                print("No students available to remove.")
                continue

            for i, student_username in enumerate(students, 1):
                print(f"{i}. {student_username}")

            try:
                choice_num = int(input(f"Enter number of student (1-{len(students)}) to remove: "))
                if 1 <= choice_num <= len(students):
                    student_to_remove = students.pop(choice_num - 1)

                    #Remove from users dict
                    if student_to_remove in users:
                        del users[student_to_remove]
                    # Remove from attendance records
                    for class_name in attendance:
                        if student_to_remove in attendance[class_name]:
                            del attendance[class_name][student_to_remove]

                    #Save all changes
                    save_users(users)
                    save_attendance(attendance)
                    print(f"Student '{student_to_remove}' removed successfully.")
                else:
                    print("Invalid student number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "5":
            #Remove lecturer
            print("\n---Remove Lecturer---")
            if not lecturers:
                print("No lecturers available to remove.")
                continue

            for i, lecturer_username in enumerate(lecturers, 1):
                print(f"{i}. {lecturer_username}")

            try:
                choice_num = int(input(f"Enter number of lecturer (1-{len(lecturers)}) to remove: "))
                if 1 <= choice_num <= len(lecturers):
                    lecturer_to_remove = lecturers.pop(choice_num - 1)

                    #Remove from users dict
                    if lecturer_to_remove in users:
                        del users[lecturer_to_remove]

                    #Save all changes
                    save_users(users)
                    print(f"Lecturer '{lecturer_to_remove}' removed successfully.")
                else:
                    print("Invalid lecturer number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "6":
            #Remove class
            print("\n---Remove Class---")
            if not classes:
                print("No classes available to remove.")
                continue

            for i, class_name in enumerate(classes, 1):
                print(f"{i}. {class_name}")
            try:
                choice_num = int(input(f"Enter number of class (1-{len(classes)}) to remove: "))
                if 1 <= choice_num <= len(classes):
                    class_to_remove = classes.pop(choice_num - 1)

                    #Remove from attendance dict
                    if class_to_remove in attendance:
                        del attendance[class_to_remove]

                    #Save all changes
                    save_classes(classes)
                    save_attendance(attendance)
                    print(f"Class '{class_to_remove}' removed successfully.")
                else:
                    print("Invalid class number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "7":
            print("Logging out...")
            break #Exit admin menu loop

        else:
            print("Invalid choice. Please enter a number from 1-4.")

def lecturer_menu(username, students, classes, attendance):
    #display menu and action for lecturer
    print(f"---Lecturer Menu (Logged In as {username})---")
    while True:
        print("\nWhat would you like to do?")
        print("1. View Attendance Records")
        print("2. Log Out")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            #View attendance
            print("\n---Choose class to view---")
            if not classes:
                print("No classes available.")
                continue

            #Display available classes
            for i, class_name in enumerate(classes, 1):
                print(f"{i}. {class_name}")

            try:
                class_choice = int(input(f"Enter number of class (1-{len(classes)}) to view: "))
                if 1 <= class_choice <= len(classes):
                    selected_class = classes[class_choice - 1]
                    print(f"\n---Attendance for {selected_class}---")
                    #Make sure class has attendance records
                    class_records = attendance.get(selected_class, {})

                    if not students:
                        print("No students are registered in the system.")
                        continue

                    print("\n"+"-"*32)
                    print(f"{'Student Username':<20} | {'Status':<10}")
                    print("-"*32)

                    #Check all registered students
                    absent_counts = 0
                    present_counts = 0

                    for student_username in students:
                        status_str = "Absent" #Default status
                        if student_username in class_records:
                            #Student is present
                            status = class_records[student_username]
                            status_str = status
                            print(f"{student_username:<20} | {status_str:<10}")
                            present_counts += 1
                        else:
                            print(f"{student_username:<20} | {'Absent':<10}")
                            absent_counts += 1

                    print("-"*32)

                    print(f"\nSummary Attendance: {present_counts} Present, {absent_counts} Absent")

                else:
                    print("Invalid class number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "2":
            print("Logging out from Lecturer Menu...")
            break #Exit lecturer menu loop

        else:
            print("Invalid choice. Please enter a number from 1-2.")

def student_menu(username, classes, attendance):
    #display menu and action for student
    print(f"--------Student Menu (Logged in as: {username})--------")
    while True:
        print("\nWhat would you like to do?")
        print("1. Mark Attendance")
        print("2. Log Out")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            #Mark attendance
            print("\n---Which class do you want to attend?---")
            if not classes:
                print("No classes available.")
                continue

            #Display available classes
            for i, class_name in enumerate(classes, 1):
                print(f"{i}. {class_name}")

            try:
                class_choice = int(input(f"Enter number of class (1-{len(classes)}): "))
                if 1 <= class_choice <= len(classes):
                    selected_class = classes[class_choice - 1]

                    #Ensure class exist in dict (attendance)
                    if selected_class not in attendance:
                        attendance[selected_class] = {}

                    #Check if already marked attendance
                    if username in attendance[selected_class]:
                        print(f"You have already marked attendance for ({selected_class}) as {attendance[selected_class][username]}.")
                    else:
                        #Mark as present
                        attendance[selected_class][username] = 'Present'
                        save_attendance(attendance) #Save updated attendance to CSV
                        print(f"Attendance marked as 'Present' for class {selected_class}.")
                else:
                    print("Invalid class number. Please try again.")
            except ValueError:
                        print("Invalid input. Please enter a number.")

        elif choice == "2":
            print("Logging out from Student Menu...")
            break

        else:
            print("Invalid choice. Please enter a number from 1-2.")








