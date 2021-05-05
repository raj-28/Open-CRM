import csv
from datetime import datetime,timedelta
# import datetime
from django.utils import timezone

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse

from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            # user= form.cleaned_data.get('username') '''this is for get username from form'''
            # print(user)
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'adminsignup.html',{'form':form})


#-----------for checking user is Hr , Employee or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_Hr(user):
    return user.groups.filter(name='HR').exists()
def is_Employee(user):
    return user.groups.filter(name='EMPLOYEE').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,Hr OR Employee
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_Hr(request.user):
        activate=models.Hr.objects.all().filter(user_id=request.user.id,status=True)
        if activate:
            return redirect('hr-dashboard')
    elif is_Employee(request.user):
        accountapproval=models.Employee.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('employee-dashboard')





#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    # hr=models.Hr.objects.all().order_by('-id')
    # patients=models.Patient.objects.all().order_by('-id')
    # #for three cards
    # doctorcount=models.Doctor.objects.all().filter(status=True).count()
    # pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()
    #
    # patientcount=models.Patient.objects.all().filter(status=True).count()
    # pendingpatientcount=models.Patient.objects.all().filter(status=False).count()
    #
    # appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    # mydict={
    # 'doctors':doctors,
    # 'patients':patients,
    # 'doctorcount':doctorcount,
    # 'pendingdoctorcount':pendingdoctorcount,
    # 'patientcount':patientcount,
    # 'pendingpatientcount':pendingpatientcount,
    # 'appointmentcount':appointmentcount,
    # 'pendingappointmentcount':pendingappointmentcount,
    # }
    # return render(request,'hospital/admin_dashboard.html',context=mydict)
    return render(request,'admin_dashboard.html')


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_hr_view(request):
    return render(request,'admin_hr.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_hr_view(request):
    userForm=forms.HrUserForm()
    HrForm=forms.HrForm()
    mydict={'userForm':userForm,'hrForm':HrForm}
    if request.method=='POST':
        userForm=forms.HrUserForm(request.POST)
        hrForm=forms.HrForm(request.POST, request.FILES)
        if userForm.is_valid() and hrForm.is_valid():
            user=userForm.save()
            print(user.password)
            user.set_password(user.password)
            user.save()

            hr=hrForm.save(commit=False)
            hr.user=user
            hr.status=True
            hr.save()

            my_HR_group = Group.objects.get_or_create(name='HR')
            my_HR_group[0].user_set.add(user)

            obj1=models.Persional_Info.objects.create(employee_id=user,)
            obj2=models.Bank_Info.objects.create(employee_id=user,)
            obj2=models.Education_Info.objects.create(employee_id=user,)
        # print(userForm.errors)
        # print(hrForm.errors)
        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'admin_add_hr.html',context=mydict)




