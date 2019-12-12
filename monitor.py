# encoding: utf-8
"""
Author: 沙振宇
CreateTime: 2019-7-9
UpdateTime: 2019-12-12
Info: 简单监控的CPU利用率、CPU平均负载、硬盘使用率、内存使用率 和 各个端口的开启状况
"""
import json
import socket
import os
import platform
import requests
import datetime
import time

# 打印间隔符
def printL():
	print("------------------------------")

# 判断系统是Windows还是Linux还是其它
sysstr = platform.system()
if(sysstr =="Windows"):
	print ("Windows tasks, no fcntl module")
	printL()
elif(sysstr == "Linux"):
	print ("Linux tasks")
	printL()
	# linux 模块
	import fcntl
else:
	print ("Other System tasks, no fcntl module")
	printL()

# @ class method 类方法（不需要实例化类就可以被类本身调用）
class Monitor():
	g_web_ip = ''		# 本机外网IP（这里之所以不自动获取是因为有些机器只有内网权限）
	g_wx_url = ''		# 读取微信地址
	g_wx_id = []		# 读取微信号
	g_email_url = ''   	# email地址
	g_email_id = []		# email账号
	g_php_url = ''		# php接口地址
	g_cpu_used = ''		# CPU利用率
	g_aver_load = ''	# CPU平均负载
	g_mem_used = ''		# 内存使用率
	g_disk_used = ''	# 磁盘使用率
	g_monitor_ports = []# 检测的端口们

	# 读取配置文件
	@classmethod
	def read_conf(cls):
		f_monitor = open('./monitor.conf','r',encoding='utf-8')
		f_monitor_lines = f_monitor.readlines()
		for f_line_num,f_monitor_line in enumerate(f_monitor_lines):
			tup = f_monitor_line.rstrip('\n').rstrip().split('\t')
			if '=' in tup[0]:	# 刨除异常状况
				# print("monitor.conf --- line:",f_line_num, tup[0])	# 读取每一行
				temp = tup[0].split('=')	# 读取每一项元素
				if temp[0] == 'web_ip': # 本机外网IP
					cls.g_web_ip = temp[1]
					print("read g_web_ip:", cls.g_web_ip)
				elif temp[0] == 'we_chat_url': # 读取微信地址
					cls.g_wx_url = temp[1]
					print("read g_wx_url:", cls.g_wx_url)
				elif temp[0] == 'wecaht_id': # 读取微信号
					wx_id = temp[1]
					cls.g_wx_id = wx_id.replace(' ','').split(',')
					print("read g_wx_id:", cls.g_wx_id)
				elif temp[0] == 'email_url': # email地址
					cls.g_email_url = temp[1]
					print("read g_email_url:", cls.g_email_url)
				elif temp[0] == 'email_id': # email账号
					email_id = temp[1]
					cls.g_email_id = email_id.replace(' ','').split(',')
					print("read email_id:", cls.g_email_id)
				elif temp[0] == 'php_url': # php接口地址
					cls.g_php_url = temp[1]
					print("read g_php_url:", cls.g_php_url)
				elif temp[0] == 'cpu_used': # CPU利用率
					cls.g_cpu_used = temp[1]
					print("read cpu_used:",cls.g_cpu_used)
				elif temp[0] == 'aver_load': # CPU平均负载
					cls.g_aver_load = temp[1]
					print("read aver_load:",cls.g_aver_load)
				elif temp[0] == 'mem_used': # 内存使用率
					cls.g_mem_used = temp[1]
					print("read mem_used:",cls.g_mem_used)
				elif temp[0] == 'disk_used': # 磁盘使用率
					cls.g_disk_used = temp[1]
					print("read disk_used:",cls.g_disk_used)
				elif temp[0] == 'monitor_ports': # 检测的端口们
					monitor_ports = temp[1]
					cls.g_monitor_ports = monitor_ports.replace(' ','').split(',')
					print("read monitor_ports:", cls.g_monitor_ports)
		printL()
		f_monitor.close()

	# 获取端口信息
	@classmethod
	def get_ports(cls, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex(('127.0.0.1',int(port)))
		if result != 0:
			send_data = cls.g_web_ip+"服务器的"+port+'端口挂了，快去修复哈'
			cls.send_msg(send_data)
		else:
			print("端口："+port+"正常")

	# CPU利用率
	@classmethod
	def get_cpu_used(cls):
		if (sysstr == "Linux"):
			f = os.popen("top -bi -n 1| awk '{print $4}'").read().split('\n')[2]
			float_cpu_used = float(f)
			float_g_cpu_used = float(cls.g_cpu_used.split("%")[0])
			print("CPU利用率:",f,"%")
			if float(float_cpu_used) > float(float_g_cpu_used):
				cls.send_msg(cls.g_web_ip+"服务器的CPU利用率超过"+cls.g_cpu_used+"了，快去看看咋回事！")
		else:
			print(sysstr + " CPU Adoption rate Cannot read.")
		printL()

	# CPU平均负载
	@classmethod
	def aver_load(cls):
		if (sysstr == "Linux"):
			f = os.popen("uptime | sed 's/,//g' | awk '{print $8,$9,$10}'")
			str_aver_load = f.read().strip().split(":")[1].strip()
			print("CPU平均负载:",str_aver_load)
			if float(str_aver_load) > float(cls.g_aver_load):
				cls.send_msg(cls.g_web_ip+"服务器的CPU平均负载超过"+cls.g_aver_load+"了，快去看看咋回事！")
		else:
			print(sysstr + " CPU Load average Cannot read.")
		printL()

	#获取硬盘使用率
	@classmethod
	def get_disk_used(cls):
		if (sysstr == "Linux"):
			disk_val = os.popen("df -h | head -2 | tail -1 |awk '{print $5}'").read().strip()
			int_disk_val = int(disk_val.split("%")[0])
			int_g_disk_val = int(cls.g_disk_used.split("%")[0])
			print("硬盘使用率:",disk_val)
			if int_disk_val > int_g_disk_val:
				cls.send_msg(cls.g_web_ip+"服务器的硬盘使用率超过"+cls.g_disk_used+"了，快去看看咋回事！")
		else:
			print(sysstr + " hard disk Cannot read.")
		printL()

	# 获取内存使用率
	@classmethod
	def get_mem_used(cls):
		if (sysstr == "Linux"):
			f = os.popen("free -m |grep Mem |awk '{print $3/$2}'")
			str_men = f.read().strip()
			print("内存使用率:",str_men)
			if float(str_men) > float(cls.g_mem_used):
				cls.send_msg(cls.g_web_ip+"服务器的内存使用率超过"+cls.g_mem_used+"了，快去看看咋回事！")
		else:
			print(sysstr + " RAM Cannot read.")
		printL()

	#调用报警函数
	@classmethod
	def send_msg(cls, content):
		cls.send_http(content)

	# 调用http接口
	@classmethod
	def send_http(cls,content):
		printL()
		print("send_http:",type(content),content)
		url_total = cls.g_php_url + "?msg=" + content
		print("url_total:",url_total)
		rp = requests.get(url_total)
		print("rp:",rp.text)
		printL()

	# 发微信预警消息
	@classmethod
	def send_wx_alarm(cls,content):
		post_url = cls.g_wx_url
		for id in cls.g_wx_id:
			try:
				post_data = '{"operSys":"MCS","content":"服务器监控告警：%s\n%s","phones":"%s"}'%(cls.g_web_ip, content, id)
				print(post_data)
				# data = urllib.parse.urlencode(post_data)
				# data = data.encode('utf-8')

				req = requests.get(url=post_url,data=post_data)
				print("send_wx_alarm req:",req,type(req))
				result = json.loads(req.text())
				print(result)
			except Exception as e:
				print("send_wx_alarm:",e)

	# 发邮件预警消息
	@classmethod
	def send_email_alarm(cls,content):
		post_url = cls.g_email_url
		for id in cls.g_email_id:
			try:
				post_data = '{"subject":"%s服务器监控告警","email":"%s","bccEmail":"","operSys":"LOG","content":"%s"}'%(cls.g_web_ip, id, content)
				print(post_data)
				# data = urllib.parse.urlencode(post_data)
				# data = data.encode('utf-8')

				req = requests.get(url=post_url,data=post_data)
				print("send_email_alarm req:",req,type(req))
				# req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
				result = json.loads(req.text())
				print(result)
			except Exception as e:
				print("send_email_alarm:",e)

# 定时检测
def fun_timer():
	print('当前检测时间为：',time.strftime('%Y-%m-%d %X',time.localtime()))
	printL()
	printL()
	print("当前时间：", datetime.datetime.now())
	printL()
	# 读取配置信息
	Monitor.read_conf()

	# CPU利用率
	Monitor.get_cpu_used()

	# 读CPU平均负载
	Monitor.aver_load()

	# 读硬盘使用率
	Monitor.get_disk_used()

	# 读内存使用率
	Monitor.get_mem_used()

	# 检测端口
	for port in Monitor.g_monitor_ports:
		Monitor.get_ports(port)

if __name__ == '__main__':
	# 检测时间间隔
	timer_interval = 300
	while True:
		print("检测时间间隔：%s秒"%timer_interval)
		fun_timer()
		time.sleep(timer_interval)# 等待300s钟调用一次fun_timer() 函数
