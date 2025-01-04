from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/<uuid:pk>/', views.MovieDetailApi.as_view(), name='movie-detail'),
    path('movies/', views.MoviesListApi.as_view(), name='movies-list'),
]
