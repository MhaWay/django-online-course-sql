from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from onlinecourse.models import Course, Enrollment, Question, Choice, Submission, Answer


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', {'course_list': courses})


def about(request):
    return render(request, 'about.html')


def course_details(request, course_id):
    if request.user.is_authenticated:
        Enrollment.objects.get_or_create(user=request.user, course_id=course_id)
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    questions = course.questions.all()
    return render(request, 'course_details.html', {'course': course, 'lessons': lessons, 'questions': questions})


def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        if request.user.is_authenticated:
            user = request.user
        else:
            user, _ = User.objects.get_or_create(username='learner')
        submission = Submission.objects.create(exam=course, user=user, score=0)
        total = 0
        correct_count = 0
        for question in course.questions.all():
            total += 1
            choice_id = request.POST.get('question_' + str(question.id))
            if choice_id:
                try:
                    choice = Choice.objects.get(pk=choice_id, question=question)
                    Answer.objects.create(question=question, selected_choice=choice, submission=submission)
                    if choice.correct:
                        correct_count += 1
                except Choice.DoesNotExist:
                    pass
        score = round((correct_count / total) * 100) if total else 0
        submission.score = score
        submission.save()
        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)
    return redirect('course_details', course_id=course_id)


def show_exam_result(request, course_id, submission_id=None):
    course = get_object_or_404(Course, pk=course_id)
    if submission_id is not None:
        submission = get_object_or_404(Submission, pk=submission_id)
    else:
        submission = Submission.objects.filter(exam=course).order_by('-created_at').first()
    if submission is None:
        return redirect('course_details', course_id=course_id)
    if submission.score >= 50:
        message = 'Congratulations! You passed the exam.'
    else:
        message = 'Sorry, you did not pass the exam. Please try again.'
    exam_results = []
    for question in course.questions.all():
        correct_choice = question.choices.filter(correct=True).first()
        selected = question.answers.filter(submission=submission).first()
        exam_results.append({
            'question': question.question_text,
            'selected': selected.selected_choice.choice_text if selected else 'No answer',
            'correct_text': correct_choice.choice_text if correct_choice else '',
            'correct': bool(selected and selected.selected_choice.correct),
        })
    return render(request, 'exam_result.html', {
        'course': course,
        'submission': submission,
        'message': message,
        'exam_results': exam_results,
    })
