from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('single-project/<int:pk>/', views.single_project, name='single-project'),
    path('add-project/', views.add_project, name='add-project'),
    path('update-project/<int:pk>', views.update_project, name='update-project'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete-project'),
]
