from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('calendar', views.calendar, name='calendar'),
    path('', views.BookingListView.as_view(), name='list'),
    path('add', views.BookingCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', views.BookingsUpdate.as_view(), name='update'),
    path('<int:pk>/', views.BookingView.as_view(), name='view'),
    path('<int:pk>/delete/', views.BookingDelete.as_view(), name='delete'),
    path('store/', views.store_booking, name="store"),
]
