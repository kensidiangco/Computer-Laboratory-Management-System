"""CLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from CLMS.apps.account import views
from CLMS.apps.transaction import views as v
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('CLMS.apps.account.urls')),
    path('schedule/', include('CLMS.apps.transaction.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    
    path('', views.index, name="index"),
    path('login/', views.loginPage, name="loginPage"),
    path('logout', views.userLogout, name='logout'),
    path('dashboard', views.profDashboard, name="profDashboard"),
    path("about", views.About_Us, name="About_Us"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
