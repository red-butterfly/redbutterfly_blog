# -*- coding: UTF-8 -*-
from red.models import *

TYPE_INDEX = 1
TYPE_EDIT = 2

IndexValues = 'id', 'title', 'summary', 'last_mod_time'
EditValues = 'id', 'title', 'typefor__typename', 'auther__username','last_mod_time', 'readtimes'


class ArticleUtil(object):

    @staticmethod
    def getcommentcount(id=None):
        if id:
            return Comment.objects.filter(blog__id=id).count()
        else:
            return Comment.objects.count()

    @staticmethod
    def getcount(author=None, type=None, tag=None):
        if author:
            return Article.objects.filter(auther__username=author)
        elif type:
            return Article.objects.filter(typefor__id=type)
        elif tag:
            return Article.objects.filter(tags__id=tag)
        else:
            return Article.objects.count()

    @staticmethod
    def getlist(start=0, end=None, type=TYPE_INDEX):
        if type == TYPE_INDEX:
            article = Article.objects.all()[start:end].values(*IndexValues)
            for item in article:
                item['comment'] = Comment.objects.filter(blog__id=item['id']).count()
        elif type == EditValues:
            article = Article.objects.all()[start:end].values(*EditValues)

        return article