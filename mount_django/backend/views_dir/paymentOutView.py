from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.paymentOutSerializers import PaymentOutSerializer
from ..models import PaymentOut
from rest_framework.permissions import IsAuthenticated

class PaymentOutApiView(APIView):
    permission_classes =[IsAuthenticated]

    def __get__company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request,pk=None):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no active or owned company!"})
        
        if pk:
            try:
                paymentOut = PaymentOut.objects.get(id= pk)
            except PaymentOut.DoesNotExist:
                raise ValidationError({"error":"No paymentOut transation found!"})
            serializer = PaymentOutSerializer(paymentOut)
            return Response({"paymentOut":serializer.data})
        try:
            paymentOut = PaymentOut.objects.filter(company= company)
        except PaymentOut.DoesNotExist:
            raise ValidationError({"error":"No paymentOut transation found!"})
        serializer = PaymentOutSerializer(paymentOut,many = True)
        return Response({"paymentOut":serializer.data})
    
    def post(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no active or owned company!"})
        
        serializer = PaymentOutSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request,pk):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no active or owned company!"})
        
        try:
            paymentOut = PaymentOut.objects.get(id=pk)
        except PaymentOut.DoesNotExist:
            raise ValidationError({"error":"No such paymentOut transaction exists!"})
        
        serializer = PaymentOutSerializer(paymentOut,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no active or owned company!"})
        
        try:
            paymentOut = PaymentOut.objects.get(id=pk)
        except PaymentOut.DoesNotExist:
            raise ValidationError({"error":"No such paymentOut transaction exists!"})

        paymentOut.delete()
        return Response({"message":"PaymentOut deleted successfully!"})
