from django.urls import path
from wiki.views import *

urlpatterns = [
    path('', create_post, name='create_post'),
    path('<str:title>', get_or_delete_or_edit_post,  name='get_post'), 
]