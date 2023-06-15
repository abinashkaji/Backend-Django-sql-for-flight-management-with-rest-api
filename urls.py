from django.urls import path
from . import views

urlpatterns=[
path("",views.index,name="index"),
path("<int:fid>",views.flight,name="flight"),    
path("<int:fid>/book",views.book,name="books"),
]