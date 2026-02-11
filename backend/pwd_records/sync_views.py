from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from .models import PWDRecord
from .serializers import PWDRecordSerializer

class SyncPWD(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data.copy()

		external_id = data.get('local_id')

		if PWDRecord.objects.filter(external_id=external_id).exists():
			return Response({"status": "already_synced"})

		serializer = PWDRecordSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save(external_id=external_id)

		return Response({"status": "synced"})