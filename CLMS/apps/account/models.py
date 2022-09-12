from operator import mod
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    position = models.CharField(_("position"), max_length=50, default="")
    id_number = models.CharField(_("id_number"), max_length=50)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    middle_name = models.CharField(_("middle_name"), max_length=50)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
class Theme(models.Model):
    user = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username