from django.urls import path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.signout, name="logout"),
    path("about/", views.about),
    path("tasks/", views.tasks, name="tasks"),
    path("create_task/", views.create_task),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
