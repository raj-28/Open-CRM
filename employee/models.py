from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
# Create your models here.

dept=[('Information Technology','Information Technology'),
    ('Manager','Manager'),
    ('Accounts','Accounts'),
    ('Sales','Sales'),
    ('HR','HR'),
    ('Admin','Admin'),
]

gndr=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]

class Hr(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email= models.EmailField(blank=False,null=False)
    profile_pic= models.ImageField(upload_to='profile_pic/HrProfilePic/',null=True,blank=True,default='default.jpeg')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    DOJ = models.DateTimeField(auto_now_add=True,)
    status=models.BooleanField(default=False)
    department=models.CharField(max_length=50, choices=dept,default='Information Technology')
    designation=models.CharField(max_length=200,blank=True,null=True)
    gender=models.CharField(default='Other',choices=gndr,max_length=50)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.user.last_name)


departments=[('Information Technology','Information Technology'),
    ('Manager','Manager'),
    ('Accounts','Accounts'),
    ('Sales','Sales'),
    ('HR','HR'),
    ('Admin','Admin'),
]

gender=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email= models.EmailField(blank=False,null=False)
    profile_pic= models.ImageField(upload_to='profile_pic/employeeProfilePic/',null=True,blank=True,default='default.jpeg')
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20,null=False)
    DOJ=models.DateField(auto_now_add=True,)
    status=models.BooleanField(default=False)
    department=models.CharField(max_length=50, choices=departments,default='Information Technology')
    designation=models.CharField(max_length=200,blank=True,null=True)
    gender=models.CharField(default='Other',choices=gender,max_length=50)
    reports_to=models.CharField(max_length=100,blank=True,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Persional_Info(models.Model):
    employee_id=models.OneToOneField(User,on_delete=models.CASCADE)
    adhar_card_no=models.CharField(max_length=100)
    nationality=models.CharField(max_length=100)
    religion=models.CharField(max_length=100)
    marital_status=models.BooleanField(default=False)
    email_id=models.EmailField()
    contact_no=PhoneField(blank=True, help_text='Contact phone number')
    guardian_name=models.CharField(max_length=200)
    relationship=models.CharField(max_length=100)
    guardian_contact=PhoneField(blank=True)


    def __str__(self):
        return self.employee_id.username+" "+self.employee_id.first_name


class Bank_Info(models.Model):
    employee_id=models.OneToOneField(User,on_delete=models.CASCADE)
    bank_name=models.CharField(max_length=100)
    bank_acc_no=models.CharField(max_length=50)
    bank_ifsc=models.CharField(max_length=50)
    pan_no=models.CharField(max_length=50)


    def __str__(self):
        return self.employee_id.username+" "+self.employee_id.first_name

class Education_Info(models.Model):
    employee_id=models.OneToOneField(User,on_delete=models.CASCADE)
    institute_name=models.CharField(max_length=200)
    course_name=models.CharField(max_length=100)
    start_year=models.CharField(max_length=10)
    final_year=models.CharField(max_length=10)


    def __str__(self):
        return self.employee_id.username+" "+self.employee_id.first_name

class Attendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attendance_date=models.DateField(blank=False,null=False)
    present=models.BooleanField(default=False)
    Start_time=models.TimeField(null=True,blank=True)
    end_time=models.TimeField(null=True,blank=True)
    approved = models.BooleanField(default=False)



    def __str__(self):
        date=str(self.attendance_date)
        return date+"_" +self.user.username

class Hr_Attendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attendance_date=models.DateField(blank=False,null=False)
    present=models.BooleanField(default=False)
    Start_time=models.TimeField(null=True,blank=True)
    end_time=models.TimeField(null=True,blank=True)
    approved = models.BooleanField(default=False)



    def __str__(self):
        date=str(self.attendance_date)
        return date+"_" +self.user.username


# class Task(models.Model):

