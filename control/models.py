from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    create_time = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)


class CIUser(models.Model):
    alias = models.CharField(max_length=50)
    userId = models.IntegerField()
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    commit = models.TextField()
    feedbackTime = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)


class Router(models.Model):
    CIUser_id = models.IntegerField()
    mac_address = models.CharField(max_length=80)
    ip1 = models.CharField(max_length = 80)
    ip2 = models.CharField(max_length = 80)
    ip3 = models.CharField(max_length = 80)
    port = models.IntegerField()
    key = models.CharField(max_length=150)
    method = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    update_time = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=0)
    commit = models.TextField()


class Command(models.Model):
    router_id = models.IntegerField()
    create_time = models.DateField(auto_now_add=True)
    cmd_type = models.CharField(max_length=50)
    params = models.TextField()
    result = models.CharField(max_length=50)
    Is_deleted = models.BooleanField(default=0)
    is_get = models.BooleanField(default=0) #weather the router get the order?
    is_return = models.BooleanField(default=0) #weather the router return the ans of the command executing?
