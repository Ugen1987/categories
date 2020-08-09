import time

from rest_framework import serializers


from rest_framework_simplejwt.serializers import TokenObtainSerializer, RefreshToken


from .models import Category, Product, Album, Track, User


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.USERNAME_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')


class TrackListingField(serializers.RelatedField):

    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(value.duration))
        return 'Track %d: %s (%s)' % (value.order, value.title, duration)


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)
    # tracks = TrackListingField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks', 'created_by')

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

    def update(self, album, validated_data):
        tracks_data = validated_data.pop('tracks')
        album.album_name = validated_data.get('album_name')
        album.artist = validated_data.get('artist')
        album.save()
        Track.objects.filter(album=album).delete()
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album


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

