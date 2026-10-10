def intro(name,age,course):
    print(f"My name is {name}")
    print(f"I am {age} years old")
    print(f"I am currently enrolled in {course}")

    

name=input(("What is your name:"))
age=float(input(("What is your age:")))
course=input(("What is your course:"))

intro(name,age,course)