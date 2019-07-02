import sys
import time
import datetime

import tweepy
from django.core.management.base import BaseCommand

from twitter.models import TwitterAuth, SearchKeyWords, StatusUrls

try:
    auth = TwitterAuth.objects.first()
except:
    sys.exit()

consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret
access_token = auth.access_token
access_token_secret = auth.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


class Command(BaseCommand):
    help = 'Runs my special command'

    def handle(self, *args, **options):
        while True:
            keywords = SearchKeyWords.objects.all()
            if keywords: 
                for j in keywords:
                    today = datetime.datetime.today()
                    try:
                        last_keyword_url = StatusUrls.objects.filter(keyword=j).order_by('-created_at').first()
                        print(last_keyword_url)
                    except:
                        since_id = ''
                    else:
                        if last_keyword_url is not None:
                            since_id = last_keyword_url.url.split('status/')[-1]
                        else:
                            since_id = ''
                    c = tweepy.Cursor(api.search, q=j.keyword, count=200, result_type='recent')
                    for i in c.items():
                        url = f"https://twitter.com/{i.user.screen_name}/status/{i.id}"
                        created_at = i.created_at
                        tweet = i.text
                        try:
                            StatusUrls.objects.create(url=url, tweet=tweet, created_at=created_at, keyword=j).save()
                            print(url)
                        except:
                            pass
                        # print(url)
            print('going for sleeping')
            time.sleep(10)
