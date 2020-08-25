from django.urls import path

from . import views

#app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>",views.call_get_entry,name="entry"),
    path("wiki/",views.show_entry,name="show_entry"),                #for search bar
    path("add/",views.add,name="add"),
    path("edit/<str:entry_name>",views.edit_page,name="edit"),
    path("random/",views.random_page,name="random"),
]
