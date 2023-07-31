from django.utils.encoding import force_str
# from firebase_admin import credentials, messaging
from urllib import parse
import random
import string
from django.utils.encoding import force_str



def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[force_str(key)] = [force_str(val)]
    query = parse.urlencode(sorted(query_dict.items()), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def generate_n(number:int=10):
    "helps u generate random char that are unqiue"
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(number))




def paystackLikeResponse(link:str):
    return {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "authorization_url": link,
                "access_code": "",
                "reference": ""
            }
        }

# def send_push_notification(registration_token, title, message):
#     # Create a message
#     notification = messaging.Notification(title=title, body=message)
#     message = messaging.Message(
#         notification=notification,
#         token=registration_token,
#     )

#     # Send the message
#     response = messaging.send(message)
#     print('Push notification sent:', response)




# def send_push_multiple_notifications(tokens, title, body):
#     # Create a MulticastMessage with the notification details
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=body
#         ),
#         tokens=tokens
#     )

#     # Send the notification
#     response = messaging.send_multicast(message)
#     print('Successfully sent notifications:', response.success_count)

# Usage example
# tokens = ['token1', 'token2', 'token3']
# send_push_multiple_notifications(tokens, 'Notification Title', 'Notification Body')
