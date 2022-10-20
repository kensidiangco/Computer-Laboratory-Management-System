from django.urls import path
from . import views

urlpatterns = [
    path('forms/', views.formPage, name="formPage"),
    path('register/prof/', views.profRegisterPage, name="profRegisterPage"),
    path('register/itdept/', views.ITDeptAccountRegister, name="ITDeptAccountRegister"),
    path('register/dean/', views.deanRegisterPage, name="deanRegisterPage"),

    path('admin/dashboard/', views.adminDashboard, name="adminDashboard"),
    path('ITDept/dashboard/', views.ITDeptDashboard, name="ITDeptDashboard"),
    path('dean/dashboard/', views.deanDashboard, name="deanDashboard"),
    path('profile/', views.profile, name="profile"),
    
    path("password_reset", views.password_reset_request, name="password_reset"),

    path("notifications", views.notification_page, name="notification_page")
]