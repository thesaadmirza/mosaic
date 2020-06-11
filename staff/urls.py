from django.urls import path

from . import views

app_name = 'staff'
urlpatterns = [

    path('<int:customer>/', views.StaffListView.as_view(), name='index'),
    path('<int:customer>/add', views.StaffCreateView.as_view(), name='add'),
    path('<int:customer>/update/<int:pk>/', views.StaffUpdate.as_view(), name='update'),
    path('<int:customer>/view/<int:pk>/', views.StaffView.as_view(), name='view'),
    path('<int:customer>/delete/<int:pk>/', views.StaffDelete.as_view(), name='delete'),
]
