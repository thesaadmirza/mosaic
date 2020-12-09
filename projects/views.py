from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
import fsutil
import os


# Create your views here.
class BookingView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'admin/projects/view.html'

    def get_context_data(self, **kwargs):
        context = super(BookingView, self).get_context_data(**kwargs)
        project_dir = settings.PROJECT_ROOT + '/' + str(self.object.id)
        context['current_path'] = project_dir
        context['folders'] = create_brudcrumbs(project_dir, str(self.object.id))
        try:
            dir_exist = fsutil.assert_exists(project_dir)
            context['dirs'] = fsutil.list_dirs(project_dir)
            context['files'] = fsutil.list_files(project_dir)
        except Exception as e:
            fsutil.create_dir(project_dir, overwrite=False)
            context['dirs'] = fsutil.list_dirs(project_dir)
            context['files'] = fsutil.list_files(project_dir)

        return context


def projectsview(request):
    project_dir = settings.PROJECT_ROOT
    current_path = project_dir
    folders = create_brudcrumbs(project_dir)
    try:
        dir_exist = fsutil.assert_exists(project_dir)
        dirs = fsutil.list_dirs(project_dir)
        files = fsutil.list_files(project_dir)
    except Exception as e:
        dirs = []
        files = []
    return render(request, 'admin/projects/admin_filemanager.html',
                  {'current_path': current_path, 'dirs': dirs, 'files': files})


def public_project_view(request, pk):
    project_dir = settings.PROJECT_ROOT + '/' + str(pk)
    current_path = project_dir
    folders = create_brudcrumbs(project_dir)
    try:
        dir_exist = fsutil.assert_exists(project_dir)
        dirs = fsutil.list_dirs(project_dir)
        files = fsutil.list_files(project_dir)
    except Exception as e:
        dirs = []
        files = []
    return render(request, 'admin/projects/public_manager.html',
                  {'current_path': current_path, 'dirs': dirs, 'files': files, 'id': str(pk)})


def testingdir(request, **kwargs):
    dirs = fsutil.list_dirs(settings.PROJECT_ROOT)
    files = fsutil.list_files(settings.PROJECT_ROOT)
    result = fsutil.assert_file(files[0])
    basename, extension = fsutil.split_filename(files[0])
    moreresult = fsutil.copy_file(files[0], settings.PROJECT_ROOT + '/saadtesting124/' + basename + '.' + extension,
                                  overwrite=False, **kwargs)
    fsutil.assert_exists(settings.PROJECT_ROOT + '/saadtesting124')
    return HttpResponse('HI, Done')


def folder_create(request):
    name = request.POST.get('folder', False)
    path = request.POST.get('path', False)
    if name and path:
        try:
            path = path + '/' + name
            fsutil.assert_not_exists(path)
            fsutil.create_dir(path, overwrite=False)
            return JsonResponse({'message': 'success', 'data': path}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'failure', 'data': 'Folder with same name already exist.'}, status=403)
    else:
        return JsonResponse({'message': 'failure', 'data': 'Please Enter Valid Name'}, status=403)


def rename_folder_file(request):
    name = request.POST.get('name', False)
    path = request.POST.get('path', False)
    if name and path:
        try:
            fulpath = request.POST.get('fullPath', False)
            path = fulpath + '/' + path
            type = request.POST.get('type', False)
            if type == "folder":
                fsutil.rename_dir(path, name)
            else:
                fsutil.rename_file_basename(path, name)
            return JsonResponse({'message': 'success', 'data': path}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'failure', 'data': 'Unable to Rename the. Try Again After Refresh.'},
                                status=403)
    else:
        return JsonResponse({'message': 'failure', 'data': 'Please Enter Valid Name'}, status=403)


def delete_folder(request):
    path = request.POST.get('path', False)
    if path:
        try:
            type = request.POST.get('type', False)
            if type == "folder":
                fsutil.delete_dir(path)
            else:
                fsutil.delete_file(path)
            return JsonResponse({'message': 'success', 'data': path}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'failure', 'data': 'Unable to Delete Folder, Not Found.'}, status=403)
    else:
        return JsonResponse({'message': 'failure', 'data': 'Whoopx, Something Went Wrong'}, status=403)


def filemanager_content(request, pk):
    path = request.POST.get('path', False)
    project = str(pk)
    if path:
        current_path = settings.PROJECT_ROOT + '/' + project
        folders = create_brudcrumbs(path, project)
        try:
            dir_exist = fsutil.assert_exists(path)
            dir = fsutil.list_dirs(path)
            files = fsutil.list_files(path)
        except Exception as e:
            dir = []
            files = []
    else:
        current_path = path
        dir = []
        files = []
    converted_string = render_to_string('admin/projects/filemanager.html',
                                        {'dirs': dir, 'files': files, 'current_path': current_path, 'folders': folders})
    return HttpResponse(converted_string)


def filemanager_content_public(request, pk):
    path = request.POST.get('path', False)
    project = str(pk)
    if path:
        current_path = settings.PROJECT_ROOT + '/' + project
        folders = create_brudcrumbs(path, project)
        try:
            dir_exist = fsutil.assert_exists(path)
            dir = fsutil.list_dirs(path)
            files = fsutil.list_files(path)
        except Exception as e:
            dir = []
            files = []
    else:
        current_path = path
        dir = []
        files = []
    converted_string = render_to_string('admin/projects/public/filemanager.html',
                                        {'dirs': dir, 'files': files, 'current_path': current_path, 'folders': folders})
    return HttpResponse(converted_string)


def filemanager_content_admin(request):
    path = request.POST.get('path', False)
    if path:
        current_path = settings.PROJECT_ROOT
        folders = create_brudcrumbs(path)
        try:
            dir_exist = fsutil.assert_exists(path)
            dir = fsutil.list_dirs(path)
            files = fsutil.list_files(path)
        except Exception as e:
            dir = []
            files = []
    else:
        current_path = path
        dir = []
        files = []
    converted_string = render_to_string('admin/projects/filemanager.html',
                                        {'dirs': dir, 'files': files, 'current_path': current_path, 'folders': folders})
    return HttpResponse(converted_string)


def create_brudcrumbs(path, project_id=False):
    sliced = path.split('media_root/projects/')
    fullurl = settings.PROJECT_ROOT
    if len(sliced) == 2:
        sliced = sliced[1].split('/')
        newarray = []
        for slic in sliced:
            fullurl = fullurl + '/' + slic
            newarray.append(fullurl)
    else:
        newarray = []
    return newarray


def handle_uploads(request, path):
    saved = []

    upload_dir = path
    upload_full_path = path

    if os.path.exists(upload_full_path):

        if request.FILES:
            for file in request.FILES.getlist('files'):
                upload = file
                while os.path.exists(os.path.join(upload_full_path, upload.name)):
                    upload.name = '_' + upload.name
                dest = open(os.path.join(upload_full_path, upload.name), 'wb')
                for chunk in upload.chunks():
                    dest.write(chunk)
                dest.close()

    # returns [(key1, path1), (key2, path2), ...]
    return saved


def upload_files(request):
    path = request.POST.get('path', False)
    result = handle_uploads(request, path)
    return JsonResponse({'message': 'success', 'data': 'Successfully Updated.'}, status=200)
