
def rating(feedbacks):

    marks = {
        'Очень плохо': 1,
        'Плохо': 2,
        'Терпимо': 3,
        'Нормально': 4,
        'Отлично': 5
    }
    total_marks = 0
    count = 0

    if feedbacks:
        for feedback in feedbacks:
            total_marks += marks.get(feedback.mark)
            count += 1
        return total_marks / count
    return 0
