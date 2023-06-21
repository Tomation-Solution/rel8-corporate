from rest_framework import serializers
from . import models
import json
import ast

class MembersReIssuanceFormSerializer(serializers.ModelSerializer):
    yearly_turn  = serializers.SerializerMethodField()
    extras= serializers.SerializerMethodField()

    file_fordate_one = serializers.FileField(required=False)
    file_fordate_two = serializers.FileField(required=False)
    date_one = serializers.DateField(required=False)
    date_two = serializers.DateField(required=False)

    products_manufactured =serializers.JSONField(required=False)
    imported_raw_materials =serializers.JSONField(required=False)
    locally_sourced_raw_materials =serializers.JSONField(required=False)
    def get_yearly_turn(self,instance):
        data,created = models.YearlyTurnOVer.objects.get_or_create(members_reissuanceform=instance)
        url_one =''
        url_two =''
        try:
            url_one=data.file_fordate_one.url 
            url_two=data.file_fordate_two.url 
        except:pass
        return {
            'date_one':data.date_one,
            'date_two':data.date_two,
            'file_fordate_one':url_one,
            'file_fordate_two':url_two,
        }

    def get_extras(self,instance):
        data={
            'plants':ast.literal_eval(instance.plants),
            'products_manufactured':ast.literal_eval(instance.products_manufactured),
            'imported_raw_materials':ast.literal_eval(instance.plants),
        }
        return data

    # def update(self, instance, validated_data):
    #     super().update(instance, validated_data)
    #     ins 

    class Meta:
        model= models.MembersReIssuanceForm
        fields ='__all__'


