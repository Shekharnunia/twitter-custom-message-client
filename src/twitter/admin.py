from django.utils.html import mark_safe

from django.contrib import admin
from .models import TwitterAuth, SearchKeyWords, StatusUrls

admin.site.register(TwitterAuth)

admin.site.register(SearchKeyWords)


class StatusUrlsAdmin(admin.ModelAdmin):
    list_display = ("keyword", 'tweet', 'created_at')
    list_filter = ("keyword",)
    search_fields = ("tweet",)
    readonly_fields = ("tweet", 'url', 'created_at', 'keyword', 'url_link',)
    exclude = ('sent',)

    # exclude = ('browser', 'screenshot')
    # ordering = ("-created",)
    # date_hierarchy = 'created'
    class Meta:
        model = StatusUrls

    def url_link(self, statusurls):
        return mark_safe('<a href="%s">Click this to go to the tweet page</a>' % (statusurls.url))
    url_link.short_description = 'Tweet Url'
    url_link.allow_tags = True


admin.site.register(StatusUrls, StatusUrlsAdmin)