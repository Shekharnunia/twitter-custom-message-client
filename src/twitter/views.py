import tweepy

from django.shortcuts import render, redirect

from twitter.models import TwitterAuth

auth = TwitterAuth.objects.first()

consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret
access_token = auth.access_token
access_token_secret = auth.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
my_id = api.me().id

def list_message(request, message_status=None):
    if request.method == 'GET':
        al = api.lists_all()
        list_slugs = []
        limit = api.rate_limit_status()
        list_remaining_limit = limit['resources']['lists']['/lists/list']['remaining']
        for i in al:
            list_slugs.append(i.slug)
        context = {
        	'user_lists' : list_slugs,
        	'list_remaining_limit' : list_remaining_limit,
        }
        return render(request, 'list_message.html', context)

    elif request.method == 'POST':
        slug = request.POST.get('list-slug')
        message = request.POST.get('message')

        if slug and message:
            context = send_message_to_list(slug=slug, message=message)

        if type(context) == dict:
            context['message_status'] = True
            return render(request, 'list_message.html', context)
        else:
            al = api.lists_all()
            list_slugs = []
            for i in al:
                list_slugs.append(i.slug)
            context = {
                'user_lists': list_slugs,
                'message_status' : False
            }
        return render(request, 'list_message.html', context)


def send_message(id,message):
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


def send_message_to_list(slug=None, message=None):
    try:
        new_list = api.list_members(slug=f'{slug}', owner_id=str(my_id))
    except:
        new_list = None
    if new_list is not None:
        sent_name = []
        unsent_name = []
        for i in new_list:
            try:
                send_message(i.id, message)
                sent_name.append(i.name)
            except:
                unsent_name.append(i.name)
        context = {
            'sent_names' : sent_name,
            'unsent_names' : unsent_name,
        }
        return context
    else:
        return False