from django.conf.urls import url, include
import management.views as views

urlpatterns = [
    url(r'^(?P<course>\w+)', views.mng_home, name='home_course'),
    url(r'^$', views.mng_home, name='home')
]
