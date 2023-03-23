from django.urls import include, path
from rest_framework import routers
from api import views

# router = routers.DefaultRouter()

# router.register(r'films', views.fetch_films)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('update/<int:id>/', views.update_film),
    path('films', views.fetch_films),
]
