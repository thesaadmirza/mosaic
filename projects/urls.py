from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projectsview, name='list'),
    path('<int:pk>/', views.BookingView.as_view(), name='view'),
    path('create_dir/', views.testingdir, name="create_dir"),
    path('delete_folder/', views.delete_folder, name="delete_folder"),
    path('rename_folder_file/', views.rename_folder_file, name='rename_folder_file'),

    # File Manager URls
    path('create_folder/', views.folder_create, name='folder_create'),
    path('get_filemanager_content/<int:pk>', views.filemanager_content, name="filemanager_content"),
    path('get_filemanager_content_public/<int:pk>', views.filemanager_content_public,
         name="filemanager_content_public"),

    # admin url
    path('get_filemanager_content_admin/', views.filemanager_content_admin, name="filemanager_content_admin"),

    path('upload_files_manager/', views.upload_files, name='upload_files_manager'),
    path('public_project_view/<int:pk>', views.public_project_view, name='public_project_view'),
]
