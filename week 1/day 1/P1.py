students =[ {
    "name1": "John Doe",
    "age1": 20,
    "course1": "Computer Science"},
    {
    "name2": "Jane Smith",
    "age2": 22,
    "course2": "Mathematics"}

]
for student in students:
    for key, value in student.items():
        print(key, value)