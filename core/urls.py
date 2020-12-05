"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', include('administrator.urls'), name="administrator"),
                  path('services/', include('services.urls'), name="services"),
                  path('booking/', include('booking.urls'), name="booking"),
                  path('projects/', include('projects.urls'), name="projects"),
                  path('customer/', include('customer.urls'), name="customer"),
                  path('staff/', include('staff.urls'), name="staff"),
                  path('user/', include('users.urls'), name="users"),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('allauth.urls'), name="accounts"),
                  path('i18n/', include('django.conf.urls.i18n')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
