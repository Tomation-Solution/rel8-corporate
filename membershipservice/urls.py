
from rest_framework.routers import DefaultRouter
from .views import (MembersReIssuanceFormViewset,RenewalOFCertWithThatChangeThierOriginialNameViewSet,CompaniesThatlostManCertViewset,
CompaniesDeactivationActivationServiceViewset,MergerOFCompanies,
UpdateFactoryLocationViewset,UpdateOnProductManufacturedViewset)
route = DefaultRouter()


route.register('',MembersReIssuanceFormViewset,basename='membersreIssuanceformViewset')
route.register('change-of-name',RenewalOFCertWithThatChangeThierOriginialNameViewSet,basename='RenewalOFCertWithThatChangeThierOriginialNameViewSet')
route.register('loss-of-cert',CompaniesThatlostManCertViewset,basename='CompaniesThatlostManCertViewset')

route.register('deactivation-activation-service',CompaniesDeactivationActivationServiceViewset,basename='CompaniesDeactivationActivationServiceViewset')
route.register('update-product-manufactured',UpdateOnProductManufacturedViewset,basename='UpdateOnProductManufacturedViewset')
route.register('update-factory-location',UpdateFactoryLocationViewset,basename='UpdateFactoryLocationViewset')
route.register('merger-of-company',MergerOFCompanies,basename='MergerOFCompanies')

urlpatterns =[

] + route.urls