def generate_ai_insight(pass_percentage):

    if pass_percentage > 90:
        return "Excellent academic performance detected."

    elif pass_percentage > 75:
        return "Overall performance is good."

    elif pass_percentage > 50:
        return "Students need moderate improvement."

    else:
        return "Critical academic improvement required."