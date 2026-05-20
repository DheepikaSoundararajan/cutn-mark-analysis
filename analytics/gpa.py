def calculate_gpa(marks):

    total = sum(marks)
    average = total / len(marks)

    gpa = round((average / 10), 2)

    return gpa