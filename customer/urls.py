from django.urls import path

from . import views

app_name = 'customer'
urlpatterns = [

    path('', views.CustomersListView.as_view(), name='index'),
    path('add', views.CustomerCreateView.as_view(), name='add'),
    path('<int:pk>/', views.CustomerView.as_view(), name='view'),
    path('<int:pk>/update', views.CustomersUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.CustomerDelete.as_view(), name='delete'),
]