#---------------------------------------------------------------------------------
#------------------------ Hr RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_dashboard_view(request):
    #for three cards
    employee=models.Employee.objects.all().filter(status=True).count()
    deactivated_employee=models.Employee.objects.all().filter(status=False).count()
    total_tasks = models.Task.objects.filter(completed=False,assigned_to=request.user).count()
    total_noti = models.Notifications.objects.filter(is_seen=False,assigned_to=request.user).count()
    notifications = models.Notifications.objects.filter(is_seen=False,assigned_to=request.user).order_by('-id')
    seened_noti = models.Notifications.objects.filter(is_seen=True,assigned_to=request.user).order_by('-id')


    mydict={
    'employee':employee,
    'deactivated_employee':deactivated_employee,
    'total_task':total_tasks,
    'total_noti':total_noti,
    'notifications':notifications,
    'seen_notifications':seened_noti    ,
    }
    # return render(request,'hospital/doctor_dashboard.html',context=mydict)
    return render(request,'hr_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
def hr_profile(request,slug):
    user=get_object_or_404(models.User,username=slug)
    if is_Hr(request.user):
        if is_Hr(user):
            personal_info=get_object_or_404(models.Hr,user=user)
            employeeinfo=get_object_or_404(models.Persional_Info,employee_id=user)
            educationinfo=get_object_or_404(models.Education_Info,employee_id=user)
            bankinfo=get_object_or_404(models.Bank_Info,employee_id=user)
            dict={
                'personalinfo':personal_info,
                'employeeinfo':employeeinfo,
                'educationinfo':educationinfo,
                'bankinfo':bankinfo,
                'slug':slug
            }
            return render(request,'hr_profile.html',context=dict)
        elif is_Employee(user):
            personal_info=get_object_or_404(models.Employee,user=user)
            employeeinfo=get_object_or_404(models.Persional_Info,employee_id=user)
            educationinfo=get_object_or_404(models.Education_Info,employee_id=user)
            bankinfo=get_object_or_404(models.Bank_Info,employee_id=request.user)
            dict={
                'personalinfo':personal_info,
                'employeeinfo':employeeinfo,
                'educationinfo':educationinfo,
                'bankinfo':bankinfo,
                'slug':slug
            }
            return render(request,'hr_profile.html',context=dict)
        else:
            return HttpResponse("wrong url")
    elif is_Employee(request.user):
        if user==request.user:
            personal_info=get_object_or_404(models.Employee,user=request.user)
            employeeinfo=get_object_or_404(models.Persional_Info,employee_id=request.user)
            educationinfo=get_object_or_404(models.Education_Info,employee_id=request.user)
            bankinfo=get_object_or_404(models.Bank_Info,employee_id=request.user)

            dict={
                'personalinfo':personal_info,
                'employeeinfo':employeeinfo,
                'educationinfo':educationinfo,
                'bankinfo':bankinfo,
                'slug':slug
            }
            return render(request,'employee_profile.html',context=dict)
        else:
            return HttpResponse("you don't allow this")
    else:
        return HttpResponse("Error")




@login_required(login_url='adminlogin',)
@user_passes_test(is_Hr)
def hr_employee_view(request):
    mydict={
    'Hr':models.Hr.objects.get(user_id=request.user.id), #for profile picture of hr in sidebar
    }
    return render(request,'hr_employee.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_add_employee_view(request):
    userForm=forms.EmployeeUserForm()
    empForm=forms.EmployeeForm()
    mydict={'userForm':userForm,'empForm':empForm}
    if request.method=='POST':
        userForm=forms.EmployeeUserForm(request.POST)
        employeeForm=forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user=userForm.save()
            print(user.password)
            user.set_password(user.password)
            user.save()

            hr=employeeForm.save(commit=False)
            hr.user=user
            hr.status=True
            hr.save()

            my_HR_group = Group.objects.get_or_create(name='EMPLOYEE')
            my_HR_group[0].user_set.add(user)
            obj1=models.Persional_Info.objects.create(employee_id=user,)
            obj2=models.Bank_Info.objects.create(employee_id=user,)
            obj2=models.Education_Info.objects.create(employee_id=user,)

        return HttpResponseRedirect('hr-add-employee')
    return render(request,'hr_add_employee.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_view_employee_view(request):
    employee=models.Employee.objects.all().filter(status=True)
    hr=models.Hr.objects.all().filter(status=True)

    return render(request,'hr_view_employee.html',{'employees':employee,'hrs':hr})

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_view_attendance(request):
    today = timezone.now().today().date()
    hr_obj = models.Hr.objects.all()
    emp_obj = models.Employee.objects.all()
    hrattend=models.Hr_Attendance.objects.filter(attendance_date=today,user=request.user)
    #if attendannce object is not create then 1st create and then go ahead
    if not hrattend:
        for user in hr_obj:
            att=models.Hr_Attendance.objects.filter(attendance_date=today,user=user.user)
            if not att:
                obj=models.Hr_Attendance.objects.create(user=user.user,attendance_date=today)
        for user in emp_obj:
            att1=models.Attendance.objects.filter(attendance_date=today,user=user.user)
            if not att1:
                obj=models.Attendance.objects.create(user=user.user,attendance_date=today)

    return render(request,'attendance_card.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_add_attendance(request):
    today = timezone.now().today().date()
    hrattend=models.Hr_Attendance.objects.filter(attendance_date=today,user=request.user)
    hrattend2=models.Hr_Attendance.objects.all().order_by('-attendance_date')
    hrlist=[]

    for i in hrattend2:
        if i.attendance_date==today:
            print("hello")
        elif i.attendance_date<today:
            hrlist.append(i)


    mydict={
        'todayattend':hrattend,
        'hrattends':hrlist,
        'today':today
    }
    return render(request,'hr_view_attendance.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_view_employee_attendance(request):
    today = timezone.now().today().date()
    empattendance=models.Attendance.objects.filter(attendance_date=today)
    attendance=models.Attendance.objects.filter().order_by('-attendance_date')
    atendlist=[]
    for i in attendance:
        if i.attendance_date==today:
            print("pass")
        elif i.attendance_date<today:
            atendlist.append(i)
    dict={
        'empattendance':empattendance,
        'today':today,
        'allempattndnc':atendlist,
    }
    return render(request,'hr_approved_employee_attendance.html',context=dict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def filter_by_date(request):
    today = timezone.now().today().date()
    empattendance=models.Attendance.objects.filter(attendance_date=today,user=request.user)
    attendance=models.Attendance.objects.filter().order_by('-attendance_date')
    atendlist=[]
    if request.method == "POST":
        start = request.POST.get('from')
        end = request.POST.get('end')
        status = request.POST.get('status')
        print("pass")
        if status == 'p':
            empattendance=models.Attendance.objects.filter(attendance_date__range=[str(start), str(end)],present=True)
        elif status == 'a':
            empattendance=models.Attendance.objects.filter(attendance_date__range=[str(start), str(end)],present=False)
        else:
            empattendance=models.Attendance.objects.filter(attendance_date__range=[str(start), str(end)])
            print(empattendance)
        dict={

            'allempattndnc':empattendance,
            'from':start,
            'end':end,

        }
        return render(request,'attandance_filter.html',context=dict)
@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def filter_by_month(request):
    today = timezone.now().today().date()
    atendlist=[]
    month="January"
    if request.method == "POST":
        month_no = request.POST.get('month')
        empattendance=models.Attendance.objects.filter(attendance_date__month=month_no)
        if month_no=="1":
            month="January"
        elif month_no=="2":
            month="February"
        elif month_no=="3":
            month="March"
        elif month_no=="4":
            month="April"
        elif month_no=="5":
            month="May"
        elif month_no=="6":
            month="June"
        elif month_no=="7":
            month="July"
        elif month_no=="8":
            month="August"
        elif month_no=="9":
            month="September"
        elif month_no=="10":
            month="October"
        elif month_no=="11":
            month="November"
        elif month_no=="11":
            month="December"

        dict={

            'allempattndnc':empattendance,
            'from':month,
            'only':True


        }
        return render(request,'attandance_filter.html',context=dict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def filter_attendance(request):
    today = timezone.now().today().date()
    empattendance=models.Attendance.objects.filter(attendance_date=today)
    attendance=models.Attendance.objects.filter().order_by('-attendance_date')
    atendlist=[]
    for i in attendance:
        if i.attendance_date==today:
            print("pass")
        elif i.attendance_date<today:
            atendlist.append(i)
    dict={
        'empattendance':{},

        'allempattndnc':{},
    }
    return render(request,'attandance_filter.html',context=dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_approved(request,slug):
    today = timezone.now().today().date()
    date=slug.split('_')
    mydate=date[1]
    userid=date[0]
    today=str(today)
    if today==mydate:

        hr_obj = models.Hr.objects.all()
        emp_obj = models.Employee.objects.all()
        empattendance=models.Attendance.objects.filter(attendance_date=today)
        obj=get_object_or_404(models.Attendance,user=userid,attendance_date=today)
        obj.approved=True
        obj.save()

        tomorrow = datetime.today().date() + timedelta(days=1)
        username=get_object_or_404(models.User,id=userid)
        getobj=models.Attendance.objects.filter(user=userid,attendance_date=tomorrow)
        print(getobj)
         #if attendannce object is not create then 1st create and then go ahead
        if not getobj:

            for user in hr_obj:
                att=models.Hr_Attendance.objects.filter(attendance_date=tomorrow,user=user.user)
                if not att:
                    obj=models.Hr_Attendance.objects.create(user=user.user,attendance_date=tomorrow)
            for user in emp_obj:
                att1=models.Attendance.objects.filter(attendance_date=tomorrow,user=user.user)
                if not att1:
                    obj=models.Attendance.objects.create(user=user.user,attendance_date=tomorrow)
    else:
        obj=get_object_or_404(models.Attendance,user=userid,attendance_date=mydate)
        obj.approved=True
        obj.save()

    return redirect('hr-view-attendance')

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_unapproved(request,slug):
    today = timezone.now().today().date()
    empattendance=models.Attendance.objects.filter(attendance_date=today)
    obj=get_object_or_404(models.Attendance,user=slug,attendance_date=today)
    obj.approved=False
    obj.save()
    return redirect('hr-view-attendance')


###attendance exel seat download for any perticular user
@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def attendance_download_exel(request,slug):
    # Get all data from UserDetail Databse Table
    username = get_object_or_404(models.User,username=slug)
    if is_Hr(username):
        attendance = models.Hr_Attendance.objects.filter(user=username).order_by('-attendance_date')
    elif is_Employee(username):
        attendance = models.Attendance.objects.filter(user=username).order_by('-attendance_date')
    else:
        attendance = "nothning"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atten_({})_({} {}).csv"'.format(username.username,username.first_name,username.last_name)

    writer = csv.writer(response)
    writer.writerow(['username:{} ({} {})'.format(username.username, username.first_name,username.last_name),])
    writer.writerow([""])

    writer.writerow(['Attendance Date', 'Attendance', 'Start_time', 'End_time','Work Duration', 'Approved', ])
    January=False
    February=False
    March = False
    April = False
    May = False
    June = False
    July = False
    August = False
    September = False
    October = False
    November = False
    December = False

    for atnd in attendance:
        date = str(atnd.attendance_date)
        month = date.split('-')
        print(month)
        month=month[1]
        if atnd.present:
            present="Present"
        else:
            present="Absent"
        if atnd.approved:
            approved = "Approved"
        else:
            approved = "Pending"
        if month=="01" and January==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("January")])
            writer.writerow([""])
            January=True
        elif month=="02" and February==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("February")])
            writer.writerow([""])
            February=True
        elif month=="03" and March==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("March")])
            writer.writerow([""])
            March=True
        elif month=="04" and April==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("April")])
            writer.writerow([""])
            April=True
        elif month=="05" and May==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("May")])
            writer.writerow([""])
            May=True
        elif month=="06" and June==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("June")])
            writer.writerow([""])
            June=True
        elif month=="07" and July==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("July")])
            writer.writerow([""])
            July=True
        elif month=="08" and August==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("August")])
            writer.writerow([""])
            August=True
        elif month=="09" and September==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("January")])
            writer.writerow([""])
            March=True
        elif month=="10" and October==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("October")])
            writer.writerow([""])
            October=True
        elif month=="11" and November==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("November")])
            writer.writerow([""])
            November=True
        elif month=="12" and December==False:
            writer.writerow([""])
            writer.writerow(["","","{}".format("December")])
            writer.writerow([""])
            December=True

        writer.writerow([date, present, atnd.Start_time, atnd.end_time, atnd.work_duration, approved,])


    return response

