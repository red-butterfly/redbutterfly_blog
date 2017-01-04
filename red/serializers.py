from rest_framework import serializers
from .models import Article,User,Tag,Blogtype,Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'last_login', 'email', 'data_joined', 'address', 'city', 'country',
                  'qq', 'phone', 'heading')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tagname', 'tagcount', 'tagcreatedata', 'tagtips')


class BlogtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogtype
        fields = ('id', 'typename', 'count', 'tips')


class ArticleSerializer(serializers.ModelSerializer):
    typefor = serializers.StringRelatedField(source='typefor.typename')
    auther = serializers.StringRelatedField(source='auther.username')
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'summary', 'isreproduce' ,'publishtime', 'last_mod_time', 'readtimes', 'workimg',
            'typefor', 'auther', 'tags')

