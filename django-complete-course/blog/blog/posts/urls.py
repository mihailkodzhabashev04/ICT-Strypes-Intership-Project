from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.HomeView.as_view()),
    #path("<int:id>/", views.post, name='post'),
    path("<int:pk>/", views.PostView.as_view(), name='post'),
    #path("tags/<int:id>/", views.Tags, name='tags'),
    path("tags/<int:pk>/", views.TagView.as_view(), name='tags'),
    #path('search/', views.search, name='search'),
    path('search/', views.SearchView.as_view(), name='search'),
]