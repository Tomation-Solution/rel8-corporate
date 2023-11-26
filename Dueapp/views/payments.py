
from django.urls import reverse
from utils.custom_exceptions import CustomError
from utils.custom_response import Success_response
from rest_framework import status,authentication,permissions
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .. import models
from event import models as event_models
import requests,json,threading
from rest_framework.views import APIView
from utils import permissions as custom_permissions
from utils.usefulFunc import convert_naira_to_kobo
from account.models import user as user_model
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.db import connection
from subscription import models as subscription_related_models
from Rel8Tenant import models as rel8tenant_related_models
from account.models.user import Memeber
from django.contrib.auth import get_user_model
from extras  import models as extras_models
from prospectivemember.models.man_prospective_model import( ManProspectiveMemberProfile,RegistrationAmountInfo,
ManProspectiveMemberFormOne,)
from mymailing import tasks as mymailing_task
from prospectivemember.models import general as generalProspectiveModels
from django.shortcuts import get_object_or_404
from publication.models import Publication
from utils.extraFunc import generate_n,paystackLikeResponse

def very_payment(request,reference=None):
    # this would be in the call back to check if the payment is a success
    if reference is None:
        raise CustomError({"error":"You need to send a refrence back"})
    schema_name = request.tenant.schema_name
    client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
    
    # this is checking if the user has pluged his paystack account 
    if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
        raise CustomError({'error':'Paystack not active please reach out to the developer'})
    PAYSTACK_SECRET = client_tenant.paystack_secret

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
    'Authorization': 'Bearer '+PAYSTACK_SECRET,
    'Content-Type' : 'application/json',
    'Accept': 'application/json',
    }
    try:
        resp = requests.get(url,headers=headers)
    except requests.ConnectionError:
        raise CustomError({"error":"Nework Error"}) 

    if resp.json()['data']['status'] == 'success':
        return Success_response(msg="Recived the Request Succefully",)
    raise CustomError({"error":"Something Went Wrong Try Again"})


def calmanLevyFee(amount,is_in_lagos):
    lagos_fee=0.00
    madeInNgeiraProducts = 10000
    legalLevy =10000
    AgmLevy =10000
    if is_in_lagos:
        lagos_fee = 20000
    if amount >=200000 or amount <= 2000000:
        return {'amountToBePaid':amount+lagos_fee+60000+madeInNgeiraProducts+AgmLevy+legalLevy,
                'landUseCharge':lagos_fee,'is_in_lagos':is_in_lagos,
            'specialLevy':60000,'madeInNgeiraProducts':madeInNgeiraProducts,'AgmLevy':AgmLevy,
            'legalLevy':legalLevy,
            'annualSub':amount

                
                }

    if amount >=180000 or amount <= 160000:
        
        return {
            'annualSubBasedOnTurnOver':amount+lagos_fee+30000+madeInNgeiraProducts+AgmLevy+legalLevy,
            'landUseCharge':lagos_fee,'is_in_lagos':is_in_lagos,
            'specialLevy':30000,'madeInNgeiraProducts':madeInNgeiraProducts,'AgmLevy':AgmLevy,
            'legalLevy':legalLevy,
            'annualSub':amount
            }

