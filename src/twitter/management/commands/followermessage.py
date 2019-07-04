import tweepy
from django.core.management.base import BaseCommand

from twitter.models import TwitterAuth, Followers

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
            me = api.me()
            
            followers = me.followers()
            followers_user_id = [(i.id,i.screen_name) for i in followers]

            database_followers = Followers.objects.all()
            if len(database_followers) == 0:
                for i in followers_user_id:
                    try:
                        Followers.objects.create(screen_name = i[1], user_id = i[0]).save()
                    except:
                        pass
            else:
                database_followers_user_id = [i.user_id for i in database_followers]
                new_followers = []
                for i,element in enumerate([x[0] for x in followers_user_id]):
                    if element not in database_followers_user_id:
                        new_followers.append(followers_user_id[i])

                if len(new_followers) != 0:
                    for i in new_followers:
                        self.send_message(i[0], 'hey how are you')
                        try:
                            Followers.objects.create(screen_name = i[1], user_id = i[0]).save()
                        except:
                            pass


    def send_message(self, id,message):
        event = {
          "event": {
            "type": "message_create",
            "message_create": {
              "target": {
                "recipient_id": f'{id}'
              },
              "message_data": {
                "text": message
              }
            }
          }
        }
        api.send_direct_message_new(event)
