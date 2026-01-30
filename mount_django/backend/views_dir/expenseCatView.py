from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.expenseCatSerializers import ExpenseCatSerializer
from ..models import ExpenseCategory,Company
from rest_framework.permissions import IsAuthenticated


# creating global expenseCategory
global_company,created = Company.objects.get_or_create(name="Global")

default_categories = ["Delivery","Miscellaneous","Travel & Transportation","Repair & Maintenance","Utilities","Marketing","Salary","Rent","Electricity"]
for cat_name in default_categories:
    ExpenseCategory.objects.get_or_create(name=cat_name,company=global_company)


class ExpenseCatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def __get__company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})

        try:
            global_company = Company.objects.get(name="Global")
            expenseCategory = ExpenseCategory.objects.filter(company__in = [global_company,company])
            
        except ExpenseCategory.DoesNotExist:
            raise ValidationError({"message":"No such expenseCategory found!"})
        serializer = ExpenseCatSerializer(expenseCategory,many = True)
        return Response(serializer.data)

    def post(self,request):
        company = self.__get__company()
        if not company:
            raise ValidationError({"error":"User has no owned/active company!!"})
        
        serializer = ExpenseCatSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company = company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    