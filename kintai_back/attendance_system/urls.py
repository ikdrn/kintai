# kintai_back/attendance_system/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # 追加

def home_view(request):
    return HttpResponse("Welcome to the 勤怠管理システム backend!")

urlpatterns = [
    path('', home_view, name='home'),  # ルートパスに対応するビューを追加
    path('admin/', admin.site.urls),
    path('api/', include('attendance_app.urls')),
]
