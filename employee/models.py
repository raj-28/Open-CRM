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
    address = models.CharField(max_length=100)
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
    work_duration = models.CharField(blank=True,null=True,max_length=20,default="00:00:00 Hr")



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
    work_duration = models.CharField(blank=True,null=True,max_length=20,default="00:00:00 Hr")




    def __str__(self):
        date=str(self.attendance_date)
        return date+"_" +self.user.username


# class Task(models.Model):


class Task(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by')
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_to')
    task_subject = models.CharField(max_length=100)
    task_detail = models.TextField()
    status = models.CharField(max_length=10,blank=True,null=True)
    completed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    due_date = models.DateField(blank=True,null=True)
    created_at = models.DateField(blank=True,null=True,auto_now_add=True)

    def __str__(self):
        return self.created_by.username +"_to_"+self.assigned_to.username

mode=[('assign','assign'),
('reply','reply'),
]

class Task_Media(models.Model):
    task_id = models.ForeignKey(Task,on_delete=models.CASCADE)
    media = models.FileField(upload_to='task_media/',blank=True,null=True)
    description = models.CharField(max_length=400)
    media_mode = models.CharField(max_length=50,choices=mode,default='assign')

class Task_Comment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_id')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    comment = models.TextField(blank=True,null=True)
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user.username



