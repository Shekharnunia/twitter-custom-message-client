from django.db import models

class TwitterAuth(models.Model):
    consumer_key = models.CharField(max_length=50)
    consumer_secret = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    access_token_secret = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "TwitterAuth"
        verbose_name_plural = "TwitterAuth"
            

class SearchKeyWords(models.Model):
    keyword = models.CharField(max_length=50)
    since_id = models.CharField(max_length=30, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "SearchKeyWords"
        verbose_name_plural = "SearchKeyWords"
            

    def __str__(self):
        return self.keyword


class StatusUrls(models.Model):
    url = models.CharField(max_length=250, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    tweet = models.CharField(max_length=350)
    keyword = models.ForeignKey(SearchKeyWords, blank=True, null=True, on_delete=models.SET_NULL)
    retweet = models.BooleanField(default=False, help_text='If this field is green means that you already have retweeted ')
    favorites = models.BooleanField(default=False, help_text='If this field is green means that you already have marked it as your favorites ')

    class Meta:
        verbose_name = "StatusUrls"
        verbose_name_plural = "StatusUrls"


    def __str__(self):
        return self.url


class Followers(models.Model):
    screen_name = models.CharField(max_length=20, unique=True)
    user_id = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"

    def __str__(self):
        return self.screen_name