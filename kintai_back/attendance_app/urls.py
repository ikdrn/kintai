# kintai_back/attendance_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('attendance/', views.get_attendance, name='get_attendance'),
    path('attendance/update/', views.update_attendance, name='update_attendance'),
]
