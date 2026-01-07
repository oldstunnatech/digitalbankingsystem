"""
URL configuration for bankingsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .import settings
from userapp.views import SignUpView 


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
    path("services", TemplateView.as_view(template_name="services.html"), name="services"),
    path("news", TemplateView.as_view(template_name="news.html"), name="news"),
    re_path(r'^accounts/', include("django.contrib.auth.urls")),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name= "signup"),
    re_path(r'^userapp/', include('userapp.urls')),
    re_path(r'^transactionapp/', include('transactionapp.urls')),

]




urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
