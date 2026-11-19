from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from onlinecourse.models import Course, Enrollment, Question, Choice, Submission


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


def calculate_score(request):
    questions = Question.objects.all()
    correct_count = 0
    total = questions.count()
    for question in questions:
        correct_ids = set(str(c.id) for c in question.choices.filter(correct=True))
        selected = set(request.POST.getlist('question_' + str(question.id), []))
        if selected & correct_ids:
            correct_count += 1
    if total == 0:
        return 0
    return round((correct_count / total) * 100)


def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        score = calculate_score(request)
        if request.user.is_authenticated:
            user = request.user
        else:
            user, _ = User.objects.get_or_create(username='learner')
        submission = Submission.objects.create(exam=course, user=user, score=score)
        return redirect('exam_result', course_id=course.id, submission_id=submission.id)
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
        exam_results.append({
            'text': question.question_text,
            'correct_text': correct_choice.choice_text if correct_choice else '',
            'correct': True,
        })
    return render(request, 'exam_result.html', {
        'course': course,
        'submission': submission,
        'message': message,
        'exam_results': exam_results,
    })
