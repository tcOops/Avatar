function addData(){
	var checkboxs = $('.selectNode')
	var nodeIds = ""
	var flag = false
	for(var i = 0; i < checkboxs.length; ++i){
		if(checkboxs[i].checked){
			if(flag) nodeIds += ','
			else flag = true
			nodeIds += checkboxs[i].value.toString()
		}
	}
	$('#reserveData').val(nodeIds)
}

function choseAll(){
	var checkboxs = $('.selectNode')
	for(var i = 0; i < checkboxs.length; ++i){
		checkboxs[i].checked = true
	}
}

function choseReverse(){
	var checkboxs = $('.selectNode')
	for(var i = 0; i < checkboxs.length; ++i){
		checkboxs[i].checked ^= 1
	}
}

function showRouterCommit(content, routerId){
	var contents = ""
	while(content){
		contents += content.substr(0, 30) + '\n'
		content = content.substr(30);
	}
	$('#routerCommit').html(contents)
	$('#reserveRouterId').val(routerId)
}


function updateCommit(){
	routerId = 	$('#reserveRouterId').val()
	newCommit = $('#newCommits').val()
	url = "/route/updateRouterCommit/"
	data = new Object()
	data.routerId = routerId.toString()
	data.commit = newCommit
	$.ajax({
		type : 'post',
		dataType : 'json',
		url : url,
		async : true,
		data :  data,

		success : function(response){
			//Construct Data
			//console.log("ok")
			//constructNodeDetail(response[0])
		},

		error : function(response){
			console.log("Oops,  some errors !")
		}
	})
}


function getAns(ans){
	ans = ans.replace(/\n/ig,"</br>")
	$('#orderAns').html(ans)
}

