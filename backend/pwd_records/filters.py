import django_filters
from .models import PWDRecord

class PWDRecordFilter(django_filters.FilterSet):
	is_verified = django_filters.BooleanFilter()

	class Meta:
		model = PWDRecord
		fields = ['is_verified']