from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("about/", views.about),
    path("projects/", views.projects),
    path("tasks/", views.tasks),
    path("create_task/", views.create_task),
    path("create_project/", views.create_project),
]
