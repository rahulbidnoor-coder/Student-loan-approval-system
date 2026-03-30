from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('loan/', views.loan_view, name='loan'),
    path('repayment/', views.repayment_view, name='repayment'),

]