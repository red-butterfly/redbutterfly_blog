# -*- coding: UTF-8 -*-
from django.contrib.auth import logout as auth_logout
from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.views.decorators.http import require_GET

from util.decorators import inc_pageviews, PAGEVIEWS_KEY
from util.redis_util import getmyredis
from util.sysinfo_util import get_sysinfo
from red.util_article import ArticleUtil
from red.util_user import UserUtil


def page_not_found(request):
    return render(request, '404.html')


def page_error( request ):
    return render(request, '500.html')


@inc_pageviews
def index(request):
    info = {}
    info['crt'] = getmyredis().get(PAGEVIEWS_KEY)
    info['articleNum'] = ArticleUtil.getcount()
    info['comments'] = ArticleUtil.getcommentcount()
    info['newtask'] = 0

    articles_line = ArticleUtil.getlist(end=6)
    username = request.user.username if request.user.is_authenticated() else "None"

    return render_to_response('index.html', {"username":username, "sysinfo":get_sysinfo(), "info":info,
                                             "articles_line":articles_line})


def login(request):
    """
    used to user login, there have three method:
    1:login;
    2:forget the password;
    3:register the user;
    """
    auth_logout(request)
    if request.method == 'POST':
        if 'login_input' in request.POST:
            ok, result = UserUtil.login(request)
            if ok:
                return HttpResponseRedirect(result)
            else:
                return render(request, 'page_user_login.html', result)

        elif 'register_input' in request.POST:
            return render(request, 'page_user_login.html', UserUtil.register(request))

        elif 'email_forget' in request.POST:
            print 'OK'
    elif request.method == 'GET':
        login_alert = u"请输入用户名密码"
        return render(request, 'page_user_login.html',{"login_alert":login_alert})
    else:
        raise Http404()


@require_GET
def sysinfo(request):
    return JsonResponse(get_sysinfo())

