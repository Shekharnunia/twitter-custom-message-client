from django.contrib import admin
from django.utils.html import mark_safe

import decimal, csv
from django.http import HttpResponse

from .models import TwitterAuth, SearchKeyWords, StatusUrls, Followers


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
    list_display = ("keyword", 'tweet', 'created_at')
    list_filter = ("keyword", 'created_at')
    search_fields = ("tweet", 'url')
    readonly_fields = ("tweet", 'url', 'created_at', 'keyword', 'url_link',)
    exclude = ('sent',)
    ordering = ('-id',)
    actions = [export_status, ]


    class Meta:
        model = StatusUrls

    def url_link(self, statusurls):
        return mark_safe('<a href="%s">Click this to go to the tweet page</a>' % (statusurls.url))
    url_link.short_description = 'Tweet Url'
    url_link.allow_tags = True


admin.site.register(StatusUrls, StatusUrlsAdmin)

admin.site.register(TwitterAuth)

admin.site.register(SearchKeyWords)

admin.site.register(Followers)