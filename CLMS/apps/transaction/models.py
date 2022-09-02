from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings

class Sched_Request(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="requester")
    course = models.CharField(_("course"), max_length=50)
    year_level = models.CharField(_("year_level"), max_length=50)
    section = models.CharField(_("section"), max_length=50)
    schedule_in = models.DateTimeField(auto_now=False, auto_now_add=False)
    schedule_out = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "requested by {0}".format(self.requester.username)

class Student(models.Model):
    sched = models.ForeignKey(Sched_Request, verbose_name=_("sched"), on_delete=models.CASCADE, related_name='sched')
    student_no = models.CharField(_("student_no"), max_length=50, null=True, blank=True)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    middle_name = models.CharField(_("middle_name"), max_length=50, null=True, blank=True)
    email = models.CharField(_("email"), max_length=50)
    contact = models.CharField(_("contact"), max_length=20)
    address = models.CharField(_("address"), max_length=100)

    def __str__(self):
        return self.student_no

class StudentListExcelFile(models.Model):
    students = models.FileField(_("students"), upload_to="student/excel")
