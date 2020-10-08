from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = 'core'

urlpatterns = [
    path('token/', views.EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('create-user/', views.create_user, name='create_user'),
    path('albums/', views.AlbumViewSet.as_view({'get': 'list', 'post': 'create'}), name='album_list'),
    path('albums/<int:pk>/', views.AlbumViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('products/', views.product_list, name='product_list'),

    path('categories/', views.CategoryCreateViewSet.as_view({'post': 'create'})),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve'})),
]
