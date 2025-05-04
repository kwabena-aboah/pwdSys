"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from users.views import UserViewset, verify_mfa
from pwd_records.views import DisabilityTypeViewSet, ServiceTypeViewSet, PWDRecordViewSet, PWDSearchView, PWDReportView, PWDByDisabilityView, VerifiedPWDCountView, CertificateViewSet, MedicalRecordsViewSet, SupportServicesViewSet, ComplaintsViewSet, DocumentVerificationView, UploadAndVerifyDocumentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'disability_type', DisabilityTypeViewSet)
router.register(r'service_type', ServiceTypeViewSet)
router.register(r'pwd_records', PWDRecordViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'medical_records', MedicalRecordsViewSet)
router.register(r'support_services', SupportServicesViewSet)
router.register(r'complaints', ComplaintsViewSet)
router.register(r'users', UserViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/pwd/search/', PWDSearchView.as_view(), name='pwd-search'),
    path('api/pwd/report/', PWDReportView.as_view(), name='pwd-report'),
    path('api/pwd/disability-report/', PWDByDisabilityView.as_view(), name='pwd-disability-report'),
    path('api/pwd/verified-report/', VerifiedPWDCountView.as_view(), name='pwd-verified-report'),
    path('api/pwd/verify-document/', DocumentVerificationView.as_view(), name='verify-document'),
    path('api/pwd/upload-and-verify/', UploadAndVerifyDocumentView.as_view(), name='upload-and-verify'),
    path('api/verify-mfa/', verify_mfa, name='verify-mfa'),
    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)