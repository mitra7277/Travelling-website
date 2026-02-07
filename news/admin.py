from django.contrib.admin.sites import site
from news.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
  list_display=('news_title', 'news_desc')
  
admin.site.register(News,NewsAdmin)


# Register your models here.
