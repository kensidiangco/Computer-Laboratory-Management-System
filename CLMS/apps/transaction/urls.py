from django.urls import path, include
from . import views

urlpatterns = [
    path('students/export', views.studentListExport, name="studentListExport"),
    
    path('', views.transactionIndexPage, name="transactionIndexPage"),
    path('request/form', views.requestForm, name="requestForm"),
    path('requests', views.requestList, name="requestList"),
    path('request/<int:pk>', views.requestDetails, name="requestDetails"),
]
