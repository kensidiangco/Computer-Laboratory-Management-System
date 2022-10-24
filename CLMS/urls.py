from django.contrib import admin
from django.urls import re_path, path, include
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
    re_path('webpush/', include('webpush.urls')),

    path("notification/push/", v.Web_Push_Notification, name="Web_Push_Notification"),
    
    path('', views.index, name="index"),
    path('login/', views.loginPage, name="loginPage"),
    path('logout', views.userLogout, name='logout'),
    path('dashboard', views.profDashboard, name="profDashboard"),
    path("about", views.About_Us, name="About_Us"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_complete.html'), name='password_reset_complete'),

] 

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
