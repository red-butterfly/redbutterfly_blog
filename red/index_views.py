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

def page_not_found(request):
	return render(request,'404.html')

def page_error(request):
	return render(request,'500.html')

def index(request):
	if not cache.has_key('visit:index'):
		cache.set('visit:index',1,25)
		cache.persist('visit:index')
	else:
		cache.incr('visit:index')
		
	sysinfo = {}
	cpumeminfo = GetCpuMemInfo()
	sysinfo['cpuused'] = str(cpumeminfo[0])
	sysinfo['memused'] = str(cpumeminfo[3])
	sysinfo['diskused'] = str(GetDiskInfo()[2])	
	
	info = {}
	artclelist = Article.objects.all()
	info['crt'] = cache.get('visit:index')
	info['articleNum'] = len(artclelist)
	info['comments'] = 0
	info['newtask'] = 0
	
	articles_line1 = []
	articles_line2 = []
	for i,article in enumerate(artclelist):
		if i <= 2:
			articles_line1.append({"title":article.title,"summary":article.summary,"date":article.last_mod_time})
		elif i <= 5:
			articles_line2.append({"title":article.title,"summary":article.summary,"date":article.last_mod_time})
		else:
			break
			
	if request.user.is_authenticated():
		username = request.user.username
	else:
		username = "None"
		
	return render( request, 'index.html',{"username":username,
		"sysinfo":sysinfo,
		"info":info,
		"articles_line1":articles_line1,
		"articles_line2":articles_line2})

def login(request):
	"""
	used to user login, there have three method:
	1:login;
	2:forget the password;
	3:register the user;
	"""
	error = {} #the error info to display in the html
	auth_logout(request)
	if request.method == 'POST':
		if 'login_input' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			if 'remember' in request.POST:
				remember = request.POST['remember']
			else:
				remember = 0

			try:
				namefilter = User.objects.get(username=username)
				user = authenticate(username=username,password=password)
				if user is not None and user.is_active:
					auth_login(request,user)
					login_alert = u"登陆成功"	
					error['login_error'] = "False" 
					response = HttpResponseRedirect( '/' )
					return response
				else:
					login_alert = u"用户名或密码错误"	
					error['login_error'] = "True" 
					return render( request, 'page_user_login.html',{"error":error,'username_login':username,"login_alert":login_alert})
			except User.DoesNotExist:
				login_alert = u"用户不存在"	
				error['login_error'] = "True" 
				return render( request, 'page_user_login.html',{"error":error,'username_login':username,"login_alert":login_alert})
			
		elif 'register_input' in request.POST:
			fullname = request.POST['fullname']
			email = request.POST['email']
			address = request.POST['address']
			city = request.POST['city']
			country = request.POST['country']
			username_register = request.POST['username']
			password = request.POST['password']
			rpassword = request.POST['rpassword']	
			
			namefilter = User.objects.filter(username=username_register)
			emailfilter = User.objects.filter(email=email)
			
			if namefilter:
				error['nameerr'] = u"该用户名已经注册."
				
			if emailfilter:
				error['emailerr'] = u"该邮箱已经注册."

			if namefilter or emailfilter:
				error['register_error'] = "True"
				return render( request, 'page_user_login.html',{"error":error,
					"username_register":username_register,
					"fullname":fullname,
					"email":email,
					"address":address,
					"city":city,
					"country":country})
			else:
				user = User()
				user.username = username_register
				user.set_password(password)
				user.email = email
				user.first_name = fullname
				user.address = address
				user.city = city
				user.country =  country
				user.save()	
				return render( request, 'page_user_login.html',{"register_ok":u"注册成功,"})

		elif 'email_forget' in request.POST:
			print 'OK'
	
	login_alert = u"请输入用户名密码"	
	return render( request, 'page_user_login.html',{"login_alert":login_alert})

def sysinfo(request):
	sysinfo = {}
	cpumeminfo = GetCpuMemInfo()
	sysinfo['cpuused'] = str(cpumeminfo[0])
	sysinfo['memused'] = str(cpumeminfo[3])
	sysinfo['diskused'] = str(GetDiskInfo()[2])	

	return JsonResponse(sysinfo)

