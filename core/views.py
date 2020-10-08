import json

from django.db.models import CharField, Value
from django.db.models.functions import Concat

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import CategorySerializer, CategoryRetrieveSerializer, CategoryFlatSerializer,  ProductSerializer,\
    AlbumSerializer, UserSerializer, CustomTokenObtainPairSerializer
from .models import Category, Product, Album, User
from .permissions import IsAdminPermission, IsAlbumAuthor


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminPermission,  IsAlbumAuthor)
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def product_list(request):
    # products = Product.objects.filter(sales__isnull=True)

    products = Product.objects.annotate(brand_title_and_brand_model_title=Concat('brand__title',
                                                      Value(' '),
                                                      'brand__brandmodel__title',
                                                      output_field=CharField())).distinct('id')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        def create_nested(data, parent):
            if parent:
                for obj in data:
                    for key, val in obj.items():
                        if key == 'name':
                            serializer = CategoryFlatSerializer(data={key: val})
                            if serializer.is_valid(raise_exception=True):
                                sub_category = serializer.save()
                                sub_category.parent = parent
                                sub_category.save()
                                if obj.get('children'):
                                    create_nested(obj.get('children'), sub_category)

        for key, val in request.data.items():
            if key == 'name':
                serializer = CategoryFlatSerializer(data={key: val})
                if serializer.is_valid(raise_exception=True):
                    category = serializer.save()
                    if request.data.get('children'):
                        create_nested(request.data.get('children'), category)
        return Response(status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()



