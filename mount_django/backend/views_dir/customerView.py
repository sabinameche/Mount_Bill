from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.customerSerializers import CustomerSerializer
from ..models import Customer
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from ..services.customer_service import CustomerService

class CustomerApiView(APIView):
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Customer.objects.all()
    
    def __get_company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request,pk=None):
        company = self.__get_company()

        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        if pk:
            try:
                customer = Customer.objects.get(id=pk,company=company)
            except Customer.DoesNotExist:
                raise ValidationError({"error":"No such client found!"})
            serializer = CustomerSerializer(customer)
            return Response({"clients":serializer.data})
        try:
            customers = Customer.objects.filter(company=company)
        except Customer.DoesNotExist:
            raise ValidationError({"message":"No Clients found!"})
        serializer = CustomerSerializer(customers,many = True)

        return Response({"clients":serializer.data})
    
    def post(self, request):
        company = self.__get_company()

        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = CustomerService.create_customer(
                    serializer.validated_data,
                    company=company 
                )
                customer_data = CustomerSerializer(customer).data
                return Response({"success": True,"client":customer_data,"message": "Customer created successfully."
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        else:
            return Response({"success": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no active/owned company!!"})
        
        try:
            customer = Customer.objects.get(id=pk,company=company)
        except Customer.DoesNotExist:
            return Response({"message": "No such client found"}, status=404)
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
            return Response({"message": "No such client found"})
        
        customer.delete()
        return Response({"message": "Client deleted successfully"})
