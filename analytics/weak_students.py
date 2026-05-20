def weak_students(student_data):

    weak = []

    for student in student_data:

        if student["mark"] < 50:
            weak.append(student)

    return weak