#---------------------------------------------------------------------------------
#------------------------ EMPLOYEE RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_Employee)
def employee_dashboard_view(request):
    total_tasks = models.Task.objects.filter(completed=False,assigned_to=request.user).count()
    total_noti = models.Notifications.objects.filter(assigned_to=request.user,is_seen=False).count()
    notifications = models.Notifications.objects.filter(is_seen=False,assigned_to=request.user).order_by('-id')
    seened_noti = models.Notifications.objects.filter(is_seen=True,assigned_to=request.user).order_by('-id')[:5]

    mydict={
    'total_tasks':total_tasks,
    'total_noti':total_noti,
    'notifications':notifications,
    'seen_notifications':seened_noti,
    }

    return render(request,'employee_dashboard.html',context=mydict)

# @login_required(login_url='adminlogin')
# @user_passes_test(is_Employee)
# def employee_profile(request):
#     personal_info=get_object_or_404(models.Employee,user=request.user)
#     employeeinfo=get_object_or_404(models.Persional_Info,employee_id=request.user)
#     educationinfo=get_object_or_404(models.Education_Info,employee_id=request.user)
#     dict={
#         'personalinfo':personal_info,
#         'employeeinfo':employeeinfo,
#         'educationinfo':educationinfo,
#     }
#     return render(request,'employee_profile.html',context=dict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Employee)
def employee_attendance(request):
    today = timezone.now().today().date()

    hr_obj = models.Hr.objects.all()
    emp_obj = models.Employee.objects.all()
    empattend=models.Attendance.objects.filter(attendance_date=today,user=request.user)
    empattend2=models.Attendance.objects.filter(user=request.user).order_by('-attendance_date')
    emplist=[]
    for i in empattend2:
        if i.attendance_date==today:
            print("hello")
        elif i.attendance_date<today:
            emplist.append(i)
    #if attendannce object is not create then 1st create and then go ahead
    if not empattend:
        for user in hr_obj:
            att=models.Hr_Attendance.objects.filter(attendance_date=today,user=user.user)
            if not att :
                obj=models.Hr_Attendance.objects.create(user=user.user,attendance_date=today)
        for user in emp_obj:
            att1=models.Attendance.objects.filter(attendance_date=today,user=user.user)
            if not att1:
                obj=models.Attendance.objects.create(user=user.user,attendance_date=today)
        # obj=models.Attendance.objects.create(user=request.user,attendance_date=today)
        empattend=models.Attendance.objects.filter(attendance_date=today,user=request.user)
        # empattend2=models.Attendance.objects.filter(user=request.user)

        mydict={
            'todayattend':empattend,
            'empattends':emplist,
            'today':today,
        }
        return render(request,'attendance.html',context=mydict)
    else:
        mydict={
            'todayattend':empattend,
            'empattends':emplist,
            'today':today
        }
        return render(request,'attendance.html',context=mydict)

