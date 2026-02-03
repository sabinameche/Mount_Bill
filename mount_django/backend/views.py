from django.shortcuts import render

# Create your views here.
from .views_dir.customerView import CustomerApiView
from .views_dir.productView import ProductApiView
from .views_dir.expenseView import ExpenseApiView
from .views_dir.productCatView import ProductCatApiView
from .views_dir.expenseCatView import ExpenseCatApiView
from .views_dir.paymentInView import PaymentInApiView
from .views_dir.paymentOutView import PaymentOutApiView
from .views_dir.orderListView import OrderListApiView
from .views_dir.balanceAdjustView import BalanceAdjustApiView

CustomerApiView = CustomerApiView
ProductApiView = ProductApiView
ProductCatApiView = ProductCatApiView
ExpenseApiView = ExpenseApiView
ExpenseCatApiView = ExpenseCatApiView
PaymentInApiView = PaymentInApiView
PaymentOutApiView = PaymentOutApiView
OrderListApiView = OrderListApiView
BalanceAdjustApiView = BalanceAdjustApiView

        

    
        
