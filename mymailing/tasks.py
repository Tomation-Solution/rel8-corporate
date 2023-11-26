from celery import shared_task
from django.contrib.auth import get_user_model

from .EmailConfirmation import activateEmail,sendInvitationMail, sendPublicationMailApi
from django.template.loader import render_to_string

from event.models import Event,EventProxyAttendies
from mymailing.views import send_mail
from django.db import connection
import os

# @shared_task()
def send_activation_mail(user_id,to_email):
    user = get_user_model().objects.get(id=user_id)
    activateEmail(user,to_email)

# @shared_task()
def send_event_invitation_mail(user_id,event_id,event_proxy_attendies_id):
    user = get_user_model().objects.get(id=user_id)
    event =Event.objects.get(id=event_id)
    event_proxy_attendies= EventProxyAttendies.objects.get(id=event_proxy_attendies_id)
    sendInvitationMail(
        user=user,
        event=event,
        event_proxy_attendies=event_proxy_attendies
    )


# @shared_task
def send_publication_downloadlink(link,email,title):
     sendPublicationMailApi(link,email,title)


@shared_task
def sendRemarkNotification(to_email,remark):
    message = render_to_string('prospective_remark_body.html',context={
        'remark':remark
    })
    domain_mail = os.environ['domain_mail']
    domain = connection.schema_name+'.'+os.environ['domain']
    if connection.schema_name == 'nimn':
        # domain_mail='rel8@members.nimn.com.ng'
        domain = 'https://members.nimn.com.ng'
    print (
        {to_email,domain_mail}
    )
    send_mail(
        subject='Man Application Remark',
        sender={'email':domain_mail,'name':'MAN'},
        to=[{"email":to_email,"name":"rel8"}],html_content=message,)
