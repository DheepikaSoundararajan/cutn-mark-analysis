def pass_fail_analysis(marks):

    passed = 0
    failed = 0

    for mark in marks:

        if mark >= 50:
            passed += 1
        else:
            failed += 1

    return passed, failed