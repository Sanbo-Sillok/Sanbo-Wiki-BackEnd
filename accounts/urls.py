from django.urls import path
from .views import *

urlpatterns = [ 
    path('signin', RegisterView.as_view()),
    path('login', AuthView.as_view()),
]