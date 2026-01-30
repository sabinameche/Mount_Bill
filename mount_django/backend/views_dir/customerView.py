from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.customerSerializers import CustomerSerializer
from ..models import Customer
from rest_framework.permissions import IsAuthenticated

class CustomerApiView(APIView):
    permission_classes = [IsAuthenticated]

    def __get_company(self):
        return self.request.user.active_company or self.request.user.owned_company
    
    def get(self,request):
        company = self.__get_company()

        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        customers = Customer.objects.filter(company=company)
        serializer = CustomerSerializer(customers,many = True)

        return Response({"clients":serializer.data})
    
    def post(self,request):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company = company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        try:
            customer = Customer.objects.get(id=pk,company=company)
        except Customer.DoesNotExist:
            return Response({"message": "No such customer found"}, status=404)
        serializer = CustomerSerializer(customer,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self,request,pk):
        company = self.__get_company()
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})

        try:
            customer = Customer.objects.get(id=pk,company=company)
        except Customer.DoesNotExist:
            return Response({"message": "No such customer found"})
        
        customer.delete()
        return Response({"message": "Customer deleted successfully"})
