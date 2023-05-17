from prospectivemember.models import man_prospective_model as manrelatedPropectiveModels
from prospectivemember import serializer
from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status
from utils.custom_exceptions import  CustomError 
from rest_framework.permissions import  IsAuthenticated,AllowAny
from rest_framework.decorators import action,permission_classes as deco_permission_classes
from utils.permissions import IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid
from utils.permissions import  IsAdminOrSuperAdmin, IsProspectiveMember,IsPropectiveMembersHasPaid_general
from Dueapp.views.payments import calMansPayment
from django.shortcuts import get_object_or_404
from  rest_framework.response import Response
class CreateManPropectiveMemberViewset(viewsets.ViewSet):
    serializer_class = serializer.CreateManPropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()

        return Success_response('Creation Success',data=response_info,status_code=status.HTTP_201_CREATED)

class StatusView:
    @action(detail=False,methods=['get'])
    def get_status(self,request,*args,**kwargs):
        return Success_response('..',data=request.user.manprospectivememberprofile.application_status)

class PropectiveMemberManageFormOneViewSet(viewsets.ModelViewSet,StatusView):
    serializer_class = serializer.PropectiveMemberManageFormOneSerializer
    permission_classes=[IsAuthenticated,IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid]
    queryset = manrelatedPropectiveModels.ManProspectiveMemberFormOne.objects.all()


    @action(detail=False,methods=['get'])
    def get_subscriptio_payment_breakdown(self,request):
        form_one,created= manrelatedPropectiveModels.ManProspectiveMemberFormOne.objects.get_or_create(prospective_member=request.user.manprospectivememberprofile)
        
        return Success_response('Successfull',data=calMansPayment(form_one),status_code=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        man_prospective_member_form_one,created= manrelatedPropectiveModels.ManProspectiveMemberFormOne.objects.get_or_create(prospective_member=request.user.manprospectivememberprofile)

        serializer_class = self.serializer_class(data=request.data,instance=man_prospective_member_form_one)
        serializer_class.is_valid(raise_exception=True)
        instance = serializer_class.save()

        clean_data =self.serializer_class(instance=instance,many=False)
        return Success_response('Update Successfull',data=clean_data.data,status_code=status.HTTP_200_OK)

    def get_queryset(self):
        query_set = self.queryset.filter(prospective_member=self.request.user.manprospectivememberprofile)
        return query_set


class PropectiveMemberManageFormTwo(viewsets.ModelViewSet,StatusView):
    serializer_class = serializer.PropectiveMemberManageFormTwoSerializer
    queryset = manrelatedPropectiveModels.ManProspectiveMemberFormTwo.objects.all()
    permission_classes=[IsAuthenticated,IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid]

    def create(self, request, *args, **kwargs):
        man_prospective_member_form_one,created= manrelatedPropectiveModels.ManProspectiveMemberFormTwo.objects.get_or_create(prospective_member=request.user.manprospectivememberprofile)

        serializer_class = self.serializer_class(data=request.data,instance=man_prospective_member_form_one)
        serializer_class.is_valid(raise_exception=True)
        instance = serializer_class.save()

        clean_data =self.serializer_class(instance=instance,many=False)
        return Success_response('Update Successfull',data=clean_data.data,status_code=status.HTTP_200_OK)

    def get_queryset(self):
        query_set = self.queryset.filter(prospective_member=self.request.user.manprospectivememberprofile)
        return query_set



class AdminManageManProspectiveMemberViewSet(viewsets.ViewSet):
    # queryset = man_prospective_model.p
    permission_classes = [
        # IsAuthenticated,IsAdminOrSuperAdmin
        # remove authentication for now for easy of user
        ]


    @action(detail=False,methods=['get'])
    def get_submissions(self,request,*args,**kwargs):
        details = request.query_params.get('id',None)
        if details is None:
            all_propective_member_profiles = manrelatedPropectiveModels.ManProspectiveMemberProfile.objects.filter(has_paid_subcription=True)
            clean_data = serializer.ProspectiveManMemberCleaner(instance=all_propective_member_profiles,many=True)
                
            return Success_response ('success',data=clean_data.data,)
        
        all_propective_member_profiles =get_object_or_404(manrelatedPropectiveModels.ManProspectiveMemberProfile,id=details)

        clean_data = serializer.ProspectiveManMemberCleaner(instance=all_propective_member_profiles,many=False)
        
        return Success_response('success',data=clean_data.data)
    
    @action(detail=False,methods=['post'])
    def update_prospective_status(self,request,*args,**kwargs):
        id = request.data.get('id')
        status = request.data.get('status','approval_in_progress')
        profile = manrelatedPropectiveModels.ManProspectiveMemberProfile.objects.get(id=id)
        profile.application_status=status
        profile.save()
        return Success_response(f'profile status has been changed to "{status}"')
        

class AdminManageRemark(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                        #   IsAdminOrSuperAdmin
                          ]
    queryset = manrelatedPropectiveModels.Remark.objects.all()

    @action(detail=False,methods=['get'])
    @deco_permission_classes([IsAuthenticated])
    def get_my_remark(self,request,*args,**kwargs):
        profile = manrelatedPropectiveModels.ManProspectiveMemberProfile.objects.get(user=request.user)
        remark = manrelatedPropectiveModels.Remark.objects.filter(member_profile=profile).values(
        'content','id','member_profile'
        )

        return Response(data=remark,status=status.HTTP_200_OK)