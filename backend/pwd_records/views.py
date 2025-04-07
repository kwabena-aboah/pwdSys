from django.shortcuts import render
from django.db.models import Q
from django.db import models
from datetime import date, timedelta
from . models import DisabilityType, ServiceType, PWDRecord, Certificate, MedicalRecords, SupportServices, Complaints
from .serializers import DisabilityTypeSerializer, ServiceTypeSerializer, PWDRecordSerializer, CertificateSerializer, MedicalRecordsSerializer, SupportServicesSerializer, ComplaintsSerializer
from .permissions import IsAdminOrSocialWorkerOrMedicalOfficer, IsOwnerOrReadOnly
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS

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

class ServiceTypeSearchView(ListAPIView):
    serializer_class = ServiceTypeSerializer
    pagination_class = ModelPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return ServiceType.objects.filter(
                Q(service_name__icontains=query)
            )
        return ServiceType.objects.none()

class PWDRecordViewSet(viewsets.ModelViewSet):
    queryset = PWDRecord.objects.all()
    serializer_class = PWDRecordSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['is_verified', 'disability_type']
    ordering_fields = ['is_verified', 'registration_date']
    ordering = ['registration_date']
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return PWDRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('q', '').strip()
        pwd_record = self.get_queryset()
        if query:
            return pwd_record.filter(
                Q(full_name__icontains=query) | Q(contact_number__icontains=query)
            )
        if pwd_record.exists():
            serializer = self.get_serializer(pwd_record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No records found"}, status=status.HTTP_204_NO_CONTENT)

        paginator = ModelPagination()
        paginated_queryset = paginator.paginate_queryset(pwd_record, request)
        serializer = PWDRecordSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data, status=status.HTTP_200_OK)

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

    def update(self, request, *args, **kwargs):
        """ Ensure optional picture upload on edit """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'medical_certificate' in request.data and not request.data['medical_certificate']:
            request.data.pop('medical_certificate')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer)

class MedicalRecordsViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecords.objects.all()
    serializer_class = MedicalRecordsSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

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