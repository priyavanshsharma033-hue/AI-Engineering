class student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")

        s1 = student("John", 20)
        s2 = student("Alice", 22)
        s1.display()
        s2.display()

        with open("Student.json", "w") as file:
            json.dump([s1.__dict__, s2.__dict__], file)

            with open("Student.json", "r") as file:
                data = json.load(file)
                for student_data in data:
                    print(f"Name: {student_data['name']}, Age: {student_data['age']}")