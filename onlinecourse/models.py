from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=63)
    course_description = models.CharField(max_length=2000)

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    lesson_title = models.CharField(max_length=100)
    lesson_content = models.TextField()
    course_name = models.ForeignKey(Course, related_name='lessons', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.lesson_title


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_lec_num = models.IntegerField(default=0)
    question_course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    exam = models.ForeignKey(Course, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.course_name}: {self.score}"
