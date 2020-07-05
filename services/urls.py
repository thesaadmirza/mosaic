from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServicesListView.as_view(), name='list'),
    path('add', views.ServicesCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', views.ServicesUpdate.as_view(), name='update'),
    path('<int:pk>/', views.ServiceView.as_view(), name='view'),
    path('<int:pk>/delete/', views.ServiceDelete.as_view(), name='delete'),

    # ajax requests
    path('<int:type>/ajax/getServices', views.get_service, name='services_list_from_type'),
]
