from django.urls import path

import management.views as views

app_name = 'manage'
urlpatterns = [
    path('exam/<int:exam_id>/change', views.exam_change, name='exam_change'),
    path('exam/<int:exam_id>', views.exam_manage, name='exam_manage'),
    path('test', views.svg_test, name='test'),
    path('<slug:course>', views.mng_home, name='home_course'),
    path('', views.mng_home, name='home')
]