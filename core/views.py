import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import CategorySerializer, CategoryRetrieveSerializer, CategoryFlatSerializer
from.models import Category


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
