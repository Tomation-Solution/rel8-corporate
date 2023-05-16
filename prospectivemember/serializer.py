from rest_framework import serializers
from .models import man_prospective_model
from django.contrib.auth import get_user_model as USER
from utils.custom_exceptions import  CustomError 
from mymailing import tasks as mymailing_task
from rest_framework.authtoken.models import Token
from Rel8Tenant import models as rel8tenant_related_models
import requests,json
from utils.usefulFunc import convert_naira_to_kobo
from prospectivemember.models.man_prospective_model import (ManProspectiveMemberProfile,RegistrationAmountInfo,
ManProspectiveMemberFormOne,ManProspectiveMemberFormTwo,Remark)
from utils.custom_response import Success_response
from rest_framework import status

class CreateManPropectiveMemberSerializer(serializers.ModelSerializer):

    def _process_paymentlink(self,request,user):

        schema_name = request.tenant.schema_name
        client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
        if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
            raise CustomError({'error':'Paystack not active please reach out to the developer'})
        PAYSTACK_SECRET = client_tenant.paystack_secret
        instance =None
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET}',
        'Content-Type' : 'application/json',
        'Accept': 'application/json',}
        reg = RegistrationAmountInfo.objects.all().first()
        if reg is None:
            raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
        instance = ManProspectiveMemberProfile.objects.get(user=user)
        member = instance
        amount_to_be_paid = reg.amount
        pk= instance.id
        if instance.has_paid:
            raise CustomError({'error':'Please hold for admin to process your info you have paid already'})

        body = {
            "email": user.email,
            "amount": convert_naira_to_kobo(amount_to_be_paid),
            "metadata":{
                "instanceID":pk,
                'member_id':member.id,
                "user_id":user.id,
                "forWhat":'prospective_member_registration',
                'schema_name':request.tenant.schema_name,
                'user_type':user.user_type,
                'amount_to_be_paid':str(amount_to_be_paid)
            },
            # "callback_url":settings.PAYMENT_FOR_MEMBERSHIP_CALLBACK,
            }

        try:
            resp = requests.post(url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if resp.status_code ==200:
            data = resp.json()
            instance.paystack_key= data['data']['reference']
            instance.save()
            return data

        raise CustomError(message='Some Error Occured Please Try Again',status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    

    def create(self, validated_data):
        email = validated_data.get('email',None)
        cac = validated_data.get('cac_registration_number')
        if USER().objects.filter(email=email).exists():
            raise CustomError({'error':'user email already exists'})
        user = USER().objects.create_user(
            email=email,
            password=cac,
            user_type='prospective_members'
        )
        user.is_active = True
        user.is_prospective_Member=True
        user.save()

        man_propective = man_prospective_model.ManProspectiveMemberProfile.objects.create(
            user=user,
            **validated_data
        )
        mymailing_task.send_activation_mail.delay(user.id,user.email)
       
       
        token,created =Token.objects.get_or_create(user=user)
        payment_info = self._process_paymentlink(self.context.get('request'),user)
        return {
                "user_type":user.user_type,
                'token':token.key,
                'has_paid':user.manprospectivememberprofile.has_paid,
                'prospective_member_id':user.manprospectivememberprofile.id,
                'payment_info':payment_info
            }
    class Meta:
        model  =man_prospective_model.ManProspectiveMemberProfile
        fields = '__all__'
        read_only_fields = ['user','paystack','has_paid']


class PropectiveMemberManageFormOneSerializer(serializers.ModelSerializer):
    prospective_member_payment_info = serializers.SerializerMethodField() 
    def create(self, validated_data):return None

    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormOne
        fields = '__all__'
        read_only_fields =['prospective_member']

    def get_prospective_member_payment_info(self,instance:man_prospective_model.ManProspectiveMemberFormOne):
        return {
            'application_payment':instance.prospective_member.has_paid,
            'has_paid_subcription':instance.prospective_member.has_paid_subcription
        }
class PropectiveMemberManageFormTwoSerializer(serializers.ModelSerializer):
    prospective_member_payment_info = serializers.SerializerMethodField() 

    def create(self, validated_data):return None
    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormTwo
        fields = '__all__'
        read_only_fields =['prospective_member']

    def get_prospective_member_payment_info(self,instance:man_prospective_model.ManProspectiveMemberFormTwo):
        return {
            'application_payment':instance.prospective_member.has_paid,
            'has_paid_subcription':instance.prospective_member.has_paid_subcription
        } 

class ProspectiveManMemberCleaner(serializers.ModelSerializer):
    form_one = serializers.SerializerMethodField()
    form_two = serializers.SerializerMethodField()


    def get_form_one(self,instance:ManProspectiveMemberProfile):
        form_one = ManProspectiveMemberFormOne.objects.filter(
            prospective_member=instance).values(
            'cac_registration_number','prospective_member','name_of_company','tax_identification_number',
            'corporate_office_addresse','office_bus_stop','office_city','office_lga','office_state',
            'postal_addresse','telephone','email_addresse','website','factoru_details','legal_status_of_company',
            'number_of_female_expatriates','number_of_male_expatriates',
            'number_of_male_permanent_staff',
            'number_of_female_permanent_staff',
            'local_share_capital',
            'foreign_share_capital',
            'ownership_structure_equity_local',
            'ownership_structure_equity_foregin',
            'total_value_of_land_asset',
            'total_value_of_building_asset',
            'total_value_of_other_asset',
            'installed_capacity',
            'current_sales_turnover',
            'projected_sales_turnover',
            'are_your_product_exported',
            'company_contact_infomation',
            'designation',
            'name_of_md_or_ceo_of_company',
            'selectdate_of_registration',
            'upload_signature',
            'all_roduct_manufactured',
            'all_raw_materials_used',
            )
        return form_one
    def get_form_two(self,instance):
        form_two= ManProspectiveMemberFormTwo.objects.filter(prospective_member=instance).values(
        'corporate_affairs_commision',
        'letter_of_breakdown_of_payment_and_docs_attached',
        'first_year_of_buisness_plan',
        'second_year_of_buisness_plan',
        'photocopy_of_your_reciept_issued_on_purchase_of_applicant_form',
        'prospective_member',

        )
        return []
    class Meta:
        model = ManProspectiveMemberProfile
        fields= '__all__'

    

class AdminRemarkSerializer(serializers.ModelSerializer):


    class Meta:
        model = Remark
        field = '__all__'