//routerInfo表里面的各种status字段， 除了vpn_status 和 dns_status为单个json对象外， 其他均为json数组
function getRouterOrderStatus(routerId){
	url = "/route/getRouterOrderStatus/"
	data = new Object()
	data.routerId = routerId.toString()
	$.ajax({
		type : 'post',
		dataType : 'json',
		url : url,
		async : true,
		data :  data,

		success : function(response){
			//Construct Data
			//console.log("ok")
			//constructNodeDetail(response[0])
			b= response
			if(response.client_info != '--'){
				client_info = JSON.parse(response.client_info)
				var tmp = '<table style="border-width:0px;border-collapse:collapse;width:100%"><tr style="background-color:#E0E0E0;height:40px;border-width:0px"><td style="width:26%;border-width:0px;font-weight:bold;text-align:center">ip</td> <td style="width:44%;border-width:0px;font-weight:bold;text-align:center">mac</td>' 
				+ '<td style="width:30%;border-width:0px;font-weight:bold;text-align:center">iface</td></tr>'
				for(var i = 0; i < client_info.length; ++i){
					tmp += '<tr> <td style="width:26%;border-width:0px;text-align:center">' + client_info[i].ip + '</td>'
					tmp += '<td style="width:44%;border-width:0px;text-align:center">' + client_info[i].mac + '</td>'
					tmp += '<td style="width:30%;border-width:0px;text-align:center">' + client_info[i].iface + '</td> </tr>'
				}
				tmp += '</table>'
				client_info = tmp
			}
			else{
				client_info = '--'
			}
			
			if(response.interface_info != '--'){
				interface_info = JSON.parse(response.interface_info)
				var tmp = '<table style="border-width:0px;border-collapse:collapse;width:100%"><tr style="background-color:#E0E0E0;height:40px;border-width:0px"><td style="width:10%;border-width:0px;font-weight:bold;text-align:center">ip</td>' 
				+ '<td style="width:25%;border-width:0px;font-weight:bold;text-align:center">mac</td> <td style="width:20%;border-width:0px;font-weight:bold;text-align:center">mask</td>'
				+ '<td style="width:25%;border-width:0px;font-weight:bold;text-align:center">name</td> <td style="width:10%;border-width:0px;font-weight:bold;text-align:center">rx</td>'
				+ '<td style="width:10%;border-width:0px;font-weight:bold;text-align:center">tx</td></tr>'
				for(var i = 0; i < interface_info.length; ++i){
					tmp += '<tr> <td style="width:10%;border-width:0px;text-align:center">' + interface_info[i].ip + '</td>'
					tmp += '<td style="width:25%;border-width:0px;text-align:center">' + interface_info[i].mac + '</td>'
					tmp += '<td style="width:20%;border-width:0px;text-align:center">' + interface_info[i].mask + '</td>'
					tmp += '<td style="width:25%;border-width:0px;text-align:center">' + interface_info[i].name + '</td>'
					tmp += '<td style="width:10%;border-width:0px;text-align:center">' + interface_info[i].rx + '</td>'
					tmp += '<td style="width:10%;border-width:0px;text-align:center">' + interface_info[i].tx + '</td> </tr>'
				}
				tmp += '</table>'
				interface_info = tmp
			}
			else{
				interface_info = '--'
			}

			if(response.link_status != '--'){
				link_status = JSON.parse(response.link_status)
				var tmp = '<table style="border-width:0px;border-collapse:collapse;width:100%"><tr style="background-color:#E0E0E0;height:40px;border-width:0px"><td style="width:29%;border-width:0px;font-weight:bold;text-align:center">src</td> <td style="width:38%;border-width:0px;font-weight:bold;text-align:center">dst</td> ' 
				+ '<td style="width:35%;border-width:0px;font-weight:bold;text-align:center">type</td></tr>'
				for(var i = 0; i < link_status.length; ++i){
					tmp += '<tr> <td style="width:29%;border-width:0px;text-align:center">' + link_status[i].src + '</td>'
					tmp += '<td style="width:38%;border-width:0px;text-align:center">' + link_status[i].dst + '</td>'
					tmp += '<td style="width:35%;border-width:0px;text-align:center">' + link_status[i].type + '</td> </tr>'
				}
				tmp += '</table>'
				link_status = tmp
			}
			else{
				link_status = '--'
			}

			if(response.dns_status != '--'){
				var tmp = ''
				dns_status = JSON.parse(response.dns_status)
				tmp += dns_status.status	
				dns_status = tmp
			}
			else{
				dns_status = '--'
			}

			if(response.route_status != '--'){
				route_status = JSON.parse(response.route_status)
				var tmp = '<table style="border-width:0px;border-collapse:collapse;width:100%"><tr style="background-color:#E0E0E0;height:40px;border-width:0px"><td style="width:25%;border-width:0px;font-weight:bold;text-align:center">目的IP</td> <td style="width:25%;border-width:0px;font-weight:bold;text-align:center">网关</td>' 
				+ '<td style="width:25%;border-width:0px;font-weight:bold;text-align:center">子网掩码</td> <td style="width:25%;border-width:0px;font-weight:bold;text-align:center">iface</td></tr>'
				for(var i = 0; i < route_status.length; ++i){
					tmp += '<tr> <td style="width:25%;border-width:0px;text-align:center">' + route_status[i].dst + '</td>'
					tmp += '<td style="width:25%;border-width:0px;text-align:center">' + route_status[i].gw + '</td>'
					tmp += '<td style="width:25%;border-width:0px;text-align:center">' + route_status[i].mask + '</td>'
					tmp += '<td style="width:25%;border-width:0px;text-align:center">' + route_status[i].iface + '</td></tr>'

				}
				tmp += '</table>'
				route_status = tmp
			}	
			else{
				route_status = '--'
			}

			if(response.vpn_status != '--'){
				vpn_status = JSON.parse(response.vpn_status)
				var tmp = ''
				tmp += vpn_status.status
				vpn_status = tmp
			}
			else{
				vpn_status = '--'
			}

			if(response.raw_command != '--'){
				raw_command = JSON.parse(response.raw_command)
				var tmp = '<table style="border-width:0px;border-collapse:collapse;width:100%"><tr style="background-color:#E0E0E0;height:40px;border-width:0px"><td style="padding-left:20px">'
				tmp += raw_command[0].cmd_result + '</td></tr></table>'
				raw_command = tmp
			}
			else{
				raw_command = '--'
			}

			var content = '<span style="margin-left:40%;font-weight:bold;">' + "客户端连接信息: " + '</span>' + client_info + "</br></br>"
			content += '<span style="margin-left:43%;font-weight:bold;">' + "接口信息: " + '</span>' + interface_info + '</br></br>'
			content += '<span style="margin-left:43%;font-weight:bold;">' + "连接状态: " + '</span>' + link_status + '</br></br>'
			if(dns_status == "ON"){
				dns_status = '<span style="color:green">' + dns_status + '</span>'
			}
			else if(dns_status == 'OFF'){
				dns_status = '<span style="color:red">' + dns_status + '</span>'
			}
			content += '<span style="margin-left:43%;font-weight:bold;">' + "dns状态: " + '</span>' + dns_status + '</br></br>'
			content += '<span style="margin-left:44%;font-weight:bold;">' + "路由表: " + '</span>' + route_status + '</br></br>'
			if(vpn_status == 'ON'){
				vpn_status = '<span style="color:green">' + vpn_status + '</span>'
			}
			else if(vpn_status == 'OFF'){
				vpn_status = '<span style="color:red">' + vpn_status + '</span>'
			}
			content += '<span style="margin-left:43%;font-weight:bold;">' + "vpn状态: " + '</span>' + vpn_status + '</br></br>'
			raw_command = raw_command.replace(/\n/ig,"</br>");
			content += '<span style="margin-left:43%;font-weight:bold;">' + "命令执行: " + '</span>' + raw_command + '</br></br>' 
			$("#orderStatus").html(content)
		},

		error : function(response){
			console.log("Oops,  some errors !")
		}
	})	
}


