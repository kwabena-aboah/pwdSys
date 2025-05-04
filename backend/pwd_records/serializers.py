from django.core.files.base import ContentFile
import base64
import six
import uuid
import binascii
from rest_framework import serializers
from . models import DisabilityType, ServiceType, PWDRecord, Certificate, MedicalRecords, SupportServices, Complaints, DocumentAuditLog
from users.models import User

class Base64ImageField(serializers.ImageField):
    """ Handles image uploads through raw post data. It uses base64 for
    encoding and decoding the contents of the image"""

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # check if the base64 string is in the "data:" format
            if 'data' in data and ';base64,' in data:
                # break out the header from the base64 content
                header, data = data.split(';base64,')
            
            # try to decode the file. Return validation error if it fails
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            
            # generate file name
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough
            # get the file name extension
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)
    
    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

class DisabilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabilityType
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class PWDRecordSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    disability_name = serializers.CharField(source='disability_type.disability_type', read_only=True)
    id_photo = serializers.SerializerMethodField()
    class Meta:
        model = PWDRecord
        fields = [
            'id', 'user', 'full_name', 'date_of_birth', 'gender', 'disability_type', 'disability_name', 'id_photo',
            'address', 'contact_number', 'emergency_contact_name', 'emergency_phone', 'is_verified', 'registration_date'
        ]
        extra_kwargs = {'user': {'read_only': True}} # make user auto-assigned

    def validate_full_name(self, value):
        return value if value else None

    def validate_disability_type(self, value):
        return value if value else None

    def validate_date_of_birth(self, value):
        return value if value else None

    def validate_id_photo(self, value):
        """Ensure file is properly handled"""
        if isinstance(value, str) and value.startswith("data:image"):
            format, imgstr = value.split.split(";base64")
            ext = format.split("/")[-1]

            img_data = base64.b64decode(imgstr)

            return ContentFile(img_data, name=f"{uuid.uuid4()}.{ext}")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user #set user automatically
        else:
            raise serializers.ValidationError("User information is missing.")
        return super().create(validated_data)

    def get_id_photo(self, obj):
        # request = self.context.get('request')
        if obj.id_photo:
            return obj.id_photo.url
        return None

    def update(self, instance, validated_data):
        # Prevent overwriting the existing file if no new id_photo is uploaded
        if 'id_photo' in validated_data:
            if validated_data['id_photo'] is None:
                validated_data.pop('id_photo')
        return super().update(instance, validated_data)

class CertificateSerializer(serializers.ModelSerializer):
    pwd_id = serializers.PrimaryKeyRelatedField(queryset=PWDRecord.objects.all(), write_only=True)
    pwd_name = serializers.CharField(source='pwd_id.full_name', read_only=True)
    medical_certificate = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_null=True
    )

    class Meta:
        model = Certificate
        fields = [
            'id','user', 'pwd_id', 'pwd_name', 'medical_certificate', 'created_at'
        ]
        extra_kwargs = {'user': {'read_only': True}} # make user auto-assigned

    def get_medical_certificate(self, obj):
        request = self.context.get('request')
        if obj.medical_certificate:
            return request.build_absolute_uri(obj.medical_certificate.url)
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user #set user automatically
        else:
            raise serializers.ValidationError("User information is missing.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent overwriting the existing file if no new picture is uploaded
        medical_certificate = validated_data.get('medical_certificate', None)

        if not medical_certificate:
            validated_data.pop('medical_certificate', None)
        return super().update(instance, validated_data)


class MedicalRecordsSerializer(serializers.ModelSerializer):
    pwd_id = serializers.PrimaryKeyRelatedField(queryset=PWDRecord.objects.all(), write_only=True)
    pwd_name = serializers.CharField(source='pwd_id.full_name', read_only=True)

    class Meta:
        model = MedicalRecords
        fields = [
            'id', 'pwd_id', 'pwd_name', 'diagnosis', 'doctor_name', 'hospital_name', 'last_checkup_date', 'user'
        ]
        extra_kwargs = {'user': {'read_only': True}} # make user auto-assigned

    def validate_pwd_id(self, value):
        return value if value else None

    def validate_diagnosis(self, value):
        return value if value else None

    def validate_last_checkup_date(self, value):
        return value if value else None

    def validate(self, data):
        pwd_id = data.get('pwd_id')
        if not PWDRecord.objects.filter(id=pwd_id.id).exists():
            raise serializers.ValidationError({'pwd_id': 'Invalid PWD ID.'})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user #set user automatically
        else:
            raise serializers.ValidationError("User information is missing.")
        return super().create(validated_data)

class SupportServicesSerializer(serializers.ModelSerializer):
    pwd_id = serializers.PrimaryKeyRelatedField(queryset=PWDRecord.objects.all(), write_only=True)
    pwd_name = serializers.CharField(source='pwd_id.full_name', read_only=True)
    service_name = serializers.CharField(source='service_type.service_name', read_only=True)

    class Meta:
        model = SupportServices
        fields = [
            'id', 'pwd_id', 'pwd_name', 'service_type', 'service_name', 'application_status', 'approval_date', 'user'
        ]
        extra_kwargs = {'user': {'read_only': True}} # make user auto-assigned

    def validate(self, data):
        pwd_id = data.get('pwd_id')
        if not PWDRecord.objects.filter(id=pwd_id.id).exists():
            raise serializers.ValidationError({'pwd_id': 'Invalid PWD ID.'})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user #set user automatically
        else:
            raise serializers.ValidationError("User information is missing.")
        return super().create(validated_data)

class ComplaintsSerializer(serializers.ModelSerializer):
    pwd_id = serializers.PrimaryKeyRelatedField(queryset=PWDRecord.objects.all(), write_only=True)
    pwd_name = serializers.CharField(source='pwd_id.full_name', read_only=True)

    class Meta:
        model = Complaints
        fields = [
            'id', 'pwd_id', 'pwd_name', 'location', 'complaint_description', 'status', 'reported_at', 'user'
        ]
        extra_kwargs = {'user': {'read_only': True}} # make user auto-assigned

    def validate(self, data):
        pwd_id = data.get('pwd_id')
        if not PWDRecord.objects.filter(id=pwd_id.id).exists():
            raise serializers.ValidationError({'pwd_id': 'Invalid PWD ID.'})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user #set user automatically
        else:
            raise serializers.ValidationError("User information is missing.")
        return super().create(validated_data)

class DocumentAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAuditLog
        fields = '__all__'