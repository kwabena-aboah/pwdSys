import os, random
from django.db import models
from auditlog.registry import auditlog
from users.models import User
from django.utils import timezone

def filename_ext(filepath):
    file_base = os.path.basename(filepath)
    filename, ext = os.path.splitext(file_base)
    return filename, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9498594795)
    name, ext = filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "pictures/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


GENDER = [
	('male', 'Male'),
	('female', 'Female'),
	('other', 'Other'),
]

APPLICATION_STATUS = [
	('pending', 'Pending'),
	('approved', 'Approved'),
	('rejected', 'Rejected'),
]

COMPLAINT_STATUS = [
	('new', 'New'),
	('under review', 'Under Review'), 
	('resolved', 'Resolved'),
]

class DisabilityType(models.Model):
	disability_type = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	created_on = models.DateField(auto_now_add=True)

	def __str__(self):
		return f"{self.disability_type} - {self.description}"

class ServiceType(models.Model):
	service_name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	created_on = models.DateField(auto_now_add=True)

	def __str__(self):
		return f"{self.service_name} - {self.description}"

class PWDRecord(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=6, choices=GENDER, default='male')
	disability_type = models.ForeignKey(DisabilityType, on_delete=models.CASCADE)
	id_photo = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	address = models.TextField(blank=True, null=True)
	contact_number = models.CharField(max_length=15, blank=True, null=True)
	emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
	emergency_phone = models.CharField(max_length=15, blank=True, null=True)
	is_verified = models.BooleanField(default=True)
	registration_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.full_name} - {self.user.role}"

class Certificate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pwd_id = models.ForeignKey(PWDRecord, on_delete=models.CASCADE)
	medical_certificate = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

class MedicalRecords(models.Model):
	pwd_id = models.ForeignKey(PWDRecord, on_delete=models.CASCADE)
	diagnosis = models.TextField()
	doctor_name = models.CharField(max_length=255, blank=True, null=True)
	hospital_name = models.CharField(max_length=255, blank=True, null=True)
	last_checkup_date = models.DateField(auto_now_add=False)
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.pwd_id.full_name}"

class SupportServices(models.Model):
	pwd_id = models.ForeignKey(PWDRecord, on_delete=models.CASCADE)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	application_status = models.CharField(max_length=8, choices=APPLICATION_STATUS, default='pending')
	applied_date = models.DateField(auto_now_add=True)
	approval_date = models.DateField(auto_now=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.pwd_id.full_name} - {self.service_type.service_name}"

class Complaints(models.Model):
	pwd_id = models.ForeignKey(PWDRecord, on_delete=models.CASCADE)
	location = models.CharField(max_length=255, blank=True, null=True)
	complaint_description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=12, choices=COMPLAINT_STATUS, default='new')
	reported_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.pwd_id.full_name} - {self.complaint_description}"


auditlog.register(PWDRecord)
auditlog.register(MedicalRecords)
auditlog.register(SupportServices)
auditlog.register(Complaints)