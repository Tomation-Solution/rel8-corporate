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
                                                # data=clean_data.data,
                                                data=[],
                                                status_code=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        instance,created = models.MembersReIssuanceForm.objects.get_or_create(member=request.user.memeber)
        serializer_class = self.serializer_class(instance=instance,many=False)
        return custom_response.Success_response(msg='Success',data=serializer_class.data,status_code=status.HTTP_200_OK)