@login_required(login_url='adminlogin')
def start_session(request):
    if is_Employee(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Attendance,attendance_date=today,user=request.user)
        obj.Start_time=timezone.now().time()
        obj.present=True
        obj.save()
        return redirect('employee-attendance')
    elif is_Hr(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Hr_Attendance,attendance_date=today,user=request.user)
        obj.Start_time=timezone.now().time()
        obj.present=True
        obj.save()
        return redirect('hr-add-attendance')
    else:
        return HttpResponse("you are not eligible for this system")


@login_required(login_url='adminlogin')
def end_session(request):
    if is_Employee(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Attendance,attendance_date=today,user=request.user)
        obj.end_time=timezone.now().time()
        date_format = "%H:%M:%S"
        start_time = obj.Start_time
        end_time=timezone.now().time()
        diff = datetime.combine(today,end_time)-datetime.combine(today,start_time)
        duration = str(diff)
        dur=duration.split('.')
        duration=dur[0]+" "+"Hr"

        # duration = datetime.timedelta(end_time,start_time)
        obj.work_duration = duration
        obj.present=True
        obj.save()
        return redirect('employee-attendance')
    elif is_Hr(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Hr_Attendance,attendance_date=today,user=request.user)
        obj.end_time=timezone.now().time()
        obj.approved=True
        date_format = "%H:%M:%S"
        start_time = obj.Start_time
        end_time=timezone.now().time()
        diff = datetime.combine(today,end_time)-datetime.combine(today,start_time)
        duration = str(diff)
        dur=duration.split('.')
        duration=dur[0]+" "+"Hr"

        # duration = datetime.timedelta(end_time,start_time)
        obj.work_duration = duration
        obj.present=True
        obj.save()
        return redirect('hr-add-attendance')