function showCIUser(userId){
	url = "/route/getCIUserById/"
	data = new Object()
	data.userId = userId.toString()
	$.ajax({
		type : 'post',
		dataType : 'json',
		url : url,
		async : true,
		data :  data,

		success : function(response){
			//Construct Data
			var content = '姓名  :   ' + response[1].name + '</br>'
			content += '备注  :   ' + response[1].commit + '</br>'
			content += '创建时间  :   ' + response[1].create_time
			$('#CIUserDesc').html(content)
		},

		error : function(response){
			console.log("Oops,  some errors !")
		}
	})
}

function showParamsBox(){
	orderType = $('#ordertype').val()
	var content = '';
	if(orderType == 'GET_CLIENTS_INFO'){

	}
	if(orderType == 'GET_LINK_STATUS'){

	}
	if(orderType == 'GET_INTERFACES_INFO'){

	}
	if(orderType == 'RAW_COMMAND'){
		content = '命令内容 : ' + '<input style="margin-left:23px" type="text" id = "r_c_content" name = "r_c_content"/>'
	}
	if(orderType == 'GET_ROUTE_STATUS'){

	}
	if(orderType == 'START_DNS_HIJACK'){
		content = 'IP : ' + '<input style="margin-left:64px" type="text" id = "s_d_h_ip"  name = "s_d_h_ip"/> </br></br>'
		content += '端口号 : ' + '<input style="margin-left:34px" type="text" id = "s_d_h_port" name = "s_d_h_port"/> </br>'
	}
	if(orderType == 'STOP_DNS_HIJACK'){

	}
	if(orderType == 'GET_DNS_STATUS'){
		
	}
	if(orderType == 'START_VPN'){
		content = 'IP : ' + '<input style="margin-left:66px" type="text" id = "s_v_ip" name = "s_v_ip"/> </br></br>'
		content += '用户名 : ' + '<input style="margin-left:36px" type="text" id = "s_v_name" name = "s_v_name"/> </br></br>'
		content += '密码 : ' + '<input style="margin-left:50px" type="password" id = "s_v_pwd" name = "s_v_pwd"/> </br></br>'
	}
	if(orderType == 'STOP_VPN'){

	}
	if(orderType == 'GET_VPN_STATUS'){

	}
	if(orderType == 'ADD_ROUTE'){
		content = '目的IP : ' + '<input style="margin-left:38px" type="text" id = "a_r_ip" name = "a_r_ip"/> </br></br>'
		content += '子网掩码 : ' + '<input style="margin-left:22px" type="text" id = "a_r_mask" name = "a_r_mask"/> </br></br>'
		content += '网关 : ' + '<input style="margin-left:50px" type="text" id = "a_r_gateway" name = "a_r_gateway"/> </br>'
	}
	if(orderType == 'DEL_ROUTE'){

	}
	$('#params').html(content)
}