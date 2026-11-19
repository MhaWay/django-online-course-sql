from django.contrib import admin
from django.contrib.auth.models import User, Group
from onlinecourse.models import Course, Lesson, Question, Choice, Submission, Instructor, Learner


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_description')
    search_fields = ('course_name',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_title', 'course_name')
    search_fields = ('lesson_title',)
    list_filter = ('course_name',)
    inlines = []


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_lec_num', 'question_course')
    search_fields = ('question_text',)
    list_filter = ('question_course',)
    inlines = [ChoiceInline]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class LearnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
