from novu.config import NovuConfig
from novu.api.subscriber import SubscriberApi
from novu.dto.subscriber import SubscriberDto
from novu.api import EventApi, TopicApi
from novu.dto.topic import TriggerTopicDto
from django.utils.text import slugify
import os

class NovuProvider:

    def __init__(self) -> None:
        # Configure Novu API once during initialization
        self.api_key = os.environ.get('YOUR_NOVU_API_KEY')
        if not self.api_key:
            raise ValueError("API key is missing. Please set 'YOUR_NOVU_API_KEY' in environment variables.")
        self.config = NovuConfig().configure("https://api.novu.co", self.api_key)

    def make_man(self, user_ids):
        # Utility function to format user IDs
        return [f'{user_id}__man' for user_id in user_ids]

    def subscribe(self, user_id: int, email: str):
        # Subscribe a user to Novu
        subscriber = SubscriberDto(
            subscriber_id=f'{user_id}__man',
            email=email,
        )
        try:
            SubscriberApi().create(subscriber)
            print(f"Successfully subscribed user {user_id}.")
        except Exception as e:
            print(f"Failed to subscribe user {user_id}: {e}")

    def send_notification(self, name: str, sub_ids, title: str, content: str):
        # Send a notification to multiple subscribers
        try:
            EventApi().trigger(
                name=name,
                recipients=self.make_man(sub_ids),
                payload={"title": title, 'content': content}
            )
            print(f"Successfully sent notification '{name}' to subscribers {sub_ids}.")
        except Exception as e:
            print(f"Failed to send notification '{name}': {e}")

    def create_topic(self, name: str):
        # Create a topic in Novu
        key = slugify(name)
        try:
            TopicApi().create(key=key, name=name)
            print(f"Successfully created topic '{key}'.")
        except Exception as e:
            if hasattr(e, 'response') and e.response.status_code == 409:
                # Handle topic already existing
                print(f"Topic '{key}' already exists. Skipping creation.")
            else:
                print(f"Failed to create topic '{key}': {e}")
                raise

    def sub_user_to_topic(self, name: str, user_ids):
        # Subscribe users to a topic
        key = slugify(name)
        try:
            TopicApi().subscribe(
                key=key,
                subscribers=self.make_man(user_ids)
            )
            print(f"Successfully subscribed users {user_ids} to topic '{name}'.")
        except Exception as e:
            print(f"Failed to subscribe users to topic '{name}': {e}")

    def notify_by_topic(self, topic_name: str, title: str, content: str, workflow_name='on-boarding-notification'):
        # Send a notification to all subscribers of a topic
        topics = TriggerTopicDto(
            topic_key=slugify(topic_name),
            type="Topic",
        )
        try:
            EventApi().trigger_topic(
                name=workflow_name,  # The trigger ID of the workflow. It can be found on the workflow page.
                topics=topics,
                payload={"title": title, 'content': content}
            )
            print(f"Successfully notified topic '{topic_name}' with workflow '{workflow_name}'.")
        except Exception as e:
            print(f"Failed to notify by topic '{topic_name}': {e}")

# from novu.config import NovuConfig
# from novu.api.subscriber import SubscriberApi
# from novu.dto.subscriber import SubscriberDto
# from novu.api import EventApi
# import os,json
# from django.utils.text import slugify
# from novu.api import TopicApi
# from novu.api import EventApi
# from novu.dto.topic import TriggerTopicDto




# class NovuProvider:
#     def make_man(self,user_id):
#         return list(map(lambda x:f'{x}__man',user_id))


#     def __init__(self) -> None:
#         self.api_key= os.environ.get('YOUR_NOVU_API_KEY')

#     def connect(self):
#         api_key= os.environ.get('YOUR_NOVU_API_KEY')
#         n =NovuConfig().configure("https://api.novu.co", api_key)

#     def subscribe(self,userID:int,email:str,):
#         api_key= os.environ.get('YOUR_NOVU_API_KEY')
#         NovuConfig().configure("https://api.novu.co", api_key)
#         subscriber = SubscriberDto(
#         subscriber_id=f'{userID}__man',
#         email=email,)
#         SubscriberApi().create(subscriber)

#     def send_notification(self,name:str,sub_id,title,content):
#         api_key= os.environ.get('YOUR_NOVU_API_KEY')
#         n =NovuConfig().configure("https://api.novu.co", api_key)
#         print({
#             'sub':sub_id
#         })
#         EventApi().trigger(
#             name=name,  
#             recipients=self.make_man(sub_id),
#             payload={"title":title,'content':content}
#         )


#     def create_topic(self,name):
#         key = slugify(name)
#         self.connect()
#         TopicApi().create(key=key,name=name)

#     def sub_user_to_topic(self,name,user_ids):
#         self.connect()
#         key = slugify(name)
#         TopicApi().subscribe(key=key,
#                 subscribers=self.make_man(user_ids) )
        
#     def notify_by_topic(self,topicName,title,content,workflowName='on-boarding-notification'):
#         self.connect()
#         topics = TriggerTopicDto(
#         topic_key=slugify(topicName),
#         type="Topic",
#         )

#         EventApi().trigger_topic(
#         name=workflowName,  # The trigger ID of the workflow. It can be found on the workflow page.
#         topics=topics,
#         payload={"title":title,'content':content})