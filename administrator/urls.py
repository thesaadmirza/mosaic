from django.urls import path

from . import views

app_name = 'administrator'
urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.CustomersListView.as_view(), name='customers')
]
