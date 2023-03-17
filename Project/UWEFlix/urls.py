from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('temp', views.temp),
    path('add_club/', views.add_club),
    path('delete_club/<int:id>', views.delete_club),
    path('display_club/', views.display_club),

]
