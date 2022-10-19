from django.contrib import admin
from .models import Computer_Lab, Student, Sched_Request, Approved_Schedule, Rejected_Schedule, Sched_Time_Usage

admin.site.register(Student)
admin.site.register(Sched_Request)

admin.site.register(Sched_Time_Usage)
admin.site.register(Approved_Schedule)
admin.site.register(Rejected_Schedule)
admin.site.register(Computer_Lab)