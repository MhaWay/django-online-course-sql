from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Course(models.Model):
    course_name = models.CharField(max_length=63)
    course_description = models.CharField(max_length=2000)

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    lesson_title = models.CharField(max_length=100)
    lesson_content = models.TextField()
    course_name = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson_title


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_lec_num = models.IntegerField(default=None)
    question_course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def is_answered(self, submission):
        return Answer.objects.filter(question=self, submission=submission).exists()


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.course.course_name


class Submission(models.Model):
    exam = models.ForeignKey(Course, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submissions', on_delete=models.CASCADE)
    score = models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.exam.course_name + ': ' + str(self.get_score())

    def get_score(self):
        total = self.exam.questions.count()
        if total == 0:
            return 0
        correct_count = Answer.objects.filter(submission=self, selected_choice__correct=True).values('question').distinct().count()
        return round((correct_count / total) * 100)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, related_name='answers', on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.question_text + ' -> ' + self.selected_choice.choice_text


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
