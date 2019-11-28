"""yadirect_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from yadirect_api import views

router = routers.DefaultRouter()
router.register(r'api', views.ApiDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Статика работает при выключенном DEBUG
if settings.DEBUG is False:
    urlpatterns += [path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT, }),
                    path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}), ]
