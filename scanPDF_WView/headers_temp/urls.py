from django.urls import path
from . import views

urlpatterns = [
    path('showpdf/headers/', views.headers, name='headers'),
]