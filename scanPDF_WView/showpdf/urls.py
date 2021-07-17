from django.urls import path, include
from django.conf.urls import url
from . import views

app_name="showpdf"
urlpatterns = [
    path("", views.index, name="index"),
    url(r"^(?P<page>[0-9]+)/(?P<post_range>[0-9]+)$", views.index, name="index_page"), 
    url(r'^bank/(?P<data_id>[0-9]+)$', views.bank_details, name="bank_details"),
    url(r'edit/(?P<data_id>[0-9]+)$', views.edit_bank, name= "edit_bank"),
    path("edit_data", views.edit_statement, name= "edit_statement"),
]