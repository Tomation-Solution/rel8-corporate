from django.shortcuts import render
# from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.views import APIView

# Create your views here.
from . import serializer,models
from account.models.user  import Memeber
from  rest_framework.response import Response
from utils import custom_response,custom_parsers
from rest_framework import status
from rest_framework.parsers import  FormParser
from rest_framework.decorators import action
from utils.permissions import IsMember
from django.shortcuts import get_object_or_404
from account.models.user  import Memeber
# from //s

class MembersReIssuanceFormViewset(ModelViewSet):
    serializer_class  =serializer.MembersReIssuanceFormSerializer
    queryset  = models.MembersReIssuanceForm.objects.all()
    permission_classes  =[IsMember]
    parser_classes =(custom_parsers.NestedMultipartParser,FormParser,)

    def create(self, request, *args, **kwargs):
        return  Response('Please use patch request')
    
  


    def partial_update(self, request, *args, **kwargs):
        # check if the there is
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        # no matter what is either we createing or updating we wont use create function
        serializer_class = self.serializer_class(instance=instance,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()        

        data,created = models.YearlyTurnOVer.objects.get_or_create(members_reissuanceform=instance)
        data.date_one = request.data.get('date_one')
        data.date_two = request.data.get('date_two')
        data.file_fordate_two = request.data.get('file_fordate_two')
        data.file_fordate_one = request.data.get('file_fordate_one')
        data.save()

        clean_data = self.serializer_class(instance=instance,many=False)

        print(
            clean_data.data
        )
        return custom_response.Success_response(msg='Updated ReIssuance Form',
                                                data=clean_data.data,
                                                status_code=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        serializer_class = self.serializer_class(instance=instance,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


class AdminGetAndUpdate:
    @action(detail=True,methods=['get'])
    def admin_get(self,request,*arg,**kwargs):
        serializer_class = self.serializer_class(instance=self.queryset.all(),many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)

    @action(detail=True,methods=['post'])
    def admin_update(self,request,*args,**kwargs):
        pk = kwargs.get('pk','-1')
        member = get_object_or_404(Memeber,id=pk)
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=member
        )
        original_name,_ = self.model.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)



class RenewalOFCertWithThatChangeThierOriginialNameViewSet(ModelViewSet,AdminGetAndUpdate):
    queryset = models.RenewalOFCertWithThatChangeThierOriginialName.objects.all()
    serializer_class = serializer.RenewalOFCertWithThatChangeThierOriginialNameSerializer
    model = models.RenewalOFCertWithThatChangeThierOriginialName

    def update(self, request, *args, **kwargs):
    
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.RenewalOFCertWithThatChangeThierOriginialName.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.RenewalOFCertWithThatChangeThierOriginialName.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


class CompaniesThatlostManCertViewset(ModelViewSet,AdminGetAndUpdate):
    queryset = models.CompaniesThatlostManCert.objects.all()
    serializer_class = serializer.CompaniesThatlostManCertSerializer
    model = models.CompaniesThatlostManCert
    def update(self, request, *args, **kwargs):
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.CompaniesThatlostManCert.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.CompaniesThatlostManCert.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)

    def get(self,request,*arg,**kwargs):
        original_name = models.CompaniesThatlostManCert.objects.all()
        serializer_class = self.serializer_class(instance=original_name,many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


class CompaniesDeactivationActivationServiceViewset(ModelViewSet,AdminGetAndUpdate):
    queryset = models.CompaniesDeactivationActivationService.objects.all()
    serializer_class = serializer.CompaniesDeactivationActivationSerializer
    model = models.CompaniesDeactivationActivationService
    def update(self, request, *args, **kwargs):
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.CompaniesDeactivationActivationService.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.CompaniesDeactivationActivationService.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


    def get(self,request,*arg,**kwargs):
        original_name = models.CompaniesDeactivationActivationService.objects.all()
        serializer_class = self.serializer_class(instance=original_name,many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)



class UpdateOnProductManufacturedViewset(ModelViewSet,AdminGetAndUpdate):
    queryset = models.UpdateOnProductManufactured.objects.all()
    serializer_class = serializer.UpdateOnProductManufacturedSerializer
    model =  models.UpdateOnProductManufactured
    def update(self, request, *args, **kwargs):
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.UpdateOnProductManufactured.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.UpdateOnProductManufactured.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)



    def get(self,request,*arg,**kwargs):
        original_name = models.UpdateOnProductManufactured.objects.all()
        serializer_class = self.serializer_class(instance=original_name,many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


class UpdateFactoryLocationViewset(ModelViewSet,AdminGetAndUpdate):
    queryset = models.UpdateFactoryLocation.objects.all()
    serializer_class = serializer.UpdateFactoryLocationSerializer
    model = models.UpdateFactoryLocation
    def update(self, request, *args, **kwargs):
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.UpdateFactoryLocation.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.UpdateFactoryLocation.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)


    def get(self,request,*arg,**kwargs):
        original_name = models.UpdateFactoryLocation.objects.all()
        serializer_class = self.serializer_class(instance=original_name,many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)

class MergerOFCompanies(ModelViewSet,AdminGetAndUpdate):
    queryset = models.MergerOfMemberCompanies.objects.all()
    serializer_class = serializer.MergerOfMemberCompaniesSerializer
    model =models.MergerOfMemberCompanies
    def update(self, request, *args, **kwargs):
        instance,created =models.MembersReIssuanceForm.objects.get_or_create(
            member=request.user.memeber
        )
        original_name,_ = models.MergerOfMemberCompanies.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,partial=True,data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return custom_response.Success_response(msg='Updated',
                                                data=serializer_class.data,
                                                status_code=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        original_name,_ = models.MergerOfMemberCompanies.objects.get_or_create(
            members_reissuanceform=instance
        )
        serializer_class = self.serializer_class(instance=original_name,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)

    def get(self,request,*arg,**kwargs):
        original_name = models.MergerOfMemberCompanies.objects.all()
        serializer_class = self.serializer_class(instance=original_name,many=True)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)
