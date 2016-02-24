#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext , Context
from django.views.decorators.csrf import *
import MySQLdb
from control.models import *
import time, subprocess, datetime
from django.core import serializers #serualizer
from django.contrib.auth import authenticate, login #用django的auth做验证
import hashlib, json

db_host = 'localhost'
db_user = 'root'
db_pwd = 'ROOT'
db_name = 'control'
db_charset = 'utf-8'


@csrf_exempt
def login(request):
	if request.method == 'GET':
		return render_to_response('login.html')
	elif request.method == 'POST':
		userName = request.POST.get('username', '')
		password = request.POST.get('password', '')
		userGet = authenticate(username=userName, password=password)
		if userGet:
			if 'username' in request.session:
				del request.session['username']
			request.session['username'] = userName
			request.session['userid'] = userGet.id
			return HttpResponseRedirect('/route/index/')
		else:
			return HttpResponseRedirect('/route/login')


@csrf_exempt
def logout(request):
	del request.session['username']  #delete session
	del request.session['userid']
   	return HttpResponseRedirect('/route/login')


# Get List of 反馈者
def index(request):
	userName = request.session.get('username', '')
	userId = request.session.get('userid')
	if not userName:
		return HttpResponseRedirect('/route/login')
	else:
		params = {}
		params['username'] = userName

	p = CI_user.objects.filter(userId=userId, is_deleted=0)
	#for node in p:
		#node.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(node.timestamp))
	params["users"] = p
	params["userCnt"] = len(p)
	return render_to_response("index.html",  params, context_instance=RequestContext(request))


@csrf_exempt
def getCIUserById(request):
	CIUserId = request.POST.get('userId', '')
	print CIUserId
	try:
		p = CI_user.objects.get(id = CIUserId)
	except Exception, e:
		print e
		ret = "[{'status':'error'}]"
	else:
		ret = '[{"status":"ok"},{"name":"' + p.name + '","commit":"' + p.commit + '","create_time":"' + p.last_time + '"}]'

	response = HttpResponse()
	response['Content-Type'] = 'text/javascript'
	response.write(ret)
	return response


