def calculate_attendance_mark(attendance):

    if attendance >= 96:
        return 5

    elif attendance >= 91:
        return 4

    elif attendance >= 86:
        return 3

    elif attendance >= 81:
        return 2

    elif attendance >= 76:
        return 1

    else:
        return 0


# ==================================================
# ATTENDANCE STATUS
# ==================================================

def attendance_status(attendance):

    if attendance >= 90:

        return "Excellent"

    elif attendance >= 80:

        return "Good"

    elif attendance >= 70:

        return "Average"

    else:

        return "Low Attendance"