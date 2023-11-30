from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login),
    path("about/", views.about),
    path("projects/", views.projects),
    path("tasks/", views.tasks),
    path("create_task/", views.create_task),
    path("create_project/", views.create_project),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
