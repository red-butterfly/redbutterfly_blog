from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(blogtype)
admin.site.register(Article)
admin.site.register(Comment)
