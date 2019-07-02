import time
import datetime

import tweepy
from django.core.management.base import BaseCommand

from twitter.models import TwitterAuth, SearchKeyWords, StatusUrls

auth = TwitterAuth.objects.first()

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
            print(keywords)
            if keywords: 
                for j in keywords:
                    today = datetime.datetime.today()
                    c = tweepy.Cursor(api.search, q=j.keyword, until=f'{today.year}-{today.month}-{today.day}', count=200, result_type='recent')
                    for i in c.items():
                        url = f"https://twitter.com/{i.user.screen_name}/status/{i.id}"
                        created_at = i.created_at
                        tweet = i.text
                        StatusUrls.objects.create(url=url, tweet=tweet, created_at=created_at, keyword=j).save()
                        print(url)
            print('going for sleeping')
            time.sleep(120)


# c = tweepy.Cursor(api.search, q='physician burnout', until='2019-07-02', count=200, result_type='recent')



# a = api.rate_limit_status()
# a
# a['resources']['search']

# j = []
# c = tweepy.Cursor(api.search, q="physician burnout", until='2019-06-28', since_id = '1144374824736907269')
# for i in c.items():
#   print(f"https://twitter.com/{i.user.screen_name}/status/{i.id}")
#   j.append(i)

# j[0].id
