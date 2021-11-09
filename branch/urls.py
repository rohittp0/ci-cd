from django.urls import path

from branch.views import on_delete

urlpatterns = [
    path(r'on_delete', on_delete),
]