def calMansPayment(form_one:ManProspectiveMemberFormOne):
    is_in_lagos = False
    amount = 0.00
    turnover = None
    "reason for the strip is to remove emptye space so if it direcly == 0 that  means it truly emtyp"
    if form_one.current_sales_turnover !='.' or  len(form_one.current_sales_turnover.strip()) ==0:
        try:
            turnover = int(form_one.current_sales_turnover)
        except:
            turnover = 0
    if form_one.projected_sales_turnover !='.' or len(form_one.projected_sales_turnover.strip()) ==0:
        try:
            turnover = int(form_one.projected_sales_turnover)
        except:
            turnover = 0
    if turnover is None:
        raise CustomError({'error':'Current Sales Turnover or Projected Sales Turn over must be created'})
    if form_one.office_state.lower()=='lagos':
        is_in_lagos =True

 
    if int(turnover) >= 40000000000:
        "line 1 in man docs"
        amount= 2000000
        return calmanLevyFee(amount,is_in_lagos)

    
    if int(turnover) >=20000000000 or int(turnover) <= 39990000000:
        "line 2 in man docs"
        amount= 1500000  
        return calmanLevyFee(amount,is_in_lagos)

    
    if int(turnover) >=15000000000 or int(turnover) <= 19990000000:
        "line 3 in man docs"
        amount=  1400000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=10000000000 or int(turnover) <= 14990000000:
        "line 4 in man docs"
        amount = 850000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=7000000000 or int(turnover) <= 9990000000:
        "line 5 in man docs"
        amount =  500000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=4000000000 or int(turnover) <= 6990000000:
        "line 6 in man docs"
        amount= 375000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=100000000 or int(turnover) <= 249900000:
        "line 11 in man docs"
        
        amount = 160000
        return calmanLevyFee(amount,is_in_lagos)

    if int(turnover) >=1500000000 or int(turnover) <= 3990000000:
        "line 7 in man docs"
        amount = 260000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=750000000 or int(turnover) <= 149000000:
        "line 8 in man docs"
        amount = 220000
        return calmanLevyFee(amount,is_in_lagos)

    if int(turnover) >=500000000 or int(turnover) <= 749900000:
        "line 9 in man docs"
        amount = 200000
        return calmanLevyFee(amount,is_in_lagos)


    if int(turnover) >=250000000 or int(turnover) <= 499900000:
        "line 10 in man docs"
        amount = 180000
        return calmanLevyFee(amount,is_in_lagos)




    if amount == 0.00:
        raise CustomError({'error':'please reach out to admin beacuse your sales turn over does not meet the set requirement'})



