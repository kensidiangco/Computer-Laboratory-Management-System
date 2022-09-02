from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_deptHeadAccount = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

class Course(models.Model):
    course_name = models.CharField(max_length=50)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    student_no = models.CharField(max_length=50, blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professor')
    professor_no = models.CharField(max_length=50, blank=False, null=False)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class ITDept(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ITDept')
    employee_no = models.CharField(max_length=50, blank=False, null=False)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Theme(models.Model):
    user = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username