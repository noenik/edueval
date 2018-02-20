from django.urls import path
import evaluate.views as views

app_name = 'eval'

urlpatterns = [
    path('<slug:url_hash>', views.evaluate, name='evaluate')
]
