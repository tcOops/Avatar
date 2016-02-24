from django.db import models

# Create your models here.
class CI_user(models.Model):
	alias = models.CharField(max_length=128)
	userId = models.IntegerField()
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	commit = models.CharField(max_length=200, default='--')
	last_time = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)


# reserve the connection data
class Routers(models.Model):
	CI_id = models.IntegerField()
	MAC = models.CharField(max_length=60)
	ip1 = models.CharField(max_length=50, default='--')
	ip2 = models.CharField(max_length=50, default='--')
	ip3 = models.CharField(max_length=50, default='--')
	port = models.IntegerField()
	keywords = models.CharField(max_length=50)
	method = models.CharField(max_length=50)
	model = models.CharField(max_length=100)
	status = models.CharField(max_length=50)
	action_time = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)


# reserve the route info
class RouterInfo(models.Model):
	CI_id = models.IntegerField()
	MAC = models.CharField(max_length=60)
	commit = models.CharField(max_length=200, default='--')
	last_time = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	client_info = models.TextField(default='--')
	link_status = models.TextField(default='--')
	interface_info = models.TextField(default='--')
	route_status = models.TextField(default='--')
	dns_status = models.TextField(max_length=200, default='--')
	vpn_status = models.TextField(max_length=100, default='--')
	raw_command = models.TextField(default='--')


class Command(models.Model):
	CI_id = models.IntegerField()
	rt_id = models.IntegerField()
	date = models.CharField(max_length=50)
	type = models.CharField(max_length=50)
	params = models.CharField(max_length=500)
	is_deleted = models.BooleanField(default=False)
	is_get = models.BooleanField(default=False)
	is_ret = models.BooleanField(default=False)
	ret_ans = models.TextField(default='--')


class Command_tpl(models.Model):
	type = models.CharField(max_length=100)
	params = models.CharField(max_length=500)
	is_deleted = models.BooleanField(default=False)
