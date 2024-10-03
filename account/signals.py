from account.models.user import User,ExcoRole,CommiteeGroup
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from mailing.models import EmailInvitation
from utils.unique_account_creation_key_generator import key_generator
from django.db import connection
from . import task
from Dueapp import models as due_models
from utils.notification import NovuProvider
# from mailing.tasks import send_activation_mail



@receiver(post_save,sender=ExcoRole)
def add_member_to_ExcoRole_group(sender,**kwargs):
    'this add or update exco topics so we can send notifcations or mail to a group of sectors e.t.c'
    isCreated = kwargs['created']
    exco = kwargs['instance']
    novu = NovuProvider()
    if isCreated:
        novu.create_topic(exco.name+'-exco')
    if exco.member:
        user_id = map(lambda member:f'{member.user.id}',exco.member.all())
        user_id =list(user_id)
        print({'user_id':user_id})
        novu.sub_user_to_topic(name=exco.name+'-excos',user_ids=user_id)



# @receiver(post_save,sender=CommiteeGroup)
# def add_member_to_Commitee_group(sender,**kwargs):
#     isCreated = kwargs['created']
#     commitee = kwargs['instance']
#     novu = NovuProvider()
#     if isCreated:
#         novu.create_topic(commitee.name+'--commitee')
#     if commitee.members:
#         user_id = map(lambda commite:f'{commite.user.id}',commitee.member.all())
#         user_id =list(user_id)
#         novu.sub_user_to_topic(name=commitee.name,user_ids=user_id)

@receiver(post_save, sender=CommiteeGroup)
def add_member_to_commitee_group(sender, **kwargs):
    is_created = kwargs['created']
    commitee = kwargs['instance']
    novu = NovuProvider()
    
    # Create topic when a new commitee group is created
    if is_created:
        novu.create_topic(commitee.name + '--commitee')
    
    # Subscribe members to the topic if there are members in the commitee group
    if commitee.members.exists():
        user_ids = [f'{member.user.id}' for member in commitee.members.all()]
        novu.sub_user_to_topic(name=commitee.name, user_ids=user_ids)