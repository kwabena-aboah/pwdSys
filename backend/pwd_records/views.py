from django.shortcuts import render
from django.db.models import Count, Q
from django.db import models
from datetime import date, timedelta
from django.utils.dateparse import parse_date
from . models import DisabilityType, ServiceType, PWDRecord, Certificate, MedicalRecords, SupportServices, Complaints, DocumentAuditLog
from .filters import PWDRecordFilter
from .serializers import DisabilityTypeSerializer, ServiceTypeSerializer, PWDRecordSerializer, CertificateSerializer, MedicalRecordsSerializer, SupportServicesSerializer, ComplaintsSerializer, DocumentAuditLogSerializer
from .permissions import IsAdminOrSocialWorkerOrMedicalOfficer, IsOwnerOrReadOnly
from rest_framework import viewsets, generics, permissions, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .ai_verifier import fake_ai_verify
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
import os

class ModelPagination(LimitOffsetPagination):
    page_size = 10 # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class DisabilityTypeViewSet(viewsets.ModelViewSet):
    queryset = DisabilityType.objects.all()
    serializer_class = DisabilityTypeSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        serializer = DisabilityTypeSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return DisabilityType.objects.filter(disability_type__icontains=query)[:10]

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        serializer = ServiceTypeSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class PWDRecordViewSet(viewsets.ModelViewSet):
    queryset = PWDRecord.objects.all()
    serializer_class = PWDRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PWDRecordFilter
    search_fields = ['full_name', 'contact_number']
    ordering_fields = ['is_verified', 'registration_date']
    ordering = ['registration_date']
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return PWDRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Ensure optional picture upload on edit"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'id_photo' in request.data and not request.data['id_photo']:
            request.data.pop('id_photo')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

# PWD Search view
class PWDSearchView(ListAPIView):
    serializer_class = PWDRecordSerializer
    pagination_class = ModelPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return PWDRecord.objects.filter(
                Q(full_name__icontains=query) |
                Q(contact_number__icontains=query)
            )
        return PWDRecord.objects.none()

# PWD Report Viewset
class PWDReportView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        queryset = PWDRecord.objects.all()

        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        if start_date:
            queryset = queryset.filter(registration_date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(registration_date__lte=parse_date(end_date))

        total_record = queryset.count()
        total_males = queryset.filter(gender='male').count()
        total_females = queryset.filter(gender='female').count()

        return Response({
            "total_record": total_record,
            "total_males": total_males,
            "total_females": total_females
        })

# Report by Disability Viewset
class PWDByDisabilityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = PWDRecord.objects.all()

        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        if start_date:
            queryset = queryset.filter(registration_date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(registration_date__lte=parse_date(end_date))

        result = {}
        for entry in queryset:
            disability = str(entry.disability_type)
            gender = entry.gender.lower()
            if disability not in result:
                result[disability] = {'male': 0, 'female': 0}
            if gender in result[disability]:
                result[disability][gender] += 1
        return Response(result, status=status.HTTP_200_OK)

# Report by Verified PWD Record Viewset
class VerifiedPWDCountView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = PWDRecord.objects.all()

        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        if start_date:
            queryset = queryset.filter(registration_date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(registration_date__lte=parse_date(end_date))

        verified = queryset.filter(is_verified=True).count()
        total = queryset.count()

        return Response({
            'verified': verified,
            'total': total
            })

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginated_queryset(self.queryset, request)
        serializer = CertificateSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """ Ensure optional picture upload on edit """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'medical_certificate' in request.data and not request.data['medical_certificate']:
            request.data.pop('medical_certificate')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class MedicalRecordsViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecords.objects.all()
    serializer_class = MedicalRecordsSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return MedicalRecords.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginated_queryset(self.queryset, request)
        serializer = MedicalRecordsSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class SupportServicesViewSet(viewsets.ModelViewSet):
    queryset = SupportServices.objects.all()
    serializer_class = SupportServicesSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def get_queryset(self):
        return SupportServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginated_queryset(self.queryset, request)
        serializer = SupportServicesSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class ComplaintsViewSet(viewsets.ModelViewSet):
    queryset = Complaints.objects.all()
    serializer_class = ComplaintsSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def get_queryset(self):
        return Complaints.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginated_queryset(self.queryset, request)
        serializer = ComplaintsSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class DocumentVerificationView(APIView):
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def post(self, request):
        doc_type = request.data.get('document_type')
        related_id = request.data.get('related_id')

        try:
            # Select appropriate model
            if doc_type == 'certificate':
                doc = Certificate.objects.get(id=related_id)
                img_path = doc.medical_certificate.path 
            elif doc_type == 'id_card':
                doc = PWDRecord.objects.get(id=related_id)
                img_path = doc.id_photo.path
            else:
                return Response({'error': 'Invalid document type'}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=404)

        is_verified = fake_ai_verify(img_path)

        verification = DocumentAuditLog.objects.create(
            document_type=doc_type,
            related_id=related_id,
            verified=is_verified["verified"],
            result=is_verified["reason"]
        )

        return Response({
            "id": verification.id,
            "verified": verification.verified,
            "result": verification.result,
            "text_extracted": is_verified["text"]
            }, status=200)

class UploadAndVerifyDocumentView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        # Temporarily save the file
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # AI verification
        ai_result = fake_ai_verify(temp_path)

        # Optionally delete after use
        os.remove(temp_path)

        return Response({
            "verified": ai_result["verified"],
            "result": ai_result["reason"],
            "text_extracted": ai_result["text"]
            }, status=200)