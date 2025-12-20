from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . models import DisabilityType, ServiceType, PWDRecord

class DisabilityTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ["id", "disability_type", "description", "created_on"]
	list_filter = ["disability_type"]
	ordering = ["created_on"]
	list_per_page = 100

class ServiceTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ["id", "service_name", "description", "created_on"]
	list_filter = ["service_name"]
	ordering = ["created_on"]
	list_per_page = 100

class PWDRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ["full_name", "date_of_birth", "gender", "disability_type", "id_photo", "occupation", "community", "area_council", "contact_number", "is_verified", "registration_date", "user"]
	list_filter = ["is_verified"]
	ordering = ["registration_date"]
	list_per_page = 100

admin.site.register(DisabilityType, DisabilityTypeAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(PWDRecord, PWDRecordAdmin)