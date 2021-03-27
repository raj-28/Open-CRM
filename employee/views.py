import datetime

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
    # patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    # appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    # patientid=[]
    # for a in appointments:
    #     patientid.append(a.patientId)
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    # appointments=zip(appointments,patients)
    mydict={
    'employee':employee,
    'deactivated_employee':deactivated_employee,
    # 'patientdischarged':patientdischarged,
    # 'appointments':appointments,
    # 'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    # return render(request,'hospital/doctor_dashboard.html',context=mydict)
    return render(request,'hr_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
def hr_profile(request,slug):
    user=get_object_or_404(models.User,username=slug)
    if is_Hr(request.user):
        if is_Hr(user):
            personal_info=get_object_or_404(models.Hr,user=request.user)
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

    return render(request,'hr_view_employee.html',{'employees':employee,})

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_view_attendance(request):

    return render(request,'attendance_card.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_add_attendance(request):
    today = timezone.now().today().date()
    hrattend=models.Hr_Attendance.objects.filter(attendance_date=today,user=request.user)
    hrattend2=models.Hr_Attendance.objects.filter(user=request.user).order_by('-attendance_date')
    hrlist=[]
    for i in hrattend2:
        if i.attendance_date==today:
            print("hello")
        elif i.attendance_date<today:
            hrlist.append(i)
    #if attendannce object is not create then 1st create and then go ahead
    if not hrattend:
        obj=models.Hr_Attendance.objects.create(user=request.user,attendance_date=today)
        hrattend=models.Hr_Attendance.objects.filter(attendance_date=today,user=request.user)
        # empattend2=models.Attendance.objects.filter(user=request.user)

        mydict={
            'todayattend':hrattend,
            'hrattends':hrlist,
            'today':today
        }
        return render(request,'hr_view_attendance.html',context=mydict)
    else:
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
        'allempattndnc':atendlist
    }
    return render(request,'hr_approved_employee_attendance.html',context=dict)

@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def hr_approved(request,slug):
    today = timezone.now().today().date()
    date=slug.split('_')
    mydate=date[1]
    userid=date[0]
    print(date)
    if today==mydate:
        empattendance=models.Attendance.objects.filter(attendance_date=today)
        obj=get_object_or_404(models.Attendance,user=userid,attendance_date=today)
        obj.approved=True
        obj.save()
    else:
        obj=get_object_or_404(models.Attendance,user=userid,attendance_date=mydate)
        obj.approved=True
        obj.save()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    username=get_object_or_404(models.User,id=userid)
    getobj=models.Attendance.objects.filter(user=userid,attendance_date=tomorrow)
    if not getobj:
        obj=models.Attendance.objects.create(user=username,attendance_date=tomorrow)
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


#---------------------------------------------------------------------------------
#------------------------ EMPLOYEE RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_Employee)
def employee_dashboard_view(request):
    # patient=models.Employee.objects.get(user_id=request.user.id)
    # doctor=models.Hr.objects.get(user_id=patient.assignedDoctorId)
    # mydict={
    # 'patient':patient,
    # 'doctorName':doctor.get_name,
    # 'doctorMobile':doctor.mobile,
    # 'doctorAddress':doctor.address,
    # 'symptoms':patient.symptoms,
    # 'doctorDepartment':doctor.department,
    # 'admitDate':patient.admitDate,
    # }
    # return render(request,'hospital/patient_dashboard.html',context=mydict)
    return render(request,'employee_dashboard.html')

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
    print(today)
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
        obj=models.Attendance.objects.create(user=request.user,attendance_date=today)
        empattend=models.Attendance.objects.filter(attendance_date=today,user=request.user)
        # empattend2=models.Attendance.objects.filter(user=request.user)

        mydict={
            'todayattend':empattend,
            'empattends':emplist,
            'today':today
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

        obj.present=True
        obj.save()
        return redirect('employee-attendance')
    elif is_Hr(request.user):
        today = timezone.now().today().date()
        obj=get_object_or_404(models.Hr_Attendance,attendance_date=today,user=request.user)
        obj.end_time=timezone.now().time()
        obj.approved=True

        obj.present=True
        obj.save()
        return redirect('hr-add-attendance')
@login_required(login_url='adminlogin')
@user_passes_test(is_Hr)
def employee_absent(request,slug):
    today = timezone.now().today().date()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
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