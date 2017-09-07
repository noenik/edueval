from django.conf.urls import url, include
from django.contrib.auth.views import logout
import main.views as views

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', logout, kwargs={'next_page': 'main:index'}, name='logout'),
    url(r'^glemtpassord/', views.forgot_password, name='forgot_pw'),
    url(r'^nybruker/', views.handle_new_user, name='newuser'),
    url(r'^brukerinfo/', views.edit_user_info, name='ch_usr'),
    url(r'^$', views.index, name='index')
]
