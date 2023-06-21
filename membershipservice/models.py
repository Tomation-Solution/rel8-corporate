from django.db import models
from account.models.user import  Memeber
# Create your models here.



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
    plants = models.JSONField( default=dict)
    # [{name:'pant1 name ..'}] products_manufactured strucuted
    products_manufactured =models.JSONField( default=dict)
    imported_raw_materials =models.JSONField( default=dict)
    locally_sourced_raw_materials =models.JSONField( default=dict)
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

    certificate_which_expired_on_thirtyone = models.FileField(upload_to='certificate_which_expired_on31/%d/',null=True,default=None,blank=True)
    copy_of_certificate_incoporation = models.FileField(upload_to='copy_of_certificate_incoporation/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_one =models.FileField(upload_to='audited_finicial_statement_one/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_two =models.FileField(upload_to='audited_finicial_statement_two/%d/',null=True,default=None,blank=True)



class CompaniesThatlostManCert(models.Model):
    members_reissuanceform =models.ForeignKey(MembersReIssuanceForm,on_delete=models.CASCADE)
    status = models.CharField(default='pending',max_length=10)
    bank_teller_of_payment = models.FileField(upload_to='bank_teller_of_payment/%d/')
    affidavit_from_court = models.FileField(upload_to='affidavit_from_court/%d/')

    certificate_which_expired_on_thirtyone = models.FileField(upload_to='certificate_which_expired_on31/%d/',null=True,default=None,blank=True)
    copy_of_certificate_incoporation = models.FileField(upload_to='copy_of_certificate_incoporation/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_one =models.FileField(upload_to='audited_finicial_statement_one/%d/',null=True,default=None,blank=True)
    audited_finicial_statement_two =models.FileField(upload_to='audited_finicial_statement_two/%d/',null=True,default=None,blank=True)
