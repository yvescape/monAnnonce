from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:id>/", views.post, name="post"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("announce/", views.announce, name="announce"),
    path("new_announce/", views.createannounce, name="createannounce"),
    path("ndit_announce/<int:id>/", views.editannounce, name="editannounce"),
    path("dilete_announce/<int:id>/", views.supannounce, name="supannounce"),
    path("annonceur/", views.dev_ann, name="announceur"),
    path("admin_site/", views.admin_site, name="admin_site"),
]