from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.balanceAdjustSerializers import BalanceAdjustSerializer
from ..models import BalanceAdjustment
from rest_framework.permissions import IsAuthenticated
from ..services.balanceAdjust_service import BalanceAdjustService

class BalanceAdjustApiView(APIView):
    permission_classes = [IsAuthenticated]
    def __get__company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no such owned/active company!!"})
        
        balanceadjust = BalanceAdjustment.objects.select_related("remainings").filter(customer__company = company)
        serializer = BalanceAdjustSerializer(balanceadjust,many = True)

        return Response({"balance_adjust":serializer.data})
     
    def post(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no such owned/active company!!"})
        
        serializer = BalanceAdjustSerializer(data = request.data)
        if serializer.is_valid():
            try:
                balance_adjustment = BalanceAdjustService.create_balance_adjustment(serializer.validated_data,company=company)
                balance_adjustment_data = BalanceAdjustSerializer(balance_adjustment).data

                return Response({"success": True,
                                "balance_adjustment_data":balance_adjustment_data,
                                "message": "BalanceAdjustment done successfully."
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)