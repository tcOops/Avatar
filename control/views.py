#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext , Context
from django.views.decorators.csrf import *
import MySQLdb
from control.models import *
import time, subprocess
from django.core import serializers #serualizer
import os, json
cur_dir = os.getcwd()
file_path = cur_dir + "/files/upload/"


#The index page, which gets the list of nodes
def index(request):
	p = CIUser.objects.filter(is_deleted=0).order_by('-id')

	d = {"nodes": p, "nodeCnt": len(p)}
	return render_to_response("index.html", d, context_instance=RequestContext(request))
