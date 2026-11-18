from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', {'course_list': courses})


def about(request):
    return render(request, 'about.html')


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    questions = course.questions.all()
    return render(request, 'course_details.html', {'course': course, 'lessons': lessons, 'questions': questions})


def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        correct_count = 0
        total = 0
        results = []
        for question in course.questions.all():
            total += 1
            answer = request.POST.get('question_' + str(question.id))
            correct_choice = question.choices.filter(correct=True).first()
            ok = False
            if answer:
                choice = Choice.objects.get(pk=answer)
                if choice.correct:
                    correct_count += 1
                    ok = True
            results.append({'question': question, 'given': answer, 'correct': ok, 'correct_text': correct_choice.choice_text if correct_choice else ''})
        score = 0
        if total > 0:
            score = round((correct_count / total) * 100)
        user, created = User.objects.get_or_create(username='learner')
        submission = Submission.objects.create(exam=course, user=user, score=score)
        request.session['exam_results'] = [{'text': r['question'].question_text, 'correct_text': r['correct_text'], 'correct': r['correct']} for r in results]
        return redirect('exam_result', course_id=course_id)
    return redirect('course_details', course_id=course_id)


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.filter(exam=course).order_by('-created_at').first()
    if submission is None:
        return redirect('course_details', course_id=course_id)
    if submission.score >= 50:
        message = 'Congratulations! You passed the exam.'
    else:
        message = 'Sorry, you did not pass the exam. Please try again.'
    exam_results = request.session.pop('exam_results', None) or [
        {'text': q.question_text, 'correct_text': q.choices.filter(correct=True).first().choice_text if q.choices.filter(correct=True).exists() else '', 'correct': True}
        for q in course.questions.all()
    ]
    return render(request, 'exam_result.html', {'course': course, 'submission': submission, 'message': message, 'exam_results': exam_results})
