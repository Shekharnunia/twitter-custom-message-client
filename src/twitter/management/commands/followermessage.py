import time
import tweepy
from django.core.management.base import BaseCommand

from twitter.models import TwitterAuth, FollowerDetail

auth = TwitterAuth.objects.first()

consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret
access_token = auth.access_token
access_token_secret = auth.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


# put followers names in database and get all followers detail from api, 
# then compare them with database that who is new and who is not

class Command(BaseCommand):
    help = 'Runs my special command'

    def handle(self, *args, **options):
        while True:
            me = api.get_user(screen_name='shekharnunia')
            c = tweepy.Cursor(api.followers, screen_name=f"{me.screen_name}")

            follower_detail_for_last_time = FollowerDetail.objects.last()

            followers_count = follower_detail_for_last_time.last_time_follower_count
            last_ten_followers = follower_detail_for_last_time.last_ten_followers

            list_of_last_ten_follower = last_ten_followers.split(',')
            
            limit = me.followers_count - followers_count
            if limit <= 0:
                limit = 20
            for i in c.items(limit):
                new_list_of_follower.append(i.screen_name)
                print(f"{i.screen_name}")
            time.sleep(30)





# def getFollower(profile):
#     i = 0
#     l = []
#     printColour("\n[*] ", BLUE)
#     print "Follower list:\n"
#     for user in tweepy.Cursor(api.followers, screen_name=profile, count=200).items():
#         try:
#             l.append(user.screen_name)
#             i = i + 1
#         except:
#             print "[-] Timeout, sleeping for 15 minutes..."
#             time.sleep(15*60)
#     for user in l:
#         printColour("[+] @" + user, GREEN)
#         print(" (https://www.twitter.com/" + user + ")\n")
#     printColour("\n[*] ", CYAN)
#     print "Total follower: " + str(len(l)-1) + "\n" 