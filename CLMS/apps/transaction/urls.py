from django.urls import path, include
from . import views

urlpatterns = [
    path('students/export', views.studentListExport, name="studentListExport"),
    
    path('', views.transactionIndexPage, name="transactionIndexPage"),
    path('request/form', views.requestForm, name="requestForm"),
    path('request/<int:pk>', views.requestDetails, name="requestDetails"),

    path('requests', views.requestList, name="requestList"),
    path('requests/approved', views.approvedRequest, name="approvedRequest"),
    path('requests/rejected', views.rejectedRequest, name="rejectedRequest"),
]
