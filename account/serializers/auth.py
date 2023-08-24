from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from utils import  custom_exceptions
from utils import validators,convertXslsTOJson
from ..models import auth as auth_models
from .. models import user as user_models
from account.serializers import user as user_related_serializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from utils.custom_exceptions import CustomError
from django.db import connection
from account.task import regiter_user_to_chat,charge_new_member_dues__fornimn
from account import task as acct_task

# this gets tge current user model which has been set in the setting useing "AUTH_USER_MODEL"
User = get_user_model()


class EmailValidateSerializer(serializers.Serializer):
    key = serializers.CharField(min_length=10)

    
class ExtraAuthFucntionMixin:

    def userExists(self,email:str):
        "if the user entered email let check if the exist if yes tell them that the user exist"
        if (not email):
            raise custom_exceptions.CustomError({"error":"Email is missing"})
        if(User.objects.filter(email=email).exists()):
            raise custom_exceptions.CustomError({"error":"Email Exists Already"})
        pass
         

class RegisterAdminUser(ExtraAuthFucntionMixin,serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    matric_number= serializers.CharField()


    def create(self, validated_data):
        return  User.objects.create_superuser(
            email = validated_data.get("email"),
            password =  validated_data.get("password"),**{"first_name":validated_data.get("first_name"),
                                                          "last_name":validated_data.get("last_name"),
                                                          'matric_number':validated_data.get('matric_number')
                                                          })
            
    def validate(self, attrs):
        self.userExists(attrs.get('email'))
        return super().validate(attrs)     

    class Meta:
        required_fields =['email','first_name','last_name']

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)
    company_name = serializers.CharField(required=False,trim_whitespace=True)
    matric_number = serializers.CharField()
    def validate(self, attrs):
        # here we would check if the email and password
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")
        company_name= attrs.get('company_name','')
        matric_number = attrs.get('matric_number')
        user =None

        try:
            user = User.objects.get(matric_number=matric_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error':'User Does Not Exist'},)


        auth_user = authenticate(matric_number=matric_number, password=password)
        if  user.is_active==False:
            raise serializers.ValidationError({'error':'please check your mail for verification'})

        if not auth_user:
            raise serializers.ValidationError({"error":'Invalid Credentials'})
        
        # UserMemberInfo
        if user.user_type == 'members':
            'here we validate his company namme'
            member = user_models.Memeber.objects.get(user=user)
            comapanyName = user_models.UserMemberInfo.objects.filter(member=member,name='names',).first()
            if comapanyName.value != company_name.strip():
                raise custom_exceptions.CustomError({'error':'member does not belong to this company'})
        attrs['user']=auth_user
        return attrs



class UploadSecondLevelDataBaseSerializer(serializers.Serializer):
    file = serializers.FileField()

    
    def create(self, validated_data):
        dataBaseFile = validated_data.get('file')
        # no matter what we set the id  to 13 and filll the data with json this would avoid two objects in dataBase
        secDb,created = auth_models.SecondLevelDatabase.objects.get_or_create(
            id=13,
        )
        # convertXslsTOJson this convert file to json format
        
        
        secDb.data=json.dumps(convertXslsTOJson.run(file=dataBaseFile),indent=4, sort_keys=True, default=str)
        # secDb.data=convertXslsTOJson.run(file=dataBaseFile)
        secDb.save()

        return validated_data

    def validate_file(self, file):
        validators.validate_file_extension_for_xlsx(file)
        return file

class UploadAndCreateMembersSerializer(serializers.Serializer):
    file = serializers.FileField()


    def serializeUpload(self,dataBaseFile):
        return convertXslsTOJson.run(file=dataBaseFile)
    def create(self, validated_data):
        dataBaseFile = validated_data.get('file')
        data= self.serializeUpload(dataBaseFile)
        allUserinfo = data.get('usersInfo')
        for eachUser in allUserinfo:
            password= str(eachUser.pop('password',1234567))
            MEMBERSHIP_NO = eachUser.get('MEMBERSHIP_NO')
            email = eachUser.get('email')
            alumni_year =  '2023-08-3'
            if MEMBERSHIP_NO is None: raise CustomError({'error':'Please MEMBERSHIP_NO is missing'})

            if user_models.UserMemberInfo.objects.filter(value=MEMBERSHIP_NO).exists():
                raise CustomError({'error':'Membership info has been registered already'})
            userDBData = eachUser

            chapter=None
            chapter_instance=None
            for key in userDBData.keys():
                if key == 'chapter':
                    chapter = userDBData[key]
            if get_user_model().objects.filter(email=email).exists():raise CustomError({'error':'email already exists'})

            if chapter:
                if  auth_models.Chapters.objects.filter(name__icontains=chapter):
                    chapter_instance = auth_models.Chapters.objects.filter(name__icontains=chapter).first()


        user = get_user_model().objects.create_user(
            email=email,
            user_type='members',
            password =password,
            
        )
        user.is_active=True
        user.save()
        if chapter_instance:
            "we going to add chapters if there is"
            # user.chapter  = chapter_instance
            user.save()
            chapter_instance.user.add(user)
            chapter_instance.save()

        member = user_models.Memeber.objects.create(
            user =user,
            alumni_year=alumni_year
        )
        for key in userDBData.keys():
            if not key =='password' and  not key == 'alumni_year':
                user_models.UserMemberInfo.objects.create(
                    name= key,
                    value= userDBData[key],
                    member=member
                )   
        charge_new_member_dues__fornimn.delay(user.id)
        if connection.schema_name == 'man':
            for key in userDBData.keys():
                if key == 'SECTOR':
                    exco_name = userDBData[key]
                    acct_task.group_MAN_subSector_and_sector.delay(
                        exco_name,member.id,type='sector'
                    )
                if key == 'SUB-SECTOR':
                    exco_name = userDBData[key]
                    acct_task.group_MAN_subSector_and_sector.delay(
                        exco_name,member.id,type='sub-sector'
                    )

        return dict()


class AdminManageCommiteeGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    members_list =serializers.ListField(required=False)
    team_of_reference =serializers.FileField(required=False)
    commitee_todo =  serializers.JSONField(required=False)
    commitee_duties =  serializers.JSONField(required=False)
    connected_members = serializers.SerializerMethodField()

    def validate(self, attrs):
        # print(attrs.get('members_list'),"memebsrr")
        # let valid the members if they actually exists in the db
        if( attrs.get('members_list') is not  None):
            for member_id in attrs.get('members_list'):
                if not user_models.Memeber.objects.all().filter(id=member_id).exists():
                    raise serializers.ValidationError({"error":f'this member id "{member_id}" is invalid'})
            
        return super().validate(attrs)

    def create(self, validated_data):
        "this helps to create a commitee"
        name = validated_data.get('name')
        members =validated_data.get('members_list')
        team_of_reference =validated_data.get('team_of_reference')
        commitee_todo =  validated_data.get('commitee_todo')
        commitee_duties= validated_data.get('commitee_todo')

        group ,_= user_models.CommiteeGroup.objects.get_or_create(
            name = name,
            # members=members,
            team_of_reference=team_of_reference,
            commitee_todo=commitee_todo,
            commitee_duties=commitee_duties,
        )
        group.save()
        for member_id in members:
            curentmember  =  user_models.Memeber.objects.get(id=member_id)
            print(curentmember,"curentmember")
            group.members.add(curentmember)
        # 'find a way to filter by multiple item in a list'
        # if len(members)!=0:
            
        #     group.members.set(list(user_models.Memeber.objects.filter(id=members[0])))

        group.save()
        return group

    def update(self, instance, validated_data):
        'this helps update a commitee'
        # if(user_models.CommiteeGroup.objects.filter(id=))
        instance.name = validated_data.get('name',instance.name)
        instance.team_of_reference =validated_data.get('team_of_reference',instance.team_of_reference)
        instance.commitee_todo =  validated_data.get('commitee_todo',instance.commitee_todo)
        instance.commitee_duties =  validated_data.get('commitee_duties',instance.commitee_duties)
        instance.save()
        return instance


    def get_connected_members(self,obj):
        members = []
        if self.context.get('detail',False):
            members = obj.members.all()
            clean_data = user_related_serializer.MemberSerializer(instance=members,many=True)
            return clean_data.data
        else:return[]

    class Meta:
        model = user_models.CommiteeGroup
        fields = ['id','name','members_list','team_of_reference','commitee_todo','connected_members','commitee_duties']
        
        write_only_fields = ['members_list',]
        read_only_fields = ['id']


class AdminManageCommiteePostion(serializers.ModelSerializer):
    
    memberId = serializers.IntegerField(required=False)
    def create(self, validated_data):
        member_id = validated_data.get('memberId',None)
        commitee_group=validated_data.get('commitee_group')
        print({'member_id':member_id})


        postion ,created=user_models.CommiteePostion.objects.get_or_create(
            commitee_group=commitee_group,
            name_of_postion=validated_data.get('name_of_postion'),
            duties=validated_data.get('duties'),
        )
        postion.save()

        if not user_models.CommiteeGroup.objects.filter(id=commitee_group.id,members=member_id).exists():
            member_id=None
        if(member_id is not None):
            member =user_models.Memeber.objects.get(id=member_id)
            postion.member=member
        postion.save()
        return postion

    class Meta:
        model = user_models.CommiteePostion
        fields= '__all__'


class ManageChapters(serializers.ModelSerializer):

    class Meta:
        model = auth_models.Chapters
        fields= '__all__'