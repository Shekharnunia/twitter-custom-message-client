from django.contrib import admin
from .models import TwitterAuth, SearchKeyWords, StatusUrls

admin.site.register(TwitterAuth)

admin.site.register(SearchKeyWords)

admin.site.register(StatusUrls)