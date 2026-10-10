name=input("Enter your name: ")
age=int(input("Enter your age: "))
course=input("Enter your course: ")
student={"Name":name,"age":age,"course":course}
for key, value in student.items():
    print(key, value)