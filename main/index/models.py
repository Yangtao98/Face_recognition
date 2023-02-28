from django.db import models

# Create your models here.
# all models are to be created in index.models
def user_directory_path(instance, filename): 
	name, ext = filename.split(".")
	name = instance.Employee_ID+"_"+ instance.section
	filename = name +'.'+ ext
	return 'Users_images/{}'.format(filename)


class Role(models.Model):
	Role_ID = models.IntegerField(primary_key=True)
	Role_Name = models.CharField(max_length=100)

	def __str__(self):
		return self.Role_Name

class Employee(models.Model):
	Employee_ID = models.IntegerField(primary_key=True)
	Full_Name = models.CharField(max_length=100)
	Job_Title = models.CharField(max_length=100)
	Phone_Number = models.CharField(max_length=100)
	salt = models.CharField(max_length=50, null=True)
	Email_Address = models.EmailField()
	Role = models.ForeignKey(Role, on_delete=models.CASCADE)
	Profile_Image = models.ImageField(null=True,blank=True, upload_to='profile_pics/')
	
	# change to password hashes later
	Password = models.CharField(max_length=256)
	Start_Date = models.DateField(auto_now_add=True)
	
	#Salt = models.CharField(max_length=100)

	def __str__(self):
		return f'Employee {self.Employee_ID}'


class WorkSchedule(models.Model):


	WorkSchedule_id = models.BigAutoField(primary_key=True)
	Employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
	#attendance
	InTime = models.TimeField(max_length=256, null=True, blank=True)
	OutTime = models.TimeField(max_length=256, null=True, blank=True)

	# schedule
	Mark = models.CharField(max_length=256,null=True)
	StartDate = models.DateField()
	StartTime = models.TimeField(null=True)
	EndTime = models.TimeField(null=True)


	def __str__(self):
		return f'WorkSchedule {self.Employee}'

	class Meta:
		db_table = 'WorkSchedule'
