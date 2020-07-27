from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('category/', views.CategoryViewSet.as_view({'get': 'list'})),
    path('category/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve'})),
    path('category/create/', views.CategoryCreateViewSet.as_view({'post': 'create'})),

]

#