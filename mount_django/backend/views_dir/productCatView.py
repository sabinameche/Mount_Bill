from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.productCatSerializers import ProductCatSerializer
from ..models import ProductCategory
from rest_framework.permissions import IsAuthenticated

class ProductCatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def __get__company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})

        try:
            productCategory = ProductCategory.objects.filter(company=company)
        except ProductCategory.DoesNotExist:
            raise ValidationError({"message":"No productCategory found!"})
        serializer = ProductCatSerializer(productCategory,many = True)
        return Response({"category":serializer.data})

    def post(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})
        
        serializer = ProductCatSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})
        
        try:
            productCategory = ProductCategory.objects.get(id=pk,company=company)
        except ProductCategory.DoesNotExist:
            raise ValidationError({"message":"No such productCategory found!"})
        
        serializer = ProductCatSerializer(productCategory,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})
        
        try:
            productCategory = ProductCategory.objects.get(id=pk,company=company)
        except ProductCategory.DoesNotExist:
            raise ValidationError({"message":"No such productCategory found!"})
        
        productCategory.delete()
        return Response({"message": "ProductCategory deleted successfully"})
