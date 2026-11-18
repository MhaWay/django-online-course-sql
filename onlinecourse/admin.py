from django.contrib import admin
from django.contrib.auth.models import User, Group
from onlinecourse.models import Course, Lesson, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_description')
    search_fields = ('course_name',)
    inlines = []


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_title', 'lesson_content', 'course_name')
    search_fields = ('lesson_title',)
    list_filter = ('course_name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_lec_num', 'question_course')
    search_fields = ('question_text',)
    list_filter = ('question_course',)
    inlines = [ChoiceInline]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'created_at')
    list_filter = ('exam',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
