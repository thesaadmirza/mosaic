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
    path('update/<int:pk>/', views.update_booking, name="custom_update"),
    path('get_events_json/', views.booking_events_json, name="get_events_json"),
    path('get_booking_json/<int:pk>/', views.booking_json_modal, name="get_booking_json"),
    path('time_calendar/', views.timeCalendar, name="time_calendar"),
    path('get_slots_json/', views.timeCalendar_json, name="slots_json"),
    path('create_dir/', views.testingdir, name="create_dir"),

    # File Manager URls
    path('create_folder/', views.folder_create, name='folder_create'),
    path('get_filemanager_content/<int:pk>', views.filemanager_content, name="filemanager_content"),
    path('upload_files_manager/', views.upload_files, name='upload_files_manager'),
]
