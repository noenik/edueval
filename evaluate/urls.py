from django.conf.urls import url, include
import evaluate.views as views

urlpatterns = [
    url(r'^(?P<url_hash>\w+)$', views.evaluate, name='evaluate')
]
