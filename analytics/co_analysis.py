def calculate_co_attainment(co_marks):

    attainment = {}

    for co, marks in co_marks.items():

        average = sum(marks) / len(marks)

        attainment[co] = round(average, 2)

    return attainment