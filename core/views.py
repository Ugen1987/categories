import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import CategorySerializer, CategoryRetrieveSerializer
from.models import Category


class CategoryCreateViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        def create_nested(data, parent):
            if parent:
                for obj in data:
                    for key, val in obj.items():
                        if key == 'name':
                            if Category.objects.filter(name=obj.get(key)).last():
                                return Response(json.dumps({key: val}), status=status.HTTP_400_BAD_REQUEST)
                            sub_category = Category.objects.create(name=obj.get(key),
                                                                   parent=parent)
                    if obj.get('children'):
                        create_nested(obj.get('children'), sub_category)

        for key, val in request.data.items():
            if key == 'name':
                if Category.objects.filter(name=request.data.get(key)).last():
                    return Response(json.dumps({key: val}), status=status.HTTP_400_BAD_REQUEST)
                category = Category.objects.create(name=request.data.get(key))
                if request.data.get('children'):
                    create_nested(request.data.get('children'), category)

        create_nested(request.data, parent=None)
        return Response(status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()

