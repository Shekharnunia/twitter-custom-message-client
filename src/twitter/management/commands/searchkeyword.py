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
                    print(j)
                    c = tweepy.Cursor(api.search, q=j.keyword, since_id=j.since_id, count=200)

                    globals()[f'lst{j.keyword}'] = []
                    for i in c.items():
                        globals()[f'lst{j}'].append(i.id)
                        url = f"https://twitter.com/{i.user.screen_name}/status/{i.id}"
                        created_at = i.created_at
                        tweet = i.text
                        try:
                            StatusUrls.objects.create(url=url, tweet=tweet, created_at=created_at, keyword=j).save()
                        except:
                            pass
                    if len(globals()[f'lst{j}']) > 0:
                        j.since_id = str(globals()[f'lst{j}'][0])
                        j.save()
            print('going for sleeping')
            time.sleep(10)
