from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.balanceAdjustSerializers import BalanceAdjustSerializer
from ..models import BalanceAdjustment
from rest_framework.permissions import IsAuthenticated
# from ..services.customer_service import CustomerService

class BalanceAdjustApiView(APIView):
    def __get__company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no such owned/active company!!"})
        
        balanceadjust = BalanceAdjustment.objects.filter(company=company)
        serializer = BalanceAdjustSerializer(balanceadjust,many = True)
        return Response(serializer.data)
     
    def post(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no such owned/active company!!"})
        
        serializer = BalanceAdjustSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company = company)
        return Response(serializer.data)