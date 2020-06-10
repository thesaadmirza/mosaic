from django.urls import path

from . import views

app_name = 'administrator'
urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.CustomersListView.as_view(), name='customers'),
    path('customer/add', views.CustomerCreateView.as_view(), name='addCustomer'),
    path('customer/<int:pk>/', views.CustomerView.as_view(), name='customerview'),
]
