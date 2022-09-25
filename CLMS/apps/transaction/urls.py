from django.urls import path, include
from . import views

urlpatterns = [
    path('students/export/', views.studentListExport, name="studentListExport"),
    
    path('', views.transactionIndexPage, name="transactionIndexPage"),
    path('request/form/', views.requestForm, name="requestForm"),
    path('request/<int:pk>/', views.requestDetails, name="requestDetails"),

    path('requests/', views.requestList, name="requestList"),
    path('ongoing/', views.onGoingSchedule, name="onGoingSchedule"),
    path('done/', views.doneSchedule, name="doneSchedule"),
    path('requests/approved/', views.approvedRequest, name="approvedRequest"),
    path('requests/rejected/', views.rejectedRequest, name="rejectedRequest"),

    path('api/notifs/', views.getNotifs, name="getNotifs"),
    path('clear-notification/', views.clearNotification, name="clearNotification"),
]
