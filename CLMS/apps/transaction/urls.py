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

    path('user/requests/', views.Prof_Pending_Schedule, name="Prof_Pending_Schedule"),
    path('user/approved/', views.Prof_Approved_Schedule, name="Prof_Approved_Schedule"),
    path('user/rejected/', views.Prof_Rejected_Schedule, name="Prof_Rejected_Schedule"),
    path('user/ongoing/', views.Prof_Ongoing_Schedule, name="Prof_Ongoing_Schedule"),
    path('user/done/', views.Prof_Done_Schedule, name="Prof_Done_Schedule"),

    path('api/notifs/', views.getNotifs, name="getNotifs"),
    path('clear-notification/', views.clearNotification, name="clearNotification"),

    path('data/export', views.exportData, name="exportData"),
    path('data/pdf/', views.ViewPDF.as_view(), name="ViewPDF"),

]
