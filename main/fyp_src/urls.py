"""fyp_src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    pip install apscheduler

"""
from django.contrib import admin
from django.urls import path, include
from index.views import index,camera,HR,sys_admin,employees
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', index.index_home, name='index'),
    path('login/', index.index_login, name='login'),
    path('logout/', index.logout,name='logout'),
    path('employee/DeletedPicture/<int:Editempid>/', index.DeletedButton, name='DeletePic'),

    path('admin/', admin.site.urls),
    path('sys_admin/home/', sys_admin.sys_admin_home, name='sys_admin_home'), 
    path('sys_admin/view_employees/', sys_admin.sys_admin_view_employees, name='sys_admin_view_employees'),
    path('sys_admin/view_employees/delete/<int:delete_employee_id>/', sys_admin.delete_employee, name='sys_admin_delete_employee'),
    path('sys_admin/view_employees/edit/<int:edit_employee_id>', sys_admin.edit_employee, name='sys_admin_edit_employee'),
    path('sys_admin/create_user/', sys_admin.sys_admin_create_user, name='sys_admin_create_user'),
    path('sys_admin/user_profile/', sys_admin.user_profile, name='sys_admin_user_profile'),
    path('sys_admin/schedule/', sys_admin.schedule, name='sys_admin_schedule'),
    path('sys_admin/upload_img/<int:empid>', sys_admin.upload_img, name='sys_admin_upload_img'),
    path('sys_admin/deletEmp_image/<int:empid>', sys_admin.sys_admin_deleepmPic, name='deleEmpimage'),
    path('sys_admin/user_profile/DeletedPicture/', sys_admin.delete_my_pfp, name="sys_admin_delete_my_pfp"),

    path('HR/home/', HR.HR_home, name='HR_home'),
    path('HR/Profile/', HR.HR_Profile, name='HR_Profile'),
    path('HR/Employees/', HR.HR_EmployeePage, name='EmployeesPage'),
    path('HR/Employees/EmployeeProfile/<int:Empid>', HR.HR_EmpProfile, name='EmployeesProfile'),
    path('HR/View_Schedule', HR.HR_View_Schedule, name='View_Schedule'),
    path('HR/Employee/Status/<int:Empid>/<int:Wid>/', HR.Change_Status, name='EmployeeStatus'),
    path('HR/Employee/Schedule/<int:Editempid>/', HR.Employee_View_Schedule, name='EmployeeSchedule'),
    path('HR/Employee/Update/Schedule/<int:Editempid>/', HR.Emp_update_Schedule, name='UpdateEmpSchedule'),

    path('camera/', camera.index, name='camera'),
    path('camera/feed', camera.video_feed, name='video_feed'),
    path('check_in/', index.Check_In, name='Check_in'),
    path('employee/employee_home',employees.Employee_home, name='Home'),
    path('employee_profile/',employees.viewProfile, name='Profile'),
    path('employee/schedule', employees.Employee_schedule, name='Employee_schedule'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
