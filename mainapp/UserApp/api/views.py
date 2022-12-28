from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response

from UserApp.models import Uye, UyeDiscordLog, UyeAccisDead, UyeAcc, WalletLogStatus
from UserApp.api.serializers import *

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


    def get_LastDiscordID(self, pk):
        uyeAccList = UyeAcc.objects.filter(UyeID = Uye(UyeID = pk))
        uye = Uye.objects.get(UyeID=pk)
        return uye, uyeAccList

    def put(self, request, pk):
        """
        Gelen UyeID ile o üyenin daha önceki Discord hesabının
        bulunduğu sunuculardan yetkisizleştrilmesi için UyeAccisDead Tablosuna
        FirmaID ile ilgili DiscordId yi ekliyoruz, Role botları beli bir süre içinde
        gelip ilgili FirmaID ile UyeAccisDeadAPIView Class ına bir get request atıyor ve yetkisizleştrilecek Discord hesaplarını 
        response da alıp gerekli işlemi yapıyor. Daha sonrada  UyeAccisDeadAPIView Class ına delete request i ile tabloda ki kayıtları siliyor.
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
    """
    Kullanılmayan Discord hesapların çekilip, discord tarafında gerekli rollerin alınması ve kayıtların silinmesi.
    """
    def get(self, request, pk):
        uye = UyeAccisDead.objects.filter(FirmaID=pk)
        serializer = UyeAccisDeadSerializer(uye, many=True)
        return Response(serializer.data)  


    def delete(self, request, pk):
        uye = UyeAccisDead.objects.filter(FirmaID=pk)
        uye.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


class UyeAccPermissionsControl(APIView):

    def get(self, request, pk):
        UyeAccList = UyeAcc.objects.filter(FirmaID = pk)
        DiscordIDList = []
        for uye in UyeAccList:
            DiscordIDList.append(uye.UyeID)
        
        serializer = UyeSerializer(DiscordIDList, many=True)
        return Response(serializer.data)
        

class UyeAccAPIView(APIView):
    """
    Kullanıcının discord üzerinden herhangi bir alışveriş sunucusundan yaptığı ürün ile ilgili
    istekler içi kullanıcının alışveriş hesaplarına API erişim ile TOKEN ı listeleme
    """
    def get_object(self, DiscordID):
        dc_instance = get_object_or_404(Uye, DiscordID=DiscordID)
        return dc_instance
    
    def get_Access(self, uye: Uye, FirmaID : int):
        uyaAcc = get_object_or_404(UyeAcc, UyeID = uye, FirmaID=FirmaID)
        return uyaAcc
    
    def get(self, request, discordid):
        """
        1. Istekte bulunan kullanıcının Discord ID sistem de kayıtlı mı? (y/N)
        2. Kayıtlıysa ilgili firmada doğrulanmış hesap erişim TOKEN ı var mı? (y/N)
            - y/y : Kullanıcı hesap bilgilerini response da gönder
        3. ve TOKEN sistem de aktif edilmiş mi? (y/N)
            - y : Kullanıcını hesap erişim TOKEN ı ile ilgili siteye
            girilen parametrelerle ürün request i gönder. (Bunu Discord bot kendi içinde yapıyor.)
        """
        firmaId = request.query_params.get('firmaId')
        uye = self.get_object(DiscordID=discordid)
        uyaAcc = self.get_Access(uye=uye, FirmaID=firmaId)
        serializer = UyeAccSerializer(uyaAcc)
        return Response(serializer.data)    
    

class UyeDiscordControlAPIView(APIView):
    """
    Kullanıcının discord üzerinden alışveriş yaparken, sanal cüzdanında yeterli miktarda bakiye
    var olup olmadığını kontrol eder. Eğer yeterli miktar bakiye varsa Kullanıcı hesap bilgileri ve adres bilgilerini response da gönder.
    """
    def get_object(self, discordid):
        dc_instance = get_object_or_404(Uye, DiscordID=discordid)
        return dc_instance


    def get(self, request, discordid):
        try:
            totalfee = Decimal(request.data["totalfee"])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        uye = self.get_object(discordid=discordid)
        if uye.UyeWALLET < totalfee:
            return Response({
                "islem":{
                    'message': 'Sanal cüzdanda yeterli miktarda bakiye yok!'
                }
            }) 
        serializer = UyeDiscordControlSerializer(uye)
        return Response(serializer.data)    


class UyeWalletAndAlisverisLogAPIView(APIView):
    """
    Kullanıcının yaptığı alışverişlerin ve sanal cüzdan hareketlerinin loglanması
    """
    def get_User_with_discordId(self, DiscordId: int):
        user_instance = get_object_or_404(Uye, DiscordID=DiscordId)
        return user_instance


    def post(self, request):
        """
        Her iki tabloya(UyeWalletLog, UyeAlisverisLog) Loglama
        """

        try:
            DiscordId = request.data["DiscordId"]
            Firma = request.data["Firma"]
            WalletLogAmount = request.data["WalletLogAmount"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        uye = self.get_User_with_discordId(DiscordId=DiscordId)
        if Decimal(WalletLogAmount) <= uye.UyeWALLET:
            UyeWalletLogDict = dict(
                UyeID=uye.UyeID,
                UyeWALLET=uye.UyeWALLET,
                UyeWalletLogIslem=WalletLogStatus.ALISVERIS,
                UyeWalletLogAmount = WalletLogAmount
            )

            UyeAlisverisLogDict = dict(
                Uye=uye.UyeID,
                Firma=Firma,
                WalletBalance=uye.UyeWALLET,
                WalletLogAmount=WalletLogAmount
            )

            Walletserializer = UyeWalletLogserializer(data=UyeWalletLogDict)
            Alisverisserializer = UyeAlisverisLogserializer(data=UyeAlisverisLogDict)

            try:
                if Walletserializer.is_valid(raise_exception=True) and Alisverisserializer.is_valid(raise_exception=True):
                    Walletserializer.save()
                    Alisverisserializer.save()
                    uye.UyeWALLET = uye.UyeWALLET - Decimal(WalletLogAmount) # Kullanıcı sanal cüzdan bakiye güncelleme
                    uye.save()
                    return Response(dict(
                        WalletserializerData=Walletserializer.data,
                        AlisverisserializerData=Alisverisserializer.data
                        ),
                    status= status.HTTP_201_CREATED)
            except serializers.ValidationError:
                return Response(dict(
                        WalletserializerErrors=Walletserializer.errors,
                        AlisverisserializerErrors=Alisverisserializer.errors
                        ),
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "islem":{
                    "message": "Sanal cüzdanda yeterli miktarda bakiye yok!"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
