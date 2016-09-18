# -*- coding: UTF-8 -*-
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import JsonResponse
from .models import * 
from redpackage.aboutsys.getsysinfo import *
from django.core.cache import cache
from django.conf import settings
from markdown import markdown

# Create your views here.

def articlelist(request):
	return render(request,'article_list.html')
	
def article(request):
	gettitle = request.GET['title']
	article = Article.objects.get(title=gettitle)
	articleinfo = {}
	taglist = []
	articleinfo['title'] = article.title
	articleinfo['content'] = markdown(article.content)
	articleinfo['date'] = article.last_mod_time
	for tmp in article.tags.all():
		taglist.append(tmp.tagname)
	return render(request,'article.html',{"articleinfo":articleinfo,
		"taglist":taglist})
	
def edit_article(request):
	typelist = []
	authorlist = []
	taglist = []
	taglistselect = []
	post_data = {}
	tagQS = []
	if request.method == 'POST':
		post_data['title'] = request.POST['article_title']
		post_data['type'] = request.POST['article_type']
		post_data['author'] = request.POST['article_author']
		post_data['tag'] = request.POST.getlist('article_tag')
		post_data['content'] = request.POST['article_content']
		post_data['summary'] = request.POST['article_summary']
		post_data['isre'] = request.POST['article_isre']
		post_data['readtimes'] = request.POST['article_readtimes']
		
		typeQS = blogtype.objects.get(typename=post_data['type'])
		authorQS = User.objects.get(username=post_data['author'])
		isre_value = 0
		if post_data['isre'] == 'on':
			isre_value = 1

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
		newArt.save()
		for tmp in post_data['tag']:
			tagtmp = Tag.objects.get(tagname=tmp)
			tagtmp.tagcount = tagtmp.tagcount + 1
			tagtmp.save()		
			newArt.tags.add(Tag.objects.get(tagname=tmp))
		return HttpResponseRedirect( '/article/?title=%s' % post_data['title'] )
		
		
	elif request.method == 'GET':
		for typetmp in blogtype.objects.all():
			typelist.append(typetmp.typename)
		for authortmp in User.objects.all():
			authorlist.append(authortmp.username)
		for tagtmp in Tag.objects.all():
			taglist.append(tagtmp.tagname) 
		if 'title' in request.GET:
			gettitle = request.GET['title']
			article = Article.objects.get(title=gettitle)
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
		
	return render(request,'edit_article.html',{"typelist":typelist,
			"authorlist":authorlist,
			"taglist":taglist,
			"tagselect":taglistselect,
			"post_data":post_data})
	

