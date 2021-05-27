"""oxiterp URL Configuration

The `urlpatterns` list routes URLs to Views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function Views
    1. Add an import:  from my_app import Views
    2. Add a URL to urlpatterns:  path('', Views.home, name='home')
Class-based Views
    1. Add an import:  from other_app.Views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from oxiterp.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
import accounts

from accounts import views

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('', views.login, name='index'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),

    path('car-service/', include('carService.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'education.Views.ErrorViews.page_not_found'
# handler500 = 'education.Views.ErrorViews.page_not_found'
