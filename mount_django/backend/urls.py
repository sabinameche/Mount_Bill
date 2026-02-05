from django.urls import path
from .views import CustomerApiView,ProductApiView,ExpenseApiView,ProductCatApiView,ExpenseCatApiView,PaymentInApiView,PaymentOutApiView,OrderListApiView,BalanceAdjustApiView,PermissionApiview,RoleApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # for user management permission
    path("permissions/<int:group_id>/",PermissionApiview.as_view()),
    path("roles/",RoleApiView.as_view()),

    # api for client
    path("client/",CustomerApiView.as_view(),name="customer_list"),
    path("client/<int:pk>/",CustomerApiView.as_view(),name="customer_detail"),

    # api for product
    path("product/",ProductApiView.as_view()),
    path("product/<int:pk>/",ProductApiView.as_view()),

    # api for productCategory
    path("productCat/",ProductCatApiView.as_view()),
    path("productCat/<int:pk>/",ProductCatApiView.as_view()),

    # api for expense
    path("expense/",ExpenseApiView.as_view()),
    path("expense/<int:pk>/",ExpenseApiView.as_view()),

    # api for expenseCategory
    path("expenseCat/",ExpenseCatApiView.as_view()),
    path("expenseCat/<int:pk>/",ExpenseCatApiView.as_view()),

    # for paymentIn
    path("paymentIn/",PaymentInApiView.as_view()),
    path("paymentIn/<int:pk>/",PaymentInApiView.as_view()),

    # for paymentOut
    path("paymentOut/",PaymentOutApiView.as_view()),
    path("paymentOut/<int:pk>/",PaymentOutApiView.as_view()),

    # for orderlist
    path('bill/',OrderListApiView.as_view()),
    path('bill/<int:pk>/',OrderListApiView.as_view()),

    # for balanceadjustment
    path('balanceAdjust/',BalanceAdjustApiView.as_view()),
    path('balanceAdjust/<int:pk>/',BalanceAdjustApiView.as_view())
]
