from django.conf.urls import url, include
import management.views as views

urlpatterns = [
    url(r'^exam/(?P<exam_id>\d+)', views.exam, name='exam'),
    url(r'^test/$', views.svg_test, name='test'),
    url(r'^(?P<course>[a-zA-Z0-9_-]+)', views.mng_home, name='home_course'),
    url(r'^$', views.mng_home, name='home')
]