@login_required(login_url='adminlogin')
def lunch_break_start(request):
    if is_Employee(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Attendance,attendance_date=today,user=request.user)
        obj.start_lunch_break=timezone.now().time()
        obj.present=True
        obj.save()
        return redirect('employee-attendance')
    elif is_Hr(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Hr_Attendance,attendance_date=today,user=request.user)
        obj.start_lunch_break=timezone.now().time()
        obj.present=True
        obj.save()
        return redirect('hr-add-attendance')
    else:
        return HttpResponse("you are not eligible for this system")

@login_required(login_url='adminlogin')
def lunch_break_end_session(request):
    if is_Employee(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Attendance,attendance_date=today,user=request.user)
        obj.end_lunch_break=timezone.now().time()
        date_format = "%H:%M:%S"
        start_time = obj.start_lunch_break
        end_time=timezone.now().time()
        diff = datetime.combine(today,end_time)-datetime.combine(today,start_time)
        duration = str(diff)
        dur=duration.split('.')
        duration=dur[0]+" "+"Hr"

        # duration = datetime.timedelta(end_time,start_time)
        obj.lunch_break_duration = duration
        obj.present=True
        obj.save()
        return redirect('employee-attendance')
    elif is_Hr(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Hr_Attendance,attendance_date=today,user=request.user)
        obj.end_lunch_break=timezone.now().time()
        obj.approved=True
        date_format = "%H:%M:%S"
        start_time = obj.start_lunch_break
        end_time=timezone.now().time()
        diff = datetime.combine(today,end_time)-datetime.combine(today,start_time)
        duration = str(diff)
        dur=duration.split('.')
        duration=dur[0]+" "+"Hr"

        # duration = datetime.timedelta(end_time,start_time)
        obj.lunch_break_duration = duration
        obj.present=True
        obj.save()
        return redirect('hr-add-attendance')

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def employee_absent(request,slug):
    today = timezone.now().today().date()
    tomorrow = datetime.today().date() + timedelta(days=1)
    username=get_object_or_404(models.User,id=slug)
    getobj=models.Attendance.objects.filter(user=slug,attendance_date=tomorrow)
    obj1=get_object_or_404(models.Attendance,user=slug,attendance_date=today)
    if not getobj:
        obj=models.Attendance.objects.create(user=username,attendance_date=tomorrow,)
    obj1.approved=True
    obj1.save()
    return redirect('hr-view-attendance')


