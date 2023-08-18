from rest_framework import serializers
from . import models
from utils.custom_exceptions import CustomError
from account.models.user import User,UserMemberInfo
from django.shortcuts import get_object_or_404
from account.serializers.user import MemberSerializer
import json

class AdminManageMeetingSerializer(serializers.ModelSerializer):
    invitees = serializers.ListField(child=serializers.CharField(),write_only=True)

    def get_invitees(self,instance):
        'does not return anything it only a write field'
        return None     
    def create(self, validated_data):
        # invitees are the list of names
        print(validated_data)
        list_of_invitee = validated_data.pop('invitees',[])

        meeting = models.Meeting.objects.create(
            **validated_data
        )
        for companyName in list_of_invitee:
            companyInfo = UserMemberInfo.objects.filter(value=companyName)
            if companyInfo.exists() and companyInfo.first():
                print('Went ',companyName)
                models.MeetingAttendies.objects.create(
                    meeting = meeting,
                    members=companyInfo.first().member
                )
        return meeting
    
    class Meta:
        model = models.Meeting
        fields = '__all__'
        extra_kwargs  = {
            'chapters':{
                'read_only':True
            },
           
        }
        write_only_fields=['invitees']

class MeetingSerializer(serializers.ModelSerializer):
    is_attending= serializers.SerializerMethodField()
    is_authorized = serializers.SerializerMethodField()
    def get_is_attending(self,instance:models.Meeting):
        user = self.context.get('user',None)
        if user.user_type !='members':
            return False
        if user is None: return False
        is_attending = instance.meetingattendies_set.filter(members=user.memeber).exists()
        return is_attending

    def get_is_authorized(self,instance:models.Meeting):
        user = self.context.get('user',None)
        if user.user_type !='members':
            return False
        member = user.memeber
        if instance.exco is not None:
            if instance.exco.member.filter(id=member.id).exists():
                return True
            else:
                return False
        return True

    class Meta:
        model = models.Meeting
        fields = '__all__'

class MeetingProxyAttendiesSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
class MeetingRegister(serializers.Serializer):
    meeting = serializers.IntegerField()
    proxy_participants = MeetingProxyAttendiesSerializer(many=True,required=False)

    def create(self, validated_data):
        memeber = self.context.get('user').memeber
        meeting =get_object_or_404( models.Meeting,id=validated_data.get('meeting',-1))
        proxy_participants = validated_data.get('proxy_participants',[])
        if models.MeetingAttendies.objects.filter(meeting=meeting,members=memeber).exists(): raise CustomError({'error':'You have registered already'})

        meeting_attendies = models.MeetingAttendies.objects.create(
            meeting=meeting
            ,members=memeber)
        if len(proxy_participants)!=0:
            models.MeetingProxyAttendies.objects.get_or_create(
                participants= proxy_participants,
                meeting= meeting,
                member=memeber
            )

        return meeting_attendies


class MeetingApologies(serializers.Serializer):
    meeting = serializers.IntegerField()
    note= serializers.CharField()


    def create(self, validated_data):
        memeber = self.context.get('user').memeber
        note = validated_data.get('note','Am sorry i can attend')
        meeting =get_object_or_404( models.Meeting,id=validated_data.get('meeting',-1))
        if models.MeetingApology.objects.filter(meeting=meeting,members=memeber).exists():
            raise CustomError({'error':'You have Sent an apology already'})

        meeting_nonattenders = models.MeetingApology.objects.create(
            meeting=meeting
            ,members=memeber,
            note=note 
            )

        return meeting_nonattenders


class NonattendersMeetingMembersSerializer(serializers.ModelSerializer):
    memeber = serializers.SerializerMethodField()
    def get_memeber(self,meeting_apology:models.MeetingApology):
        clean_data = MemberSerializer(instance=meeting_apology.members,many=False)
        return clean_data.data
    
    

    class Meta:
        model = models.MeetingApology
        fields = ['memeber','id','note','meeting']


class RegisteredMeetingMembersSerializer(serializers.ModelSerializer):
    proxy_participants = serializers.SerializerMethodField()
    memebers = serializers.SerializerMethodField()
    def get_memebers(self,meeting):
        # 
        def clean(d):return d.members
        members = map(clean,models.MeetingAttendies.objects.filter(meeting=meeting))
        serializer = MemberSerializer(instance=members,many=True)
        return serializer.data
    def get_proxy_participants(self,instance:models.Meeting):
        try:
            meeting_proxy_attendies = models.MeetingProxyAttendies.objects.get(meeting=instance)
            return meeting_proxy_attendies.participants
        except:
            return []

    class Meta:
        model = models.Meeting
        fields = [
            'name','date_for','memebers','proxy_participants'
        ]


