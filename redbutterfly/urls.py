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
from red import index_views,article_views
from django.conf.urls import handler404,handler500

handler404 = "red.views.page_not_found"
handler500 = "red.views.page_error"

urlpatterns = [
	url(r'^$', index_views.index, name='index'),
	url(r'^login/$', index_views.login, name='login'),
	url(r'^article/$', article_views.article, name='article'),
	url(r'^article/setting/$', article_views.edit_article, name='edit_article'),
	url(r'^articlelist/$', article_views.articlelist, name='articlelist'),
	url(r'^articlelist/setting/$', article_views.articlelist_edit, name='articlelist_edit'),
	url(r'^comments/$', article_views.add_comment, name='add_comment'), 
	url(r'^sysinfo/$',index_views.sysinfo, name='sysinfo'),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^admin/', admin.site.urls),
	
]
