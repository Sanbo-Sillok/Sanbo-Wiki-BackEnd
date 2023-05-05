from django.urls import path
from testapp.views import *

urlpatterns = [
    path('', get_testdata_all, name='get_testdata_all'),
    path('<int:id>', get_testdata,  name='get_testdata'),
    path('new', create_testdata, name='create_testdata'),
]