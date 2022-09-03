from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.registerPage, name="registerPage"),
    path('ITDept/register/', views.ITDeptAccountRegister, name="ITDeptAccountRegister"),

    path('admin/dashboard/', views.adminDashboard, name="adminDashboard"),
    path('ITDept/dashboard/', views.ITDeptDashboard, name="ITDeptDashboard"),
    path('theme', views.theme, name="theme"),
    
]