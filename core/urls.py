from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('categories/', views.CategoryCreateViewSet.as_view({'post': 'create'})),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve'})),
]
