from django.urls import path, include
from . import views

urlpatterns = [
    path('students/export', views.studentListExport, name="studentListExport"),
    
    path('', views.transactionIndexPage, name="transactionIndexPage"),
    path('request', views.schedRequestPage, name="schedRequestPage"),
]
