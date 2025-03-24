from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from .serializers import UserSerializer
from .models import User

User = get_user_model()

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination
    

# class LoginView(APIView):
# 	def post(self, request):
# 		username = resquest.data.get('username')
# 		password = request.data.get('password')
# 		otp_token = request.data.get('otp_token')

# 		user = authenticate(username=username, password=password)

# 		if user is not None:
# 			# Verify OTP
# 			device = TOTPDevice.objects.filter(user=user).first()
# 			if device and device.verify_token(otp_token):
# 				token, created = Token.objects.get_or_create(user=user)
# 				return Response({'token': token.key, 'role': user.role})
# 			return Response({'error': 'Invalid OTP'}, status=400)
# 		return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_mfa(request):
	username = request.data.get('username')
	otp_token = request.data.get('otp_token')
	if TOTPDevice.objects.get(username) == otp_token:
		token = f"fake-token-for-{username}"
		del TOTPDevice[username]
		user = User.objects.get(username=username)
		return Response({"message": "MFA verified", "token": token, "user": UserSerializer(user).data})
	else:
		return Response({"error": "Invaild OTP"}, status=status.HTTP_400_BAD_REQUEST)