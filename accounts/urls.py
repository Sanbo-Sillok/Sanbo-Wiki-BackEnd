from django.urls import path
from .views import *

urlpatterns = [ 
    path('signup', RegisterView.as_view()),
    path('login', AuthView.as_view()),
]