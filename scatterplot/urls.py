from django.urls import path
from . import views

urlpatterns = [
    path('scatter/', views.scatter_view, name='scatter_view'),
]
