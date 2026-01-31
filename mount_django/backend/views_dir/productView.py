from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.productSerializers import ProductSerializer
from ..models import Product
from rest_framework.permissions import IsAuthenticated

class ProductApiView(APIView):
    permission_classes = [IsAuthenticated] 

    def __get_company(self):
        return self.request.user.active_company or self.request.owned_company  
    
    def get(self,request,pk=None):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no owned_company or active_company!!"})

        if pk:
            try:
                product = Product.objects.get(id=pk,company=company)
            except Product.DoesNotExist:
                raise ValidationError({"error":"No such Product found!"})
            serializer = ProductSerializer(product)
            return Response({"products":serializer.data})

        try:    
            product = Product.objects.filter(company=company)
        except Product.DoesNotExist:
            raise ValidationError({"message":"No products found!"})
        serializer = ProductSerializer(product,many=True)
        return Response({"products":serializer.data})

    def post(self,request):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no owned_company or active_company!!"})
        
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no owned_company or active_company!!"})
        
        try:
            product = Product.objects.get(id=pk,company=company)
        except Product.DoesNotExist:
            return Response({"message": "No such product found"}, status=404)
        serializer = ProductSerializer(product,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400 )
    
    def delete(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company":"User has no owned_company or active_company!!"})
        
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"message": "No such product found"})
        product.delete()
        return Response({"message": "Product deleted successfully"})