class InitPaymentTran(APIView):
    "this is were the members pay for stuff read the code weel to get a hag of it"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[
        permissions.IsAuthenticated,
        custom_permissions.IsMemberOrProspectiveMember]


    def generateMetaData(self,request,forWhat='due',pk=None):
        if forWhat == 'paid_publication':
            instance = get_object_or_404(Publication,id=pk)
            amount_to_be_paid = instance.amount
            try:instance.danload.url
            except:raise CustomError({'error':'please reach out to admin to upload publication file because it not available'})
            
        if forWhat == 'prospective_member_registration':
            # it will be only on instance that will ever exist
            if connection.schema_name == 'man':
                reg = RegistrationAmountInfo.objects.all().first()
                if reg is None:
                    raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
                instance =get_object_or_404(ManProspectiveMemberProfile,user=request.user)
                amount_to_be_paid = reg.amount
                pk= instance.id
                if instance.has_paid:
                    raise CustomError({'error':'Please hold for admin to process your info you have paid already'})
            else:
                rule = generalProspectiveModels.AdminSetPropectiveMembershipRule.objects.all().first()
                if rule is None:
                    raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
                instance = get_object_or_404(generalProspectiveModels.ProspectiveMemberProfile,user=request.user)
                amount_to_be_paid = rule.amount
                pk= instance.id
                if instance.has_paid:
                    raise CustomError({'error':'Please hold for admin to process your info you have paid already'})
        if forWhat =='man_prospective_subscription_payment':
            if connection.schema_name == 'man':
                """
                    we need to get how much they make so we can know what the will pay
                    depending on 'current_sales_turnover' in  ManProspectiveMemberFormOne form
                """
                instance =get_object_or_404(ManProspectiveMemberProfile,user=request.user)
                form_one = ManProspectiveMemberFormOne.objects.get(prospective_member=instance)
                if form_one.current_sales_turnover==0.00:
                    raise CustomError({'error':'please fill current sales turnover field'})
                amount_to_be_paid = calMansPayment(form_one)['amountToBePaid']
                pk= instance.id
                if instance.has_paid_subcription:
                    raise CustomError({'error':'Please hold for admin to process your info you have paid already'})

        if forWhat=="due":
            # let get the id of due_user
            # let check if this user actually have due_user
            due_users = models.Due_User.objects.all()
            if not due_users.filter(user=request.user,id=pk,).exists():raise CustomError({"error":"Due Doesnt Exist"})
            if  due_users.filter(user=request.user,id=pk,is_paid=True).exists():raise CustomError({"error":"you have paid for this due already"})
            instance = models.Due_User.objects.get(user=request.user,id=pk)
            amount_to_be_paid = instance.amount

        if forWhat =='deactivating_due':
            deactivating_due = models.DeactivatingDue_User.objects.all()
            if not deactivating_due.filter(user=request.user,id=pk,).exists():raise CustomError({"error":"Due Deactivating Due Exist"})
            if  deactivating_due.filter(user=request.user,id=pk,is_paid=True).exists():raise CustomError({"error":"you have paid for this due already"})
            
            instance = models.DeactivatingDue_User.objects.get(user=request.user,id=pk)
            amount_to_be_paid = instance.amount

        if forWhat =='event_payment':
            event_users = event_models.EventDue_User.objects.all()
            events = event_models.Event.objects.all()
            if not events.filter(id=pk,).exists():raise CustomError({"error":"Event Does Not Exist maybe it was deleted"})
            event = event_models.Event.objects.get(id=pk )
            if event_users.filter(user=request.user,event=event,is_paid=True).exists():raise CustomError({"error":"Hello you have paid for this event"})
            
            instance,_ = event_models.EventDue_User.objects.get_or_create(
                user=request.user,event=event,amount=event.amount,)
            amount_to_be_paid = instance.amount
            pk = instance.id#we did this cause we accessing the eventdue_user
        if forWhat =='fund_a_project':
            'since this is a donation there is no fix price we get it from the query param'
            amount  = request.query_params.get('donated_amount',None)
            if amount is None:
                raise CustomError({'error':'Please amount it missing'})
            "here we check it the"
            try:
                amount = int(amount)
                amount_to_be_paid=amount
            except ValueError:
                raise CustomError({'error':'amount must be number '})
            fundAProject = extras_models.FundAProject.objects.get(id=pk)
            instance,_ = extras_models.SupportProjectInCash.objects.get_or_create(
                member = request.user.memeber,
                project=fundAProject,
                
            )
            instance.amount = amount
            instance.save()
            amount_to_be_paid=amount

        # if 
        if(instance==None):raise CustomError({"error":"Something went wrong"})
        if request.user.user_type== 'members':
            member = user_model.Memeber.objects.get(user=request.user)
        if request.user.user_type== 'prospective_members':
            if connection.schema_name == 'man':
                member =ManProspectiveMemberProfile.objects.get(user=request.user)
            else:
                member = generalProspectiveModels.ProspectiveMemberProfile.objects.get(user=request.user)
        
        return {
            'amount':amount_to_be_paid,
            'instance':instance,
            'metadata':{
                "instanceID":pk,
                'member_id':member.id,
                "user_id":request.user.id,
                "forWhat":forWhat,
                'schema_name':request.tenant.schema_name,
                'user_type':request.user.user_type,
                'amount_to_be_paid':str(amount_to_be_paid)}
        }

    def post(self, request, forWhat="due",pk=None):
        

        """
        forWhat can be  = due,event,deactivating_due
        """
        if request.user.user_type== 'members':
            if(not user_model.Memeber.objects.all().filter(user=request.user).exists()):
                raise CustomError({"error":'member doest not exist'})

        

        schema_name = request.tenant.schema_name
        client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
        payment_type = request.query_params.get('payment_type','paystack')


        if payment_type == 'paystack':

            # this is checking if the user has pluged his paystack account 
            if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
                raise CustomError({'error':'Paystack not active please reach out to the developer'})
            PAYSTACK_SECRET = client_tenant.paystack_secret
            instance =None
                # Paystack intialization Url



            generateInfo = self.generateMetaData(request,forWhat,pk)
            instance = generateInfo.get('instance')


            url = 'https://api.paystack.co/transaction/initialize/'
            headers = {
                'Authorization': f'Bearer {PAYSTACK_SECRET}',
                'Content-Type' : 'application/json',
                'Accept': 'application/json',}
            body = {
                "email": request.user.email,
                "amount": convert_naira_to_kobo(generateInfo.get('amount')),
                "metadata":generateInfo.get('metadata'),
                
                # "callback_url":settings.PAYMENT_FOR_MEMBERSHIP_CALLBACK,
                }
            try:
                resp = requests.post(url,headers=headers,data=json.dumps(body))
            except requests.ConnectionError:
                raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            if resp.status_code ==200:
                data = resp.json()
            
                # we create a transaction history upload nessary data by this time is_successfull will always be false
                # we put in paystack refrence in the current due the user wants to pay  data['data']['reference']
                # we use wehook to confirm the payment
                instance.paystack_key= data['data']['reference']
                instance.save()

                return Success_response(msg='Success',data=data)


        if payment_type == 'flutterwave':
            if client_tenant.flutterwave_publickey =='null' or client_tenant.flutterwave_secret =='null':
                raise CustomError({'error':'Flutterwave Key not active please reach out to the developer'})
            generateInfo = self.generateMetaData(request,forWhat,pk)
            instance = generateInfo.get('instance')
            url ='https://api.flutterwave.com/v3/payments'
            headers = {
                'Authorization': f'Bearer {client_tenant.flutterwave_secret}',
                'Content-Type' : 'application/json',
                'Accept': 'application/json',}
            body = {
            'tx_ref': f'{generate_n(5)}---{forWhat}--{request.user.id}--{instance.id}--{schema_name}--{generateInfo.get("amount")}',
            'amount': f'{generateInfo.get("amount")}',
            'currency': "NGN",
            'redirect_url': "https://www.google.com/",
            'meta':generateInfo.get('metadata'),
            'customer': {
                'email':'test@gmail.com',
                'phonenumber': "08162047348",
                'name': "Markothedev"
            },
            }

            try:
                resp = requests.post(url,headers=headers,data=json.dumps(body))
            except requests.ConnectionError:
                raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
            print({'status':resp.status_code})
            print({'data':resp.json()})
            if resp.status_code ==200:
                data = resp.json()
            
            #     # instance.paystack_key= data['data']['reference']
            #     # instance.save()

                return Success_response(msg='Success',data= paystackLikeResponse(data['data']['link']) )
        
        raise CustomError(message='Some Error Occured Please Try Again',status_code=status.HTTP_503_SERVICE_UNAVAILABLE)



















