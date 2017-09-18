from django.conf.urls import url, include
from django.contrib.auth.views import logout
import evaluate.views as views

urlpatterns = [
    url(r'^(?P<id>\d+)$', views.evaluate, name='evaluate')
]
