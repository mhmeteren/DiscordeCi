from rest_framework import status
from rest_framework.response import Response

from UserApp.models import Uye, UyeDiscordLog
from UserApp.api.serializers import UyeDiscordLogSerializer

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

class UyeAccListCreateAPIView(APIView):

    def get_object(self, pk):
        dc_instance = get_object_or_404(UyeDiscordLog, DiscordID=pk, TOKENDURUM=False)
        return dc_instance


    def get(self, request, pk):
        dcAcc = self.get_object(pk=pk)
        serializer = UyeDiscordLogSerializer(dcAcc)
        return Response(serializer.data)

    def put(self, request, pk):
        dcAcc = self.get_object(pk=pk)
        serializer = UyeDiscordLogSerializer(dcAcc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)