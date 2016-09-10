"""redbutterfly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from red import views as red_views
from django.conf.urls import handler404,handler500

handler404 = "red.views.page_not_found"
handler500 = "red.views.page_error"

urlpatterns = [
	url(r'^$', red_views.index, name='index'),
	url(r'^login/$', red_views.login, name='login'),
	url(r'^sysinfo/$',red_views.sysinfo, name='sysinfo'),
	url(r'^admin/', admin.site.urls),
]
