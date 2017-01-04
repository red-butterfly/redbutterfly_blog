from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer

class ArticleList_Re(APIView):

    def get(self,requset,format=None):
        art = ArticleList()
        return Response(art.get(end=1))

class ArticleList():

    def get(self, start=0, end=None):
        article = Article.objects.all()[start:end]
        serializer = ArticleSerializer(article,many=True)
        #serializer = ArticleSerializer(article)
        return serializer.data
