# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class User(AbstractUser):
	address = models.CharField(u'地址',max_length=150,blank=True) 
	city = models.CharField(u'城市',max_length=30,blank=True)
	country = models.CharField(u'国家',max_length=30,blank=True)
	qq = models.CharField(u'QQ',max_length=15,blank=True)
	phone = models.CharField(u'电话',max_length=15,blank=True)
	heading = models.ImageField(u'头像',blank=True)

	def __unicode__(self):
		return self.username	

class Tag(models.Model):
	tagname = models.CharField(u'标签名称',max_length=30)
	tagcount = models.IntegerField(u'标签作品数量')
	tagcreatedata = models.DateTimeField(u'标签创建时间',auto_now_add=True)
	tagtips = models.IntegerField(u'标签访问量')
	
	def __unicode__(self):
		return self.tagname

	def get_article(self):
		"""
		获取该标签的文章列表
		"""
		article = Article.objects.filter(tags=self)
		return article 

	

class blogtype(models.Model):
	typename = models.CharField(u'类型名称',max_length=30)
	count = models.IntegerField(u'作品数量')
	tips = models.IntegerField(u'类型访问量')
	
	def __unicode__(self):
		return self.typename
	
	def get_article(self):
		"""
		获取该类型的文章列表
		"""
		article = Article.objects.filter(typefor=self)
		return article


class Article(models.Model):
	title = models.CharField(u'标题',max_length=100)

	typefor = models.ForeignKey(blogtype)
	auther = models.ForeignKey(User,default="")
	tags = models.ManyToManyField(Tag)

	content = models.TextField(u'文章内容')
	summary = models.CharField(u'文章摘要',max_length=200,blank=True)
	isreproduce = models.BooleanField(u'是否转载')
	publishtime = models.DateTimeField(u'上传时间',auto_now_add=True)
	last_mod_time = models.DateTimeField(u'修改时间',auto_now=True)
	readtimes = models.IntegerField(u'阅读量',default=0)

	def save(self,*args,**kwargs):
		add_new = False
		if self.id == None:
			add_new = True
		super(Article,self).save(*args,**kwargs)
		if add_new:
			self.typefor.count = self.typefor.count + 1
			self.typefor.save() 

	def delete(self,*args,**kwargs):
		tmp = self.typefor
		super(Article,self).delete(*args,**kwargs)		
		tmp.count = tmp.count - 1
		tmp.save()

	def __unicode__(self):
		return self.title
	
	def get_tags(self):
		tags = self.tags.all()
		return tags

	def get_pre_article(self):
		"""
		获取同分类的上一篇文章
		"""
		cur = Article.objects.get(id=self.id)
		temp = Article.objects.filter(typefor=cur.typefor).order_by('id')
		count=0
		for i in temp:
			if i.id == cur.id:
				index = count
				break
			else:
				count = count + 1
		if index != 0:
			return temp[index-1]
		
	def get_next_article(self):
		"""
		获取同分类的下一篇文章
		"""
		cur = Article.objects.get(id=self.id)
		temp = Article.objects.filter(typefor=cur.typefor).order_by('id')
		max = len(temp)+1
		count=0
		for i in temp:
			if i.id == cur.id:
				index = count
				break
			else:
				count = count + 1
		if index != max:
			return temp[index+1]
		
	
	class Meta:
		ordering = ['-publishtime']

class Comment(models.Model):
	user = models.CharField(u'用户名称',max_length=30)
	blog = models.OneToOneField(Article)	
	email = models.EmailField(u'邮箱',blank=True)
	content = models.TextField(u'评论内容')
	replaytime = models.DateTimeField(u'评论时间',auto_now_add=True)
	
	def __unicode__(self):
		return self.user


	
	
	

