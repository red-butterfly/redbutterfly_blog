# -*- coding: UTF-8 -*-
from red.models import User
from django.contrib.auth import authenticate,login as auth_login


class UserUtil(object):

    @staticmethod
    def login(request):
        error = {}
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST['remember'] if 'remember' in request.POST else 0 #TODO

        try:
            tmp = User.objects.get(username=username)
        except User.DoesNotExist:
            login_alert = u"用户不存在"
            error['login_error'] = "True"
            return False, {"error": error.copy(), 'username_login': username, 'login_alert':login_alert}
        else:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                try:
                    url = request.GET['next']
                except:
                    url = '/'
                return True, url

            else:
                login_alert = u"用户名或密码错误"
                error['login_error'] = "True"
                return False, {"error": error, 'username_login': username,  'login_alert':login_alert}

    @staticmethod
    def register(request):
        error = {}
        fullname = request.POST['fullname']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        country = request.POST['country']
        username_register = request.POST['username']
        password = request.POST['password']

        namefilter = User.objects.filter(username=username_register)
        emailfilter = User.objects.filter(email=email)

        if namefilter:
            error['nameerr'] = u"该用户名已经注册."
        if emailfilter:
            error['emailerr'] = u"该邮箱已经注册."

        if namefilter or emailfilter:
            error['register_error'] = "True"
            return {"error": error, "username_register": username_register, "fullname": fullname, "email": email,
                    "address": address, "city": city, "country": country}
        else:
            user = User()
            user.username = username_register
            user.set_password(password)
            user.email = email
            user.first_name = fullname
            user.address = address
            user.city = city
            user.country = country
            user.save()
            return {"register_ok": u"注册成功,"}