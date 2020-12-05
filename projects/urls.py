from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('<int:pk>/', views.BookingView.as_view(), name='view'),
    path('create_dir/', views.testingdir, name="create_dir"),

    # File Manager URls
    path('create_folder/', views.folder_create, name='folder_create'),
    path('get_filemanager_content/<int:pk>', views.filemanager_content, name="filemanager_content"),
    path('upload_files_manager/', views.upload_files, name='upload_files_manager'),
]
