from django.urls import path
from server.views import (home, loginview, user, new, camera, teacher, grade,
                          create, link, update_qrcode, register, para_end, para, requests,
                          success_grade,)


urlpatterns = [
    path('', home),
    path('user', user),
    path('new/<int:pk>', new),
    path('link/<str:qrcode>', link),
    path('camera', camera),
    path('teacher', teacher),
    path('grade', grade),
    path('create', create),
    path('para/<int:pk>', para),
    path('requests/<int:pk>', requests),
    path('success_grade/<int:pk>', success_grade),
    path('update_qrcode/<int:pk>', update_qrcode),
    path('login', loginview, name='login'),
    path('para_end/<int:pk>', para_end),
    path('register', register, name='register'),
]