def webhookPayloadHandler(meta_data,user):
        if meta_data['forWhat'] == 'due':
            # instanceID in this context means Due_User id
            due = models.Due_User.objects.get(user=user,id=meta_data['instanceID'])
            due.is_paid=True
            due.save()
            # since the payment was a success then we reduce the amount owing in memeber profile
            member_profile = Memeber.objects.get(user=user)
            member_profile.amount_owing= member_profile.amount_owing + due.amount
            member_profile.save()

        if meta_data['forWhat'] == 'deactivating_due':
            # instanceID in this context means Due_User id
            due = models.DeactivatingDue_User.objects.get(user=user,id=meta_data['instanceID'])
            due.is_paid=True
            due.save()    
        if meta_data['forWhat'] =='event_payment':
            event_user = event_models.EventDue_User.objects.get(user=user,id=meta_data['instanceID'])
            event_user.is_paid=True
            event_user.save()
#Note setTimer set the subscription so it would end at a given time
        if meta_data['forWhat'] =='individualSub':
            CurrentTenant  = rel8tenant_related_models.Client.objects.get(schema_name=meta_data['schema_name'])
            # the payment means a memebers is trying to subscribe
            member = user_model.Memeber.objects.get(id=meta_data.get('member_id'))
            individualSub = subscription_related_models.IndividualSubscription.objects.get(
            # member=member,
            id =meta_data.get('instanceID'))
            # this means the payment was succesfful
            individualSub.is_paid_succesfully=True
            # this would be false for now our periodic task will set it to true meaning th sub has ended
            individualSub.is_end=False
            individualSub.save()
            subscription_related_models.setTimer(meta_data.get('instanceID'),"individual",meta_data['schema_name'],CurrentTenant)

 
        if meta_data['forWhat'] =='organizationSub':
           

            # the payment means a Admin is trying to subscribe
            CurrentTenant  = rel8tenant_related_models.Client.objects.get(schema_name=meta_data['schema_name'])
            TenantSub = subscription_related_models.TenantSubscription.objects.get(
           id =meta_data.get('instanceID'))
            # tenant=CurrentTenant,
            # this means the payment was succesfful
            TenantSub.is_paid_succesfully=True
            # this would be false for now our periodic task will set it to true meaning th sub has ended
            TenantSub.is_end=False
            TenantSub.save()
            subscription_related_models.setTimer(meta_data.get('instanceID'),"organization",meta_data['schema_name'],CurrentTenant)
        if meta_data['forWhat'] == 'fund_a_project':
            support_project_incash =  extras_models.SupportProjectInCash.objects.get(id=meta_data['instanceID'])
            support_project_incash.is_paid=True 
            support_project_incash.save()
            "update project amount made"
            project = extras_models.FundAProject.objects.get(id=support_project_incash.project.id)
            project.amount_made =project.amount_made+  support_project_incash.amount
            project.save()


        if meta_data['forWhat'] == 'prospective_member_registration':
            member_id =meta_data['member_id']
            instanceID = meta_data['instanceID']
            amount_to_be_paid= meta_data['amount_to_be_paid']
            if connection.schema_name == 'man':
                prospective_member = ManProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid=True
                prospective_member.amount=float(amount_to_be_paid)
                prospective_member.save()
                thread = threading.Thread(target=mymailing_task.send_activation_mail,args=[prospective_member.user.id,prospective_member.user.email])
                thread.start()
                thread.join()

            else:
                prospective_member= generalProspectiveModels.ProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid=True
                prospective_member.amount_paid=amount_to_be_paid
                prospective_member.save()

        if meta_data['forWhat'] == 'man_prospective_subscription_payment':
            # member_id =meta_data['member_id']
            instanceID = meta_data['instanceID']
            amount_to_be_paid= meta_data['amount_to_be_paid']
            if connection.schema_name == 'man':
                prospective_member = ManProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid_subcription=True
                prospective_member.subcription_amount=float(amount_to_be_paid)
                prospective_member.save()
        if meta_data['forWhat'] =='paid_publication':
            publication= Publication.objects.get(id=meta_data['instanceID'])
            thread = threading.Thread(
                target=mymailing_task.send_publication_downloadlink,
                args=[
                     publication.danload.url,user.email,
                    publication.name
                ]
                )
            thread.start()
            thread.join()
        return HttpResponse(status.HTTP_200_OK)


@csrf_exempt
def useWebhook(request,pk=None):
    "this receives Payload from paystack"
    data = json.loads(request.body)
    meta_data =data['data']['metadata']
    connection.set_schema(schema_name=meta_data['schema_name'])
    user = get_user_model().objects.get(id=meta_data['user_id'])

    if data.get('event') == 'charge.success':
        return webhookPayloadHandler(meta_data,user)




@csrf_exempt
def useFlutterWaveWebhook(request,pk=None):
    'this receives payload from flutter waVE'
    print(request.body)
    data = json.loads(request.body)
    forWhat,user_id,instanceID,schema_name,amount = data.get('txRef').split('---')[1].split('--') 
    meta_data ={
        'forWhat':forWhat,
        'instanceID':instanceID,
        'schema_name':schema_name,
        'amount_to_be_paid':amount,
    }
    connection.set_schema(schema_name=meta_data['schema_name'])
    user = get_user_model().objects.get(id=user_id)
    # meta_data['member_id']= Memeber.objects.filter(user=user).first().id

    if data.get('status') == 'successful' or data.get('event') == 'charge.completed':
        return webhookPayloadHandler(meta_data,user)
