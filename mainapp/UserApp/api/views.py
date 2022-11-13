from rest_framework import status
from rest_framework.response import Response

from UserApp.models import Uye, UyeDiscordLog, UyeAccisDead, UyeAcc
from UserApp.api.serializers import UyeDiscordLogSerializer, UyeSerializer, UyeAccisDeadSerializer

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class UyeDiscordAccListCreateAPIView(APIView):

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
    

class UyeAPIView(APIView):
    def get_object(self, pk):
        dc_instance = get_object_or_404(Uye, UyeID=pk)
        return dc_instance

    # def get(self, request, pk):
    #     uye = self.get_object(pk=pk)
    #     serializer = UyeSerializer(uye)
    #     return Response(serializer.data)    
    
    # def put(self, request, pk):
    #     uye = self.get_object(pk=pk)
    #     serializer = UyeSerializer(uye, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_LastDiscordID(self, pk):
        uyeAccList = UyeAcc.objects.filter(UyeID = Uye(UyeID = pk))
        uye = Uye.objects.get(UyeID=pk)
        return uye, uyeAccList

    def put(self, request, pk):

        """
        gelen UyeID ile o üyenin daha önceki Discord hesabının
        bulunduğu sunuculardan yetkisizleştrilmesi için UyeAccisDead Tablosuna
        FirmaID ile ilgili DiscordId yi ekliyoruz, Role botları beli bir süre içinde
        gelip ilgili FirmaID ile UyeAccisDeadAPIView Class ına bir get request atıyor ve yetkisizleştrilecek Discord hesaplarını 
        respons da alıp gerekli işlemi yapıyor. Daha sonrada  UyeAccisDeadAPIView Class ına delete request i ile tabloda ki kayıtları siliyor.
        """

        _user, uyeAccList = self.get_LastDiscordID(pk)
        for u in uyeAccList:
            user = {"DiscordID":str(_user.DiscordID), "FirmaID": u.FirmaID.FirmaID}
            serializer = UyeAccisDeadSerializer(data=user)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        """uye hesap doğrulamasından sonra discord ID günceleme"""
        uye = self.get_object(pk=pk)
        serializer = UyeSerializer(uye, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status= status.HTTP_201_CREATED)

class UyeAccisDeadAPIView(APIView):

    # def get_object(self, pk):
    #     dead_instance = get_object_or_404(UyeAccisDead, DeadID=pk)
    #     return dead_instance



    def get(self, request, pk):
        uye = UyeAccisDead.objects.filter(FirmaID=pk)
        serializer = UyeAccisDeadSerializer(uye, many=True)
        return Response(serializer.data)  


   

    def delete(self, request, pk):
        uye = UyeAccisDead.objects.filter(FirmaID=pk)
        uye.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
