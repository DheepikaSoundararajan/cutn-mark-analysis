def predict_rank(gpa):

    if gpa >= 9:
        return "Top 10 Rank"

    elif gpa >= 8:
        return "Top 25 Rank"

    elif gpa >= 7:
        return "Top 50 Rank"

    else:
        return "Needs Improvement"