##profile edit for employee

@login_required(login_url='adminlogin')
def edit_company_info(request):
    if is_Hr(request.user):
        get_info=get_object_or_404(models.Hr,user=request.user)
        p_form = forms.ProfileUpdateFormforHr(request.POST,instance=request.user.hr)
        if request.method == 'POST':
            p_form = forms.ProfileUpdateFormforHr(request.POST, request.FILES or None,instance=request.user.hr)
            if  p_form.is_valid():

                p_form.save()
            user=get_object_or_404(models.User,id=request.user.id)
            hr=get_object_or_404(models.Hr,user=user)
            user.first_name=request.POST.get('firstname')
            user.last_name=request.POST.get('lastname')
            user.save()

            hr.gender=request.POST.get('gender')
            hr.gender=request.POST.get('address')
            hr.save()

            return redirect('profile',user.username)

        dict={
            'info':get_info,
            'p_form':p_form,
            'is_hr':True
        }
        return render(request,'profile_edit/edit_company_info.html',context=dict)
    elif is_Employee(request.user):
        get_info=get_object_or_404(models.Employee,user=request.user.id)
        p_form = forms.ProfileUpdateForm(request.POST,instance=request.user.employee)
        if request.method == 'POST':
            p_form = forms.ProfileUpdateForm(request.POST, request.FILES or None,instance=request.user.employee)
            if  p_form.is_valid():

                p_form.save()

            user=get_object_or_404(models.User,id=request.user.id)
            emp=get_object_or_404(models.Employee,user=user)

            user.first_name=request.POST.get('firstname')
            user.last_name=request.POST.get('lastname')
            user.save()

            emp.gender=request.POST.get('gender')
            emp.address=request.POST.get('address')
            emp.save()

            return redirect('profile',user.username)


        dict={
            'info':get_info,
            'p_form':p_form,
            'is_hr':False
        }

        return render(request,'profile_edit/edit_company_info.html',context=dict)
    else:
        return HttpResponse("Error")


@login_required(login_url='adminlogin')
def edit_personal_info(request):
    if is_Hr(request.user):
        get_info=get_object_or_404(models.Persional_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Hr,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            hr=get_object_or_404(models.Persional_Info,employee_id=user)

            hr.adhar_card_no=request.POST.get('aadharno')
            hr.nationality=request.POST.get('nationality')

            hr.religion=request.POST.get('religion')
            merital=request.POST.get('meritalstatus')
            if merital=="UnMarried":

                hr.marital_status=False
            else:
                hr.merital_status=True
            hr.email_id=request.POST.get('email')
            hr.contact_no=request.POST.get('mobileno')
            hr.guardian_name=request.POST.get('gardianname')
            hr.relationship=request.POST.get('relationship')
            hr.guardian_contact=request.POST.get('conttactno')
            hr.save()

            return redirect('profile',user.username)
        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':True
        }
        return render(request,'profile_edit/edit_personal_info.html',context=dict)
    elif is_Employee(request.user):
        get_info=get_object_or_404(models.Persional_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Employee,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            emp=get_object_or_404(models.Persional_Info,employee_id=user)

            emp.adhar_card_no=request.POST.get('aadharno')
            emp.nationality=request.POST.get('nationality')

            emp.religion=request.POST.get('religion')
            emp.marital_status=request.POST.get('meritalstatus')
            emp.email_id=request.POST.get('email')
            emp.contact_no=request.POST.get('mobileno')
            emp.guardian_name=request.POST.get('gardianname')
            emp.relationship=request.POST.get('relationship')
            emp.guardian_contact=request.POST.get('conttactno')
            emp.save()
            return redirect('profile',user.username)

        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':False
        }
        return render(request,'profile_edit/edit_personal_info.html',context=dict)
    else:
        return HttpResponse("Error")


@login_required(login_url='adminlogin')
def edit_education_info(request):
    if is_Hr(request.user):
        get_info=get_object_or_404(models.Education_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Hr,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            e_info=get_object_or_404(models.Education_Info,employee_id=user)

            e_info.institite_name=request.POST.get('institutename')
            e_info.course_name=request.POST.get('coursename')

            e_info.start_year=request.POST.get('starts')
            e_info.final_year=request.POST.get('ends')

            e_info.save()
            return redirect('profile',user.username)

        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':True
        }
        return render(request,'profile_edit/edit_education_info.html',context=dict)
    elif is_Employee(request.user):
        get_info=get_object_or_404(models.Education_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Employee,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            e_info=get_object_or_404(models.Education_Info,employee_id=user)

            e_info.institite_name=request.POST.get('institutename')
            e_info.course_name=request.POST.get('coursename')

            e_info.start_year=request.POST.get('starts')
            e_info.final_year=request.POST.get('ends')

            e_info.save()
            return redirect('profile',user.username)
        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':False
        }
        return render(request,'profile_edit/edit_education_info.html',context=dict)
    else:
        return HttpResponse("Error")

@login_required(login_url='adminlogin')
def edit_bank_info(request):
    if is_Hr(request.user):
        get_info=get_object_or_404(models.Bank_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Hr,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            b_info=get_object_or_404(models.Bank_Info,employee_id=user)

            b_info.bank_name=request.POST.get('bankname')
            b_info.bank_acc_no=request.POST.get('bankaccnu')

            b_info.bank_ifsc=request.POST.get('ifsccode')
            b_info.pan_no=request.POST.get('panno')

            b_info.save()
            return redirect('profile',user.username)
        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':True
        }
        return render(request,'profile_edit/edit_bank_info.html',context=dict)
    elif is_Employee(request.user):
        get_info=get_object_or_404(models.Bank_Info,employee_id=request.user)
        profile_pics=get_object_or_404(models.Employee,user=request.user)
        if request.method == 'POST':
            user=get_object_or_404(models.User,id=request.user.id)
            b_info=get_object_or_404(models.Bank_Info,employee_id=user)

            b_info.bank_name=request.POST.get('bankname')
            b_info.bank_acc_no=request.POST.get('bankaccnu')

            b_info.bank_ifsc=request.POST.get('ifsccode')
            b_info.pan_no=request.POST.get('panno')

            b_info.save()
            return redirect('profile',user.username)
        dict={
            'info':get_info,
            'profile_pics':profile_pics,
            'is_hr':False
        }
        return render(request,'profile_edit/edit_bank_info.html',context=dict)
    else:
        return HttpResponse("Error")


@login_required(login_url='adminlogin')
def task_view(request):
    dict={
        'is_hr':is_Hr(request.user)
    }
    return render(request,'tasks/task_view.html',context=dict)

@login_required(login_url='adminlogin')
def my_tasks(request):
    tasks = models.Task.objects.filter(created_by=request.user).order_by('-id')
    dict={
        'tasks':tasks,
        'is_hr':is_Hr(request.user),
    }
    return render(request,'tasks/my_tasks.html',context=dict)

@login_required(login_url='adminlogin')
def create_task(request):
    user = models.User.objects.filter()
    users1=[]
    users2=[]
    for i in user:
        if i!=request.user:
            if i.groups.filter(name="EMPLOYEE").exists():
                users1.append(i)
            elif i.groups.filter(name="HR").exists():
                users2.append(i)

    users=[]
    users=users1+users2

    if request.method=='POST':
        task_sub = request.POST.get('subject')
        task_detail = request.POST.get('details')
        assigned_to = request.POST.get('assigned')
        usr = get_object_or_404(models.User,username=assigned_to)
        created_by=request.user
        due_date = request.POST.get('duedate')

        if due_date=="":
            task=models.Task.objects.create(created_by=created_by,assigned_to=usr,task_subject=task_sub,task_detail=task_detail,)
            print(task.id)
        else:
            task=models.Task.objects.create(created_by=created_by,assigned_to=usr,task_subject=task_sub,task_detail=task_detail,due_date=due_date)
        task_id=get_object_or_404(models.Task,id=task.id)
        noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=usr,type="task_assigned",task_id=task_id)
        return redirect('add-media',task_id.id)


    dict={
        'users':users,
        'is_hr':is_Hr(request.user),
    }
    return render(request,'tasks/task_create.html',context=dict)

@login_required(login_url='adminlogin')
def add_media(request,slug):
    task_id = get_object_or_404(models.Task,id=slug)
    form=forms.taskmediaForm()
    if task_id.created_by==request.user:
        mode='assign'
        go='mytask'
    else:
        mode='reply'
        go='assignedtask'
    if task_id.created_by==request.user or task_id.assigned_to==request.user:
        if request.method=="POST":
            form=forms.taskmediaForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.task_id=task_id
                form.instance.description=request.POST.get('desc')
                form.instance.media_mode=mode
                f=form.save()
                f.save()

                return redirect('add-media',task_id.id)
        dict={
            'slug':slug,
            'form':form,
            'is_hr':is_Hr(request.user),
            'checkuser':go
        }
        return render(request,'tasks/add_media_page.html',context=dict)
    else:
        return HttpResponse('you are not allowed')

@login_required(login_url='adminlogin')
def task_detail(request,slug):
    assigned_media=[]
    responsed_media=[]
    task = get_object_or_404(models.Task,id=slug)
    rel_media = models.Task_Media.objects.filter(task_id=task.id,)
    task_cmt = models.Task_Comment.objects.filter(task_id=task.id)
    noti = models.Notifications.objects.filter(assigned_to=request.user,is_seen=False,task_id=task)
    for i in noti:
        notification_seen = get_object_or_404(models.Notifications,id=i.id)
        notification_seen.is_seen = True
        notification_seen.save()
    if task.created_by==request.user:
        go='mytask'
    else:
        go='assignedtask'
    if task.created_by==request.user or task.assigned_to==request.user:
        for i in rel_media:
            if i.media_mode == 'assign':
                assigned_media.append(i)
            else:
                responsed_media.append(i)
        if task.created_by==request.user:
            if request.method == 'POST':
                comment = request.POST.get('comment')


                models.Task_Comment.objects.create(task_id=task,comment=comment,user=request.user)
                if comment:
                    if task.created_by == request.user:
                        noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=task.assigned_to,type="task_comment",task_id=task)
                    else:
                        noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=task.created_by,type="task_comment",task_id=task)
            dict={
                'is_hr':is_Hr(request.user),
                'task':task,
                'assigned_media':assigned_media,
                'responsed_media':responsed_media,
                'currentuser':True,
                'task_cmt':task_cmt,
                'checkuser':go
            }
            return render(request,'tasks/task_detail.html',context=dict)
        else:
            if request.method=='POST':
                status = request.POST.get('status')
                completed = request.POST.get('Task')
                print(completed)
                comment = request.POST.get('comment')
                task.status = status
                task.completed =completed
                task.save()
                models.Task_Comment.objects.create(task_id=task,comment=comment,user=request.user)
                if comment:
                    if task.created_by == request.user:
                        noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=task.assigned_to,type="task_comment",task_id=task)
                    else:
                        noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=task.created_by,type="task_comment",task_id=task)
                if completed == "True":
                    noti = models.Notifications.objects.create(assigned_by=request.user,assigned_to=task.created_by,type="task_complete",task_id=task)
            dict={
                'is_hr':is_Hr(request.user),
                'task':task,
                'assigned_media':assigned_media,
                'responsed_media':responsed_media,
                'currentuser':False,
                'task_cmt':task_cmt
            }
            return render(request,'tasks/task_detail.html',context=dict)
    else:
        return HttpResponse("you are not allow here")

@login_required(login_url='adminlogin')
def assigned_task(request):
    tasks = models.Task.objects.filter(assigned_to=request.user).order_by('-id')
    dict={
        'is_hr':is_Hr(request.user),
        'tasks':tasks
    }
    return render(request,'tasks/assigned_task_view.html',context=dict)
@login_required(login_url='adminlogin')
def edit_task_list(request):
    tasks = models.Task.objects.filter(created_by=request.user).order_by('-id')
    dict={
        'tasks':tasks,
        'is_hr':is_Hr(request.user),
    }
    return render(request,'tasks/edit_task_list.html',context=dict)


@login_required(login_url='adminlogin')
def Edit_task(request,slug):
    task = get_object_or_404(models.Task,id=slug)
    user = models.User.objects.filter()
    users1=[]
    users2=[]
    for i in user:
        if i!=request.user:
            if i.groups.filter(name="EMPLOYEE").exists():
                users1.append(i)
            elif i.groups.filter(name="HR").exists():
                users2.append(i)

    users=[]
    users=users1+users2
    if request.user == task.created_by or request.user == task.assigned_to:

        if request.method=='POST':
            task_sub = request.POST.get('subject')
            task_detail = request.POST.get('details')
            assigned_to = request.POST.get('assigned')
            usr = get_object_or_404(models.User,username=assigned_to)
            created_by=request.user
            due_date = request.POST.get('duedate')

            task.task_subject = task_sub
            task.task_detail=task_detail
            if due_date:
                task.due_date = due_date
            task.assigned_to = usr
            task.save()



        mydict = {
            'task':task,
            'users':users
        }

        return render(request,'tasks/task_edit.html',context=mydict)
    else:

        return HttpResponse("you are not allow here")
