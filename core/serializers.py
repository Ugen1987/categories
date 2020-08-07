from rest_framework import serializers
from .models import Category, Product


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = CategorySerializer(instance, context=self.context)
        return serializer.data


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()
    children = RecursiveSerializer(many=True)
    siblings = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'children', 'parents', 'siblings')

    def get_parents(self, obj):
        categories = Category.objects.exclude(id=obj.id)
        parents = []
        for category in categories:
            if obj in category.children.all():
                parents.append({"id": category.id, "name": category.name})
        return parents

    def get_siblings(self, obj):
        categories = Category.objects.exclude(id=obj.id)
        siblings = []
        for category in categories:
            if obj.parent == category.parent:
                siblings.append({"id": category.id, "name": category.name})
        return siblings


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'children')


class CategoryFlatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    brand_title_and_brand_model_title = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'price', 'brand', 'brand_title_and_brand_model_title')

