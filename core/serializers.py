from rest_framework import serializers
from .models import Category


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = CategorySerializer(instance, context=self.context)
        return serializer.data


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = CategorySerializer(instance, context=self.context)
        return serializer.data


class CategoryCreateSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'children')
