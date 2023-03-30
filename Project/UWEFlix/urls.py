from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('booking', views.booking, name='booking'),
    path('temp', views.temp, name='temp'),
    path('account', views.account, name='account'),
    path('account_management', views.account_management, name='account_management'),
    path('add_account', views.add_account),
    path('view_account', views.view_account),
    path('modify_account', views.modify_account),
    path('cinema_management', views.cm_dash, name='cinema_management'),
    path('film_management', views.film_dash, name='film_management'),
    path('add_film', views.add_film, name='add_film'),
    path('modify_film', views.modify_film, name='modify_film'),
    path('delete_film', views.delete_film, name='delete_film'),
    path('showings_management', views.showings_dash, name='showings_management'),
    path('add_showing', views.add_showing, name='add_showing'),
    path('modify_showing', views.modify_showing, name='modify_showing'),
    path('delete_showing', views.delete_showing, name='delete_showing'),

]
