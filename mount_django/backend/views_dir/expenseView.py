from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.expenseSerializers import ExpenseSerializer
from ..models import Expense
from rest_framework.permissions import IsAuthenticated

class ExpenseApiView(APIView):
    permission_classes = [IsAuthenticated]
    def __get_company(self):
        return self.request.user.owned_company or self.request.user.active_company
    
    def get(self,request,pk=None):
        company = self.__get_company()
        if not company:
            raise ValidationError({"error":"User has no owned or active company!!"})
        
        if pk:
            try:
                expense = Expense.objects.get(id=pk,company=company)
            except Expense.DoesNotExist:
                return Response({"message":"No such expense found!"})
            return Response(
                {
                    "expense_number":expense.expense_number,
                    "created_at":expense.created_at,
                    "category":expense.category.name,
                    "total_amount":expense.total_amount,
                    "remarks":expense.remarks or "",
                }
            )
        try:
            expense = Expense.objects.filter(company=company)
        except Expense.DoesNotExist:
            return Response({"message":"No expenses found!"})
        serializer = ExpenseSerializer(expense,many=True)
        return Response({"expenses":serializer.data})
    
    def post(self,request):
        company = self.__get_company()
        if not company:
            raise ValidationError({"error":"User has no owned or active company!!"})
        
        serializer = ExpenseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company=company)
    
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
        
    def patch(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"error":"User has no owned or active company!!"})
        
        try:
            expense = Expense.objects.get(company=company,id=pk)
        except Expense.DoesNotExist:
            raise ValidationError({"error":"No such expense found!"})
        
        serializer =  ExpenseSerializer(expense,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400 )
    
    def delete(self,request,pk):
        company = self.__get_company()
        if not company:
            raise ValidationError({"error":"User has no owned or active company!!"})
        
        try:
            expense = Expense.objects.get(company=company,id=pk)
        except Expense.DoesNotExist:
            raise ValidationError({"error":"No such expense found!"})
        expense.delete()
        return Response({"message":"expense deleted successfully!"})