# ADD 反馈者
@csrf_exempt
def addUser(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')

	userName = request.POST.get('username', '')
	remark = request.POST.get('remark', '')
	pwd = request.POST.get('pwd')
	alias = hashlib.md5(userName).hexdigest()
	userId = int(request.session.get('userid'))
	p = CI_user(
		name = userName,
		password = pwd,
		userId = userId,
		commit = remark,
		alias = alias,
		last_time = str(datetime.datetime.now()).split('.')[0],
		is_deleted = 0,
	)
	p.save()
	return HttpResponseRedirect('/route/index/')


# ADD 反馈者
@csrf_exempt
def deleteUser(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')

	userId = request.POST.get('userId')
	print userId

	p = CI_user.objects.get(id = userId)
	if p:
		p.is_deleted = 1
		p.save()
	return HttpResponseRedirect('/route/index/')


# Get List of routers
def router(request):
	userName = request.session.get('username', '')
	userId = request.session.get('userid')
	if not userName:
		return HttpResponseRedirect('/route/login')
	else:
		params = {}
		params['username'] = userName

	p = RouterInfo.objects.filter(is_deleted=0)
	routers = []
	for each in p:
		CI_id = each.CI_id
		q = CI_user.objects.get(id = CI_id)
		if q.userId == userId:
			each.client_info = q.name
			routers.append(each)
	#for node in p:
		#node.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(node.timestamp))
	params["routers"] = routers

	params["routerCnt"] = len(routers)
	#c =Context(dict)
	return render_to_response("router.html",  params, context_instance=RequestContext(request))


@csrf_exempt
def updateRouterCommit(request):
	routerId = request.POST.get("routerId", "")
	commit = request.POST.get("commit", '')
	print routerId, commit
	if routerId:
		routerId = int(routerId)
	try:
		p = RouterInfo.objects.get(id = routerId)
		p.commit = commit
		p.save()
	except Exception, ex:
		print ex
		return '{"status":"error"}'
	else:
		response = HttpResponse()
		response['Content-Type'] = 'text/javascript'
		response.write('{"status":"ok"}')
		return response


@csrf_exempt
def getRouterOrderStatus(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')

	routerId = request.POST.get('routerId')
	p = RouterInfo.objects.get(id = routerId)
	data = {"link_status":p.link_status, "client_info":p.client_info, "interface_info":p.interface_info, "route_status":p.route_status,
	"dns_status":p.dns_status, "vpn_status":p.vpn_status, "raw_command":p.raw_command}
	
	response = HttpResponse()
	response['Content_Type'] = 'text/javascript'
	response.write(json.dumps(data))
	return response # return results' json	


#Get router connect info
def routerConnect(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')
	else:
		params = {}
		params['username'] = userName

	p = Routers.objects.filter(is_deleted=0).order_by('-id')
	for each in p:
		CI_id = each.CI_id
		q = CI_user.objects.get(id = CI_id)
		each.status = q.name
	#for node in p:
		#node.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(node.timestamp))
	params["routerConnects"] = p
	params["routerConnectCnt"] = len(p)
	#c =Context(dict)
	return render_to_response("routeConnect.html",  params, context_instance=RequestContext(request))


@csrf_exempt
def deleteRouter(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')
	else:
		params = {}
		params['username'] = userName


	routerId = request.POST.get('routerId')
	routerMAC = request.POST.get('routerMAC')
	p = Routers.objects.get(id=routerId)
	if p:
		p.is_deleted = 1
		p.save()

		q = RouterInfo.objects.get(MAC=routerMAC)
		if q:
			q.is_deleted = 1
			q.save()
	return HttpResponseRedirect('/route/routerconnect/')


def order(request):
	userName = request.session.get('username', '')
	userId = request.session.get('userid')
	if not userName:
		return HttpResponseRedirect('/route/login')
	else:
		params = {}
		params['username'] = userName

	p = Command.objects.filter(is_get = 0, is_deleted = 0).order_by('-id')
	orders = []
	for each in p:
		CI_id = each.CI_id
		q = CI_user.objects.get(id=CI_id)
		if q.userId == userId:
			each.ret_ans = each.ret_ans[1:-1]
			orders.append(each)

	params["orders"] = orders
	params["orderCnt"] = len(orders)
	#c =Context(dict)
	return render_to_response("order.html",  params, context_instance=RequestContext(request))


@csrf_exempt
def addOrders(request):
	userName = request.session.get('username', '')
	if not userName:
		return HttpResponseRedirect('/route/login')

	routerIds = request.POST.get('routerIds', '')
	orderType = request.POST.get('ordertype', '')
	#params = request.POST.get('params', '')
	if orderType == 'GET_CLIENTS_INFO':
		params = '{}'
	
	if orderType == 'GET_LINK_STATUS':
		params = '{}'
	
	if orderType == 'GET_INTERFACES_INFO':
		params = '{}'
	
	if orderType == 'RAW_COMMAND':
		cmd = request.POST.get('r_c_content')
		params = '{"cmd":"%s"}'%(cmd)

	if orderType == 'GET_ROUTE_STATUS':
		params = '{}'
	
	if orderType == 'START_DNS_HIJACK':
		dns_ip = request.POST.get("s_d_h_ip")
		dns_port = request.POST.get("s_d_h_port")
		params = '{"dns_ip":"%s", "dns_port":"%s"}'%(dns_ip, dns_port)

	if orderType == 'STOP_DNS_HIJACK':
		params = '{}'
	
	if orderType == 'GET_DNS_STATUS':
		params = '{}'
	
	if orderType == 'START_VPN':
		ip = request.POST.get("s_v_ip")
		name = request.POST.get("s_v_name")
		pwd = request.POST.get("s_v_pwd")
		params = '{"server_ip":"%s", "user":"%s", "password":"%s"}'%(ip, name, pwd)

	if orderType == 'STOP_VPN':
		params = '{}'

	if orderType == 'GET_VPN_STATUS':
		params = '{}'
	
	if orderType == 'ADD_ROUTE': 
		ip = request.POST.get("a_r_ip")
		mask = request.POST.get("a_r_mask")
		gateway = request.POST.get("a_r_gateway")
		params = '{"dst":"%s", "mask":"%s", "gw":"%s"}'%(ip, mask, gateway)

	if orderType == 'DEL_ROUTE':
		params = '{}'

	if routerIds: routerIdList = routerIds.split(",")
	else:  routerIdList = []
	for routerId in routerIdList:
		q = RouterInfo.objects.filter(id = routerId, is_deleted=0)
		CI_id = q[0].CI_id
		p = Command(
			CI_id = CI_id,
			rt_id = routerId,
			date = str(datetime.datetime.now()).split('.')[0],
			type = orderType,
			params = params,
			is_deleted = 0,
			is_get = 0,
			is_ret = 0
		)
		p.save()
	return HttpResponseRedirect('/route/router/')

def sync(request):
	return render_to_response("sync.html" )


###############################
#         RESTFUL API         #
###############################
@csrf_exempt
def CI_login(request):
	data = json.loads(request.body)
	name = data["name"]
	pwd = data["p"]
	p = CI_user.objects.filter(name=name, password=pwd, is_deleted=0)
	#p is [] "not []" = True

	if len(p) == 0:
		data = {'status':'404'}
	else:
		data = {'status':'ok', 'alias':p[0].alias}
	response = HttpResponse()
	response['Content_Type'] = 'text/javascript'
	response.write(json.dumps(data))
	return response # return results' json


@csrf_exempt
def CI_post(request, alias):
	datas = json.loads(request.body)
	CI_id = CI_user.objects.filter(alias=alias)[0].id
	print datas
	for data in datas:
		MAC = data['mac']
		ips = data['ips']
		port = data['port']
		keyword = data['key']
		method = data['method']
		model = data['model']
		status = data['status']
		ips = ips.strip().split(';') #获取IP地址
		ip1, ip2, ip3 = '', '', ''
		date = data['date']
		if len(ips) >= 1:
			ip1 = ips[0]
		if len(ips) >= 2:
			ip2 = ips[1]
		if len(ips) >= 3:
			ip3 = ips[2]
		print ip1, ip2, ip3

		try:
			q = Routers.objects.filter(MAC = MAC, is_deleted=0)
			if q:
				p = q[0]
				p.ip1 = ip1,
				p.ip2 = ip2,
				p.ip3 = ip3,
				p.port = port,
				p.keywords = keyword,
				p.method = method,
				p.model = model,
				p.status = status,
				p.action_time = date
				p.save()

			else:
				p = Routers(
					CI_id = CI_id,
					MAC = MAC,
					ip1 = ip1,
					ip2 = ip2,
					ip3 = ip3,
					port = port,
					keywords = keyword,
					method = method,
					model = model,
					status = status,
					action_time = date
				)
				p.save()

			q = RouterInfo.objects.filter(MAC=MAC, is_deleted=0)
			if not q:
				p = RouterInfo(
					CI_id = CI_id,
					MAC = MAC,
					last_time = str(datetime.datetime.now()).split('.')[0],
					is_deleted = 0
				)
				p.save()
			else:
				q = q[0]
			   	q.last_time = date
				q.save()
		except Exception, e:
			print e
			data = {'status':'error'}

	data = {'status':'ok'}
	response = HttpResponse()
	response['Content_Type'] = 'text/javascript'
	response.write(json.dumps(data))
	return response


@csrf_exempt 
def CI_getOrder(request, token):
	if token == '123456':
		db = MySQLdb.connect(db_host, db_user, db_pwd, db_name)
		p = Command.objects.filter(is_get = 0, is_deleted=0)
		param = {"num":len(p)}
		cmds = []
		for each in p:
			rt_id = each.rt_id
			q = RouterInfo.objects.get(id=rt_id)
			r = Routers.objects.get(MAC=q.MAC)

			commandType, commandParams = each.type, each.params
			vpn_status = q.vpn_status
			dns_status = q.dns_status
			commandParams = json.loads(commandParams)
			if commandType == 'GET_DNS_STATUS':
				commandParams = {"status_string":json.loads(dns_status)['status_string']}
			if commandType == 'STOP_DNS_HIJACK':
				commandParams = {"stop_string":json.loads(dns_status)['stop_string']}
			if commandType == 'GET_VPN_STATUS':
				commandParams = {"status_string":json.loads(vpn_status)['status_string']}
			if commandType == 'STOP_VPN_HIJACK':
				commandParams = {"status_string":json.loads(vpn_status)['status_string']}

			ip1, ip2, ip3 = r.ip1, r.ip2, r.ip3
			ip = ip1 + ',' + ip2 + ',' + ip3
			cmds.append({"uuid":rt_id, "id":each.id, "func":each.type, "params":commandParams, "ip":ip, "port":r.port, "enc":r.method, "key":r.keywords})
		
			#sql = 'update control_command set is_get = 1 where id = {0}'.format(each.id)
			#print sql
			#cursor = db.cursor()
			#cursor.execute(sql)
			#db.commit()

		param["cmd"] = cmds
		data = json.dumps(param)
		response = HttpResponse()
		response['Content_Type'] = 'text/javascript'
		response.write(data)
		return response

	p = CI_user.objects.filter(alias = token, is_deleted = 0)
	ci_id = p[0].id
	sql = '''select w.id, w.type, w.params, w.rt_id, r.dns_status, r.vpn_status from control_command w inner join control_RouterInfo r where w.ci_id = %s and w.rt_id = r.id and w.is_ret = 0
	and w.is_deleted = 0'''%(ci_id)

	print sql
	db = MySQLdb.connect(db_host, db_user, db_pwd, db_name)
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()
	print data
	param = {"num":len(data)}
	cmds = []
	for each in data:
		if not each: break
		commandId, commandType, commandParams, routerId, dns_status, vpn_status = each
		commandParams = json.loads(commandParams)
		if commandType == 'GET_DNS_STATUS':
			commandParams = {"status_string":json.loads(dns_status)['status_string']}
		if commandType == 'STOP_DNS_HIJACK':
			commandParams = {"stop_string":json.loads(dns_status)['stop_string']}
		if commandType == 'GET_VPN_STATUS':
			commandParams = {"status_string":json.loads(vpn_status)['status_string']}
		if commandType == 'STOP_VPN_HIJACK':
			commandParams = {"status_string":json.loads(vpn_status)['status_string']}

		sql = 'select q.ip1, q.ip2, q.ip3, q.port, q.keywords, q.method from control_RouterInfo w inner join control_routers q where w.id = {0} and w.mac = q.mac'.format(routerId)
		cursor = db.cursor()
		cursor.execute(sql)
		data_ = cursor.fetchone()
		ip1, ip2, ip3, port, keywords, method = data_
		ip = ip1 + ',' + ip2 + ',' + ip3
		cmds.append({"uuid":routerId, "id":commandId, "func":commandType, "params":commandParams, "ip":ip, "port":port, "enc":method, "key":keywords})		
		sql = 'update control_command set is_get = 1 where id = {0}'.format(commandId)
		print sql
		cursor.execute(sql)
		db.commit()

	param["cmd"] = cmds
	data = json.dumps(param)
	response = HttpResponse()
	response['Content_Type'] = 'text/javascript'
	response.write(data)
	return response


@csrf_exempt
def CI_orderResult(request, token):
	datas = json.loads(request.body)
	orderId = datas['id']
	data = json.dumps(datas['return'])
	statusCode = datas['code']	
	p = Command.objects.get(id = orderId)
	orderType, routerId = p.type, p.rt_id
	p.ret_ans = data
	p.is_ret = 1

	router = RouterInfo.objects.get(id = routerId)
	####judge oreder type
	if orderType == 'GET_CLIENTS_INFO':
		if statusCode == 1:
			router.client_info = '--'
		else:
			router.client_info = data

	if orderType == 'GET_LINK_STATUS':
		if statusCode == 1:
			router.link_status = '--'
		else:
			router.link_status = data

	if orderType == 'GET_INTERFACES_INFO':
		if statusCode == 1:
			router.interface_info = '--'
		else:
			router.interface_info = data

	if orderType == 'RAW_COMMAND':
		if statusCode == 1:
			router.raw_command = '--'
		else:
			router.raw_command = data

	if orderType == 'GET_ROUTE_STATUS':
		if statusCode == 1:
			router.route_status = '--'
		else:
			router.route_status = data
	
	if orderType == 'START_DNS_HIJACK':
		if statusCode == 1:
			dns_status = json.loads(router.dns_status)
			dns_status['status'] = 'OFF'
			router.dns_status = json.dumps(dns_status)
		else:		
			dns_status = datas['return'][0]
			dns_status['status'] = 'ON'
			router.dns_status = json.dumps(dns_status)

	if orderType == 'GET_DNS_STATUS':
		if statusCode == 1:
			dns_status = json.loads(router.dns_status)
			dns_status['status'] = 'UNKNOWN'
			router.dns_status = json.dumps(dns_status)
		else:
			dns_status = json.loads(router.dns_status)
			dns_status['status'] = 'ON'
			router.dns_status = json.dumps(dns_status)

	if orderType == 'STOP_DNS_HIJACK':
		if statusCode == 1:
			dns_status = json.loads(router.dns_status)
			dns_status['status'] = 'UNKNOWN'
			router.dns_status = json.dumps(dns_status)
		else:	
			dns_status = json.loads(router.dns_status)
			dns_status['status'] = 'OFF'
			router.dns_status = json.dumps(dns_status)

	if orderType == 'START_VPN':
		if statusCode == 1:
			vpn_status = json.loads(router.vpn_status)
			vpn_status['status'] = 'OFF'
			router.vpn_status = json.dumps(vpn_status)
		else:
			vpn_status = datas['return'][0]
			vpn_status['status'] = 'ON'
			router.vpn_status = json.dumps(vpn_status)

	if orderType == 'STOP_VPN':
		if statusCode == 1:
			vpn_status = json.loads(router.vpn_status)
			vpn['status'] = 'UNKNOWN'
			router.vpn_status = json.dumps(vpn_status)
		else:
			vpn_status = json.loads(router.vpn_status)
			vpn_status['status'] = 'OFF'
			router.vpn_status = json.dumps(vpn_status)

	if orderType == 'GET_VPN_STATUS':
		if statusCode == 1:
			vpn_status = json.loads(router.vpn_status)
			vpn['status'] = 'UNKNOWN'
			router.vpn_status = json.dumps(vpn_status)

		else:
			vpn_status = json.loads(router.vpn_status)
			vpn['status'] = 'OFF'
			router.vpn_status = json.dumps(vpn_status)

	p.save()
	router.save()

	data = {"status":"ok"}
	response = HttpResponse()
	response['Content_Type'] = 'text/javascript'
	response.write(json.dumps(data))
	return response

