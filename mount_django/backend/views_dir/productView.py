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
        return self.request.user.owned_company or self.request.user.active_company

    def get(self, request, pk=None):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company": "User has no owned_company or active_company!"})

        try:
            if pk:
                # Fetch single product
                product = Product.objects.get(id=pk, company=company)
                serializer = ProductSerializer(product)
                return Response({"products": serializer.data}, status=status.HTTP_200_OK)
            else:
                # Fetch all products for the company
                products = Product.objects.filter(company=company)
                if not products.exists():
                    return Response({"products": [], "message": "No products found!"}, status=status.HTTP_200_OK)
                serializer = ProductSerializer(products, many=True)
                return Response({"products": serializer.data}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            # Only triggered if pk is provided and product is not found
            raise ValidationError({"error": "No such Product found!"})
        except Exception as e:
            # Catch any other unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company": "User has no owned_company or active_company!"})

        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(company=company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Return validation errors if serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"company": "User has no owned_company or active_company!"})

        try:
            # Fetch the product
            product = Product.objects.get(id=pk, company=company)

            # Partial update
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Return serializer validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            # Product not found for the given company and pk
            return Response({"message": "No such product found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Catch unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
