from django.contrib.auth.views import logout
from django.urls import path

import main.views as views

app_name = 'main'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', logout, kwargs={'next_page': 'main:index'}, name='logout'),
    path('forgotpw', views.forgot_password, name='forgot_pw'),
    path('newuser', views.handle_new_user, name='newuser'),
    path('userinfo', views.edit_user_info, name='ch_usr'),
    path('', views.index, name='index')
]
