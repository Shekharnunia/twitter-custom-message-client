import csv
from django.contrib import messages

from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import mark_safe

from .models import TwitterAuth, SearchKeyWords, StatusUrls, Followers

import tweepy

def export_status(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="status.csv"'
    writer = csv.writer(response)
    writer.writerow(['URl', 'Created Date', 'Tweet', 'Keyword'])
    status = queryset.values_list('url', 'created_at', 'tweet', 'keyword__keyword')
    for stat in status:
        writer.writerow(stat)
    return response
export_status.short_description = 'Export to csv'


class StatusUrlsAdmin(admin.ModelAdmin):
    list_display = ('username', "keyword", 'tweet', 'created_at')
    list_filter = ("keyword", 'created_at')
    search_fields = ("tweet", 'url')
    readonly_fields = ('username', "tweet", 'url', 'created_at', 'keyword', 'url_link', 'retweet', 'favorites')
    exclude = ('sent',)
    ordering = ('-id',)
    actions = [export_status, ]
    actions_on_top = True
    change_form_template = "new_admin_form.html"


    class Meta:
        model = StatusUrls
    
    def response_change(self, request, obj):
        if "_retweet" in request.POST:
            try:
                auth = TwitterAuth.objects.first()
            except:
                self.message_user(request, "first add your AUTHENTICATION TOKEN in TwitterAuth section so that it can do other things", level=messages.ERROR)
                return HttpResponseRedirect(".")   

            consumer_key = auth.consumer_key
            consumer_secret = auth.consumer_secret
            access_token = auth.access_token
            access_token_secret = auth.access_token_secret

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True)

            status_id = obj.url.split('status/')[-1]

            try:
                ret = api.retweet(id=status_id)
            except:
                self.message_user(request, "You have already Retweeted this status or its twitter api problem", level=messages.ERROR)
                return HttpResponseRedirect(".")    
            obj.retweet = True
            obj.save()
            self.message_user(request, "You have successfully Retweeted this status")
            return HttpResponseRedirect(".")
        if "_favourite" in request.POST:
            try:
                auth = TwitterAuth.objects.first()
            except:
                self.message_user(request, "You first add your AUTHENTICATION TOKEN in TwitterAuth section so that it can do other things", level=messages.ERROR)
                return HttpResponseRedirect(".")    
            
            consumer_key = auth.consumer_key
            consumer_secret = auth.consumer_secret
            access_token = auth.access_token
            access_token_secret = auth.access_token_secret

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True)
            
            status_id = obj.url.split('status/')[-1]
            try:
                ret = api.create_favorite(id=status_id)
            except:
                self.message_user(request, "You have already made this status favorite or its twitter api problem", level=messages.ERROR)
                return HttpResponseRedirect(".")    
            obj.favorites = True
            obj.save()
            self.message_user(request, "You have successfully liked this status")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)    
        

    def url_link(self, statusurls):
        return mark_safe('<a href="%s">Click this to go to the tweet page</a>' % (statusurls.url))
    url_link.short_description = 'Tweet Url'
    url_link.allow_tags = True

    def has_add_permission(self, request):
        return False

    def username(self, statusurls):
        a = statusurls.url.split('/')
        if len(a) == 6:
        	return a[3]
        else:
        	return ''
    username.short_description = 'Username'
    username.allow_tags = True


admin.site.register(StatusUrls, StatusUrlsAdmin)

admin.site.register(TwitterAuth)

@admin.register(SearchKeyWords)
class SearchKeyWordAdmin(admin.ModelAdmin):
    exclude = ('since_id',)

admin.site.register(Followers)