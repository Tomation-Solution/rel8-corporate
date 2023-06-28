from django.db import models
from account.models.user import  Memeber
import json

def defualts(): return json.dumps(["0","0"])
class MembersReIssuanceForm(models.Model):
    member = models.OneToOneField(Memeber,on_delete=models.CASCADE,null=True,default=None)
    name_of_company  = models.CharField(max_length=500)
    cac_number  = models.CharField(max_length=500)
    tax_identification_number  = models.CharField(max_length=500)
    man_reg_number  = models.CharField(max_length=10)
    man_reg_number  = models.CharField(max_length=10)
    company_official_email = models.EmailField()
    corporate_addresse = models.TextField()
    # [{name:'pant1 name ..'}] that how plants should be structured
    # plants = models.JSONField( blank=True,default=defualts)
    # [{name:'pant1 name ..'}] products_manufactured strucuted
    # products_manufactured =models.JSONField(blank=True,default=defualts)
    # imported_raw_materials =models.JSONField(blank=True,default=defualts)
    # locally_sourced_raw_materials =models.JSONField(blank=True,default=defualts)
    ceo_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=15)

    chief_finace_officer = models.CharField(max_length=40)
    chief_finace_officer_phone_number = models.CharField(max_length=15)

    head_of_coporate = models.CharField(max_length=40)
    head_of_coporate_phone_number = models.CharField(max_length=15)

    officer_handling_man = models.CharField(max_length=40)
    officer_handling_man_phone_number = models.CharField(max_length=15)


class YearlyTurnOVer(models.Model):
    members_reissuanceform=models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    date_one = models.DateField(null=True,blank=True,default=None)
    date_two = models.DateField(null=True,blank=True,default=None)

    file_fordate_one = models.FileField(upload_to='file_fordate_one/%d/',null=True,blank=True,default=None)
    file_fordate_two = models.FileField(upload_to='file_fordate_two/%d/',null=True,blank=True,default=None)


class RenewalOFCertWithCompaniesThatHave2Batch(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    # "pending"|"approved"|"closed"
    status = models.CharField(default='pending',max_length=10)


class RenewalOFCertWithThatChangeThierOriginialName(models.Model):
    submit_change_of_name_cert =models.FileField(upload_to='submit_change_of_name_cert/%d/')
    bank_teller_of_payment = models.FileField(upload_to='bank_teller_of_payment/%d/')
    status = models.CharField(default='pending',max_length=10)
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    note = models.TextField(default='')
    certificate_which_expired_on_thirtyone = models.FileField(upload_to='certificate_which_expired_on31/%d/',null=True,default=None,blank=True)
    copy_of_certificate_incoporation = models.FileField(upload_to='copy_of_certificate_incoporation/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_one =models.FileField(upload_to='audited_finicial_statement_one/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_two =models.FileField(upload_to='audited_finicial_statement_two/%d/',null=True,default=None,blank=True)



class CompaniesThatlostManCert(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    bank_teller_of_payment = models.FileField(upload_to='bank_teller_of_payment/%d/')
    affidavit_from_court = models.FileField(upload_to='affidavit_from_court/%d/')
    note = models.TextField(default='')

    certificate_which_expired_on_thirtyone = models.FileField(upload_to='certificate_which_expired_on31/%d/',null=True,default=None,blank=True)
    copy_of_certificate_incoporation = models.FileField(upload_to='copy_of_certificate_incoporation/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_one =models.FileField(upload_to='audited_finicial_statement_one/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_two =models.FileField(upload_to='audited_finicial_statement_two/%d/',null=True,default=None,blank=True)



class CompaniesDeactivationActivationService(models.Model):
    note = models.TextField(default='')
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    letter_request_for_activation_or_deactivation =models.FileField(upload_to='letter_request_for_activation_or_deactivation/%d/',null=True,default=None,blank=True)
    submit_original_membership_cert =models.FileField(upload_to='submit_original_membership_cert/%d/',null=True,default=None,blank=True)

class UpdateOnProductManufactured(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    most_recent_finicial_statement =models.FileField(upload_to='most_recent_finicial_statement/%d/',null=True,default=None,blank=True)
    product_report_for_branch_inspection =models.FileField(upload_to='product_report_for_branch_inspection/%d/',null=True,default=None,blank=True)
    note = models.TextField(default='')



class UpdateFactoryLocation(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    most_recent_finicial_statement =models.FileField(upload_to='most_recent_finicial_statement/%d/',null=True,default=None,blank=True)
    product_report_for_branch_inspection =models.FileField(upload_to='product_report_for_branch_inspection/%d/',null=True,default=None,blank=True)
    note = models.TextField(default='')




class   MergerOfMemberCompanies(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    letter_requesting_merge =models.FileField(upload_to='letter_requesting_merge/%d/',null=True,default=None,blank=True)
    most_recent_finicial_statement =models.FileField(upload_to='most_recent_finicial_statement/%d/',null=True,default=None,blank=True)
    note = models.TextField(default='')

