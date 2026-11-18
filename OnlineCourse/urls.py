from django.contrib import admin
from django.urls import path, include
from onlinecourse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('onlinecourse/', include('onlinecourse.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.about, name='index'),
]
