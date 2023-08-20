from rest_framework import serializers
from . import models
from utils.notification import NovuProvider
from account.models.user import User,UserMemberInfo,ExcoRole,CommiteeGroup
import asyncio


class  LastestUpdatesAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LastestUpdates
        fields = '__all__'


class  LastestUpdatesMemberSerializer(serializers.ModelSerializer):
    def create(self, validated_data):return None
    def update(self, instance, validated_data):return None


    class Meta: 
        model = models.LastestUpdates
        fields = '__all__'


class IndividaulNotification(serializers.Serializer):
    names = serializers.ListField(child=serializers.CharField())
    title = serializers.CharField()
    message = serializers.CharField()


    def create(self, validated_data):
        novu = NovuProvider()
        user_ids = []
        title= validated_data['title']
        content= validated_data['message']
        for companyName in validated_data['names']:
            companyInfo = UserMemberInfo.objects.filter(value=companyName)
            if companyInfo.exists() and companyInfo.first():
                user_ids.append(f'{companyInfo.first().member.user.id}')
                # asyncio.run(
                # )

        novu.send_notification(
        name='on-boarding-notification',
        sub_id=user_ids,
        title=title,
        content=content)
        return dict()



class NotificationByTopicSerializer(serializers.Serializer):
    type = serializers.CharField()#e.g exco 
    title = serializers.CharField()
    content = serializers.CharField()
    id = serializers.IntegerField()

    def create(self, validated_data):
        type = validated_data['type']
        title = validated_data['title']
        content = validated_data['content']
        id = validated_data['id']
        novu = NovuProvider()
        user_ids = []
        if type =='exco':
            exco = ExcoRole.objects.get(id=id)
            for member in exco.member.all():
                user_ids.append(f'{member.user.id}')

        if type =='commitee':
            commitee = CommiteeGroup.objects.get(id=id)
            for member in commitee.members.all():
                user_ids.append(f'{member.user.id}')

        novu.send_notification(
            name='on-boarding-notification',
            sub_id=user_ids,
            title=title,
            content=content
        )
        return dict()