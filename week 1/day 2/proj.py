student = [
    {
        "name": "Vanshu",
        "age": 19,
        "course": "B.Tech"
    }
]


def add_student():
    name1 = input("Enter your name: ")
    age1 = int(input("Enter your age: "))
    course2 = input("Enter your course: ")

    new_student = {
        "name": name1,
        "age": age1,
        "course": course2
    }

    student.append(new_student)


while True:
    print(
        "1. Add a new student\n"
        "2. Display all students\n"
        "3. Find a student\n"
        "4. Exit\n"
    )

    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_student()

    elif choice == 2:
        for i in student:
            print(i)

    elif choice == 3:
        naam = input("Enter the name of the student to find: ")
        for i in student:
            if i["name"] == naam:
                print(i)
                break
        else:
            print("Student not found.")

    elif choice == 4:
        print("Exiting the program...")
        break

    else:
        print("Invalid choice")