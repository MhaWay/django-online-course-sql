from django.urls import path
from onlinecourse import views

urlpatterns = [
    path('', views.index, name='index'),
    path('course_details/<int:course_id>/', views.course_details, name='course_details'),
    path('course_details/<int:course_id>/submit', views.submit, name='submit'),
    path('course_details/<int:course_id>/exam_result/<int:submission_id>', views.show_exam_result, name='exam_result'),
    path('course_details/<int:course_id>/exam_result', views.show_exam_result, name='exam_result_latest'),
]
