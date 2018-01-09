from django.conf.urls import url, include
import management.views as views

app_name = 'manage'
urlpatterns = [
    url(r'^exam/(?P<exam_id>\d+)/change$', views.exam_change, name='exam_change'),
    url(r'^exam/(?P<exam_id>\d+)$', views.exam_manage, name='exam_manage'),
    url(r'^test/$', views.svg_test, name='test'),
    url(r'^(?P<course>[a-zA-Z0-9_-]+)', views.mng_home, name='home_course'),
    url(r'^$', views.mng_home, name='home')
]