# -*- coding: UTF-8 -*-
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import * 
from redpackage.aboutsys.getsysinfo import *
from django.core.cache import cache
from django.conf import settings
from markdown import markdown
from django.conf import settings 
from PIL import Image

# Create your views here.

def articlelist(request):
	return render(request,'article_list.html')

@login_required
def articlelist_edit(request):
	articlelist = []
	if request.method == "POST":
		for tmp in request.POST.getlist('delete_id'):
			Article.objects.filter(id=tmp).delete()
	for tmp in Article.objects.all():
		articlelist.append({"id":tmp.id,"title":tmp.title,"type":tmp.typefor.typename,"author":tmp.auther.username,"date":tmp.last_mod_time,"readtimes":tmp.readtimes})
	
	if request.user.is_authenticated():
		username = request.user.username
	else:
		username = "None"
	return render(request,'edit_article_list.html',{"articlelist":articlelist,
			"username":username})
	
	
def article(request):
	if request.method == 'GET':
		articleinfo = {}
		commentlist = []
		#获取文章相关的所有信息，包括评论
		getid = request.GET['id']
		taglist = []

		article = Article.objects.get(id=getid)
		articleinfo['id'] = article.id
		articleinfo['title'] = article.title
		articleinfo['user'] = article.auther.username
		articleinfo['content'] = markdown(article.content)
		articleinfo['date'] = article.last_mod_time
		articleinfo['imgurl'] = article.workimg
		for tmp in article.tags.all():
			taglist.append(tmp.tagname)
		article.readtimes = article.readtimes + 1
		article.save()	
		getcomment = Comment.objects.filter(blog=article)
		commentcount = len(getcomment)
		for tmp in getcomment:
			commentlist.append({"user":tmp.user,"date":tmp.replaytime,"message":tmp.content})	

		#获取 类型 和 tags，用于右侧展示
		alltypelist = []
		alltaglist = []
		alltype = Blogtype.objects.all() 
		for typetmp in alltype:
			alltypelist.append({"id":typetmp.id,"name":typetmp.typename})
		alltag = Tag.objects.all()
		for tagtmp in alltag:
			alltaglist.append({"id":tagtmp.id,"name":tagtmp.tagname})
		
		if request.user.is_authenticated():
			username = request.user.username
		else:
			username = "None"
		return render(request,'article.html',{"articleinfo":articleinfo,
			"username":username,
			"taglist":taglist,
			"commentcount":commentcount,
			"commentlist":commentlist,
			"alltypelist":alltypelist,
			"alltaglist":alltaglist})
	
	
def edit_article(request):
	typelist = []
	authorlist = []
	taglist = []
	taglistselect = []
	post_data = {}
	tagQS = []
	#当方法为POST，为提交更新/添加信息
	if request.method == 'POST':
		isre_value = 0
		post_data['title'] = request.POST['article_title']
		post_data['type'] = request.POST['article_type']
		post_data['author'] = request.POST['article_author']
		post_data['tag'] = request.POST.getlist('article_tag')
		post_data['content'] = request.POST['article_content']
		post_data['summary'] = request.POST['article_summary']
		post_data['readtimes'] = request.POST['article_readtimes']
		#针对是否转载的信息，进行判断
		try:
			post_data['isre'] = request.POST['article_isre']
			if post_data['isre'] == 'on':
				isre_value = 1
		except:
			isre_value = 0
		#获取上传的图片
		image = request.FILES['image']
		if image:
			imagetime = request.user.username+str(time.time()).split('.')[0]
			image_last = str(image).split('.')[-1]
			imagename = 'article_img/%s.%s' % (imagetime,image_last)
			img = Image.open(image)
			img.save('media/'+imagename)
		
		typeQS = Blogtype.objects.get(typename=post_data['type'])
		authorQS = User.objects.get(username=post_data['author'])

		is_new = 0
		try:
			newArt = Article.objects.get(title=post_data['title'])
		except Article.DoesNotExist:
			newArt = Article()
			is_new = 1
		newArt.title=post_data['title']
		newArt.typefor=typeQS
		newArt.auther=authorQS
		newArt.content=post_data['content']
		newArt.summary=post_data['summary']
		newArt.readtimes=int(post_data['readtimes'])
		newArt.isreproduce=isre_value
		if image:
			newArt.workimg = imagename
		newArt.save()
		#ManyToMany的字段，在保存之后，通过以下方式进行添加
		for tmp in post_data['tag']:
			tagtmp = Tag.objects.get(tagname=tmp)
			tagtmp.tagcount = tagtmp.tagcount + 1
			tagtmp.save()		
			newArt.tags.add(Tag.objects.get(tagname=tmp))
		return HttpResponseRedirect( '/article/?id=%s' % newArt.id )
		
	#方法为GET，则为获取编辑界面，通过判断是否包含title，来决定是更新，还是新添加	
	elif request.method == 'GET':
		for typetmp in Blogtype.objects.all():
			typelist.append(typetmp.typename)
		for authortmp in User.objects.all():
			authorlist.append(authortmp.username)
		for tagtmp in Tag.objects.all():
			taglist.append(tagtmp.tagname) 
		if 'id' in request.GET:
			artid = request.GET['id']
			article = Article.objects.get(id=artid)
			post_data['title'] = article.title
			post_data['type'] = article.typefor.typename
			post_data['author'] = article.auther.username
			post_data['tag'] = article.tags
			post_data['content'] = article.content
			post_data['summary'] = article.summary
			post_data['isre'] = article.isreproduce
			post_data['readtimes'] = article.readtimes
			for tmp in article.tags.all():
				taglistselect.append(tmp.tagname)
		
	if request.user.is_authenticated():
		username = request.user.username
	else:
		username = "None"
	return render(request,'edit_article.html',{"typelist":typelist,
			"username":username,
			"authorlist":authorlist,
			"taglist":taglist,
			"tagselect":taglistselect,
			"post_data":post_data})

def add_comment(request):
	if request.method == "POST":
		user = request.POST['username']
		email = request.POST['email']
		message = request.POST['message']
		getid = request.POST['id']
		article = Article.objects.get(id=getid)
		newcomment = Comment()
		newcomment.user = user
		newcomment.email = email
		newcomment.content = message
		newcomment.blog = article
		newcomment.save()
		
		return HttpResponseRedirect( '/article/?id=%s' % getid )
		
		
		
	

