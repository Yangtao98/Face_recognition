from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib import messages
from django.urls import reverse
from ..models import Employee,Role,WorkSchedule
from apscheduler.schedulers.blocking import BlockingScheduler
from django.db.models import Q
# pip install schedule
from datetime import date,datetime, timedelta
import random
import string
import hashlib
import os



def CheckMark():
	UserStatus = WorkSchedule.objects.filter(StartDate__lt=currentDate)
	for i in UserStatus:
		WorksId = WorkSchedule.objects.get(WorkSchedule_id=i.WorkSchedule_id)
		if WorksId.Mark != 'Off' and WorksId.Mark != 'MC':
			if WorksId.InTime is None and WorksId.StartTime is not None or WorksId.OutTime is None and WorksId.EndTime is not None:
				WorksId.Mark = 'Absent'
				WorksId.save()
			elif WorksId.InTime is not None and WorksId.StartTime is not None or WorksId.OutTime is not None and WorksId.EndTime is not None:
				if WorksId.StartTime >= WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
					WorksId.Mark = 'Present'
					WorksId.save()
				elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
					WorksId.Mark = 'Late & leave early'
					WorksId.save()
				elif WorksId.StartTime >= WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
					WorksId.Mark = 'Leave early'
					WorksId.save()
				elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
					WorksId.Mark = 'Late'
					WorksId.save()
	current = WorkSchedule.objects.filter(StartDate=currentDate)

	for k in current:
		userid = WorkSchedule.objects.get(WorkSchedule_id=k.WorkSchedule_id)
		if userid.Mark != 'Off' and userid.Mark != 'MC':
			if userid.InTime is not None and userid.OutTime is not None:
				if userid.StartTime < userid.InTime and userid.EndTime > userid.OutTime:
					userid.Mark = 'Late & leave early'
					userid.save()
				elif userid.StartTime >= userid.InTime and userid.EndTime <= userid.OutTime:
					userid.Mark = 'Present'
					userid.save()
				elif userid.StartTime >= userid.InTime and userid.EndTime > userid.OutTime:
					userid.Mark = 'Leave early'
					userid.save()
				elif userid.StartTime < userid.InTime and userid.EndTime <= userid.OutTime:
					userid.Mark = 'Late'
					userid.save()



def get_MD5(Password):
	md5 = hashlib.md5()
	md5.update(Password.encode('utf-8'))
	return md5.hexdigest()

currentDate = datetime.now().strftime("%Y-%m-%d")
currentTime =  datetime.now().strftime('%H:%M:%S')



def index_home(request):
	return render(request, 'index/index.html')

def Check_In(request):
	return render(request, 'index/camera.html')

# def UpdateAttendance():
# 		WorkTime = WorkSchedule.objects.filter(StartDate=currentDate)
# 		print(WorkTime)
# 		for i in WorkTime:
# 			E=Employee.objects.all().exclude(Employee_ID=i.Employee_id)
# 			if currentTime >= '00:00:00':
# 			# 可运行的代码
#
# 				WordSche = WorkSchedule(StartDate=currentDate, StartTime=None, EndTime=None, Employee_id=E,
# 										Mark='pending')
# 				WordSche.save()

	# if currentTime >'12:00:00':

def index_login(request):
	#if request.POST:
	Title='Login Page'
	CheckMark()
	if request.method == 'POST':
		try:
			# EmployeeID = request.POST.get('EmployeeID')
			user_login = Employee.objects.get(Employee_ID=request.POST['EmployeeID'])
			password = request.POST.get('password')+user_login.salt

			# user authentication, might move this function to another place if needed

			if user_login.Password == get_MD5(password):
				userObject = Employee.objects.get(Employee_ID=user_login.Employee_ID)
				request.session['Employee_ID'] = user_login.Employee_ID

				# if user == Sys_Admin
				if userObject.Role.Role_ID == 1:
					return redirect('sys_admin_home')
				elif userObject.Role.Role_ID == 2:
					return redirect('HR_home')
				else:
					return redirect('Home')

			else:
				messages.error(request, 'Invalid Username or Password')
				return redirect('login')

		except Exception as err:
			print(err)
			context = {"info": "account is not exist "}
			messages.error(request, 'Invalid Username')
			return redirect('login')
	else:
		context={
			'title': Title,
		}
		return render(request, 'index/login.html',context)


def DeletedButton(request, Editempid):
	# Emp = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
	#
	currentEmployee = Employee.objects.get(Employee_ID=Editempid)

	DEFAULT = 'profile_pics/default.jpg'

	if currentEmployee.Profile_Image != 'profile_pics/default.jpg':
		if os.path.isfile(currentEmployee.Profile_Image.path) is not None:
			os.remove(currentEmployee.Profile_Image.path)
		currentEmployee.Profile_Image=DEFAULT
		currentEmployee.save()
		userObject = Employee.objects.get(Employee_ID=Editempid)
		if userObject.Role.Role_ID == 1:
			return redirect('sys_admin_home')
		elif userObject.Role.Role_ID == 2:
			return redirect('HR_home')
		elif userObject.Role.Role_ID == 3:
			return redirect('Home')


def logout(request):
	try:
		del request.session['Employee_ID']
	except KeyError:
		pass
	request.session.flush()

	messages.info(request, 'You have been logged out')
	return redirect('login')



