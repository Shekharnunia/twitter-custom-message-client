from django.db import models

class TwitterAuth(models.Model):
    consumer_key = models.CharField(max_length=50)
    consumer_secret = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    access_token_secret = models.CharField(max_length=50)



class FollowerDetail(models.Model):
    last_time_follower_count = models.PositiveIntegerField(default=0)
    last_ten_followers = models.CharField(max_length=250)

    class Meta:
        verbose_name = "FollowerDetail"
        verbose_name_plural = "FollowerDetails"

    def __str__(self):
        return str(self.last_time_follower_count)



class SearchKeyWords(models.Model):
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword


class StatusUrls(models.Model):
    url = models.CharField(max_length=250, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.CharField(max_length=30)
    sent = models.BooleanField(default=False)
    tweet = models.CharField(max_length=350)
    keyword = models.ForeignKey(SearchKeyWords, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.url

# class Followers(models.Model):
#     screen_name = models.CharField(max_length=20)
#     user_id = models.PositiveIntegerField()

