from django.shortcuts import render
from django.db.models import Count, Q
from django.db import models
from django.http import HttpResponse
import csv
import io
from datetime import date, timedelta
from django.template.loader import get_template
from weasyprint import HTML
from django.utils.dateparse import parse_date
from . models import DisabilityType, ServiceType, PWDRecord, Certificate, MedicalRecords, SupportServices, Complaints, DocumentAuditLog
from .utils.pwd_pdf import generate_pwd_pdf
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['disability_type']
    ordering = ['created_on']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DisabilityType.objects.filter()

    def get(self, request, *args, **kwargs):
        paginator = ModelPagination
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        serializer = DisabilityTypeSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['service_name']
    ordering = ['created_on']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ServiceType.objects.filter()

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
    pagination_class = ModelPagination

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
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)
    
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
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

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
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

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

class PWDRecordExportCSV(APIView):
    permission_classes = (IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer)

    def get(self, request):
        f = PWDRecordFilter(request.GET, queryset=PWDRecord.objects.all())
        records = f.qs 

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Full Name', 'Disability Type', 'Gender', 'community', 'area_council', 'occupation', 'Verified', 'Registration Date'])

        for r in records:
            writer.writerow([r.full_name, r.disability_type, r.gender, r.is_verified, r.registration_date])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pwd_records.csv"'
        return response

def export_pwd_pdf(request):
    search = request.GET.get("search", "")
    is_verified = request.GET.get("is_verified")

    records = PWDRecord.objects.all()

    if search:
        records = records.filter(full_name__icontains=search) | records.filter(contact_number__icontains)

    if is_verified in ["true", "false"]:
        records = records.filter(is_verified=(is_verified == "true"))

    template = get_template("pdf/pwd_report.html")
    html = template.render({"records": records})
    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PWD_Records_Report.pdf"'
    return response

class PWDPrintSelectedPDFView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer]

    def post(self, request):
        ids = request.data.get("ids", [])

        records = PWDRecord.objects.filter(id__in=ids)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=pwd_selected_records.pdf"

        generate_pwd_pdf(response, records)
        return response

class PrintAllPWD(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSocialWorkerOrMedicalOfficer]

    def get(self, request):
        records = PWDRecord.objects.all().order_by('registration_date')

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=pwd_all_records.pdf"

        generate_pwd_pdf(response, records)
        return response

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pwd_id__full_name']
    ordering = ['created_at']
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pwd_id__full_name']
    ordering = ['last_checkup_date']
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'service_name']
    ordering = ['approval_date']
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pwd_id__full_name']
    ordering = ['reported_at']
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