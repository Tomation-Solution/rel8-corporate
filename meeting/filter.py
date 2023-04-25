import django_filters
from . import models

class MeetingFitlter(django_filters.FilterSet):
    council = django_filters.NumberFilter(field_name='exco')

    is_for_all_grade = django_filters.BooleanFilter(field_name='membership_grade', lookup_expr='isnull')
    
    not_council = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')
    not_commitee  = django_filters.BooleanFilter(field_name='commitee',lookup_expr='isnull')
    not_chapters  = django_filters.BooleanFilter(field_name='chapters',lookup_expr='isnull')

    membership_grade = django_filters.NumberFilter(field_name='membership_grade',)
    commitee = django_filters.NumberFilter(field_name='commitee')
    chapters = django_filters.NumberFilter(field_name='chapters')

    class Meta:
        model = models.Meeting
        fields = [
            'council','is_for_all_grade','not_council','not_commitee','not_chapters',
            'membership_grade','commitee','chapters'
        ]
