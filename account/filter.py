from .models import  user  as user_related_model
import django_filters
from django.db.models import Q

class MemberSearch(django_filters.FilterSet):
    general_search =django_filters.CharFilter(method='my_custom_filter', label="Search")
    class Meta:
        model = user_related_model.UserMemberInfo
        fields =['value']

    # def my_custom_filter(self, queryset, name, value):
    #     user_related_model.UserMemberInfo.objects.filter(value=value)
    #     return queryset.filter(
    #         Q(user)
    #     )