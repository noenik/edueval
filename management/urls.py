from django.conf.urls import url, include
import management.views as views

urlpatterns = [
    url(r'^$', views.mng_home, name='home')
]
