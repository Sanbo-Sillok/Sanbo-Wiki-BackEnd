from django.urls import path
from wiki.views import *


urlpatterns = [
    path('', PostList.as_view()),
    path('<str:title>', PostDetail.as_view()),
    path('w/all', get_all_title.as_view()),
]