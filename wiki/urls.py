from django.urls import path
from wiki.views import *

urlpatterns = [
    path('', create_post, name='create_post'),
    path('<str:title>', get_post,  name='get_post'), 
    path('<str:title>', delete_post,  name='delete_post'),
    path('edit/<str:title>', edit_post,  name='edit_post'),           
]