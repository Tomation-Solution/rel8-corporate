
from rest_framework.routers import DefaultRouter
from .views import MembersReIssuanceFormViewset
route = DefaultRouter()


route.register('',MembersReIssuanceFormViewset,basename='membersreIssuanceformViewset')

urlpatterns =[

] + route.urls