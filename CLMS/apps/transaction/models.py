from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings

class Sched_Request(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="requester")
    course = models.CharField(_("course"), max_length=50)
    year_level = models.CharField(_("year_level"), max_length=50)
    section = models.CharField(_("section"), max_length=50)
    class_list = models.FileField(_("students"), upload_to="student/excel")
    date_request = models.DateField(auto_now=False, auto_now_add=False)
    time_in = models.TimeField(auto_now=False, auto_now_add=False)
    time_out = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(_("status"), max_length=50, default="Pending")
    notif_status = models.CharField(_("notif_status"), max_length=50, default="unread")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return "Requested by {0}".format(self.requester.username)

class Student(models.Model):
    sched = models.ForeignKey(Sched_Request, on_delete=models.CASCADE)
    student_no = models.CharField(_("student_no"), max_length=50)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    middle_name = models.CharField(_("middle_name"), max_length=50)
    email = models.CharField(_("email"), max_length=50)
    contact = models.CharField(_("contact"), max_length=20)
    address = models.CharField(_("address"), max_length=100)

    def __str__(self):
        return "Student ID: {0}".format(self.student_no)

class Approved_Schedule(models.Model):
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sched = models.OneToOneField(Sched_Request, verbose_name=_("sched"), on_delete=models.CASCADE)
    date_approved = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_approved',)

class Rejected_Schedule(models.Model):
    rejected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sched = models.OneToOneField(Sched_Request, verbose_name=_("sched"), on_delete=models.CASCADE)
    description = models.CharField(_("description"), max_length=100, null=True, blank=True)
    date_approved = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_approved',)

class Sched_Time_Usage(models.Model):
    sched = models.OneToOneField(Approved_Schedule, verbose_name=_("sched"), on_delete=models.CASCADE)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)
