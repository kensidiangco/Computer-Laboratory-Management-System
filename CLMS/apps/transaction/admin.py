from django.contrib import admin
from .models import Student, Sched_Request, Approved_Schedule, Rejected_Schedule

admin.site.register(Student)
admin.site.register(Sched_Request)

admin.site.register(Approved_Schedule)
admin.site.register(Rejected_Schedule)