"""employeemanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# noinspection PyUnresolvedReferences
from employee import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminsignup', views.admin_signup_view),
    path('', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('logout', LogoutView.as_view(next_page='adminlogin'),name='logout'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-hr', views.admin_hr_view,name='admin-hr'),
    path('admin-add-hr', views.admin_add_hr_view,name='admin-add-hr'),


    path('hr-dashboard', views.hr_dashboard_view,name='hr-dashboard'),
    path('profile/<slug:slug>/', views.hr_profile,name='profile'),
    path('hr-employee', views.hr_employee_view,name='hr-employee'),
    path('hr-add-employee', views.hr_add_employee_view,name='hr-add-employee'),
    path('hr-view-employee/', views.hr_view_employee_view,name='hr-view-employee'),
    path('hr-attendance/', views.hr_view_attendance,name='hr-attendance'),
    path('hr_attendance/', views.hr_add_attendance,name='hr-add-attendance'),
    path('hr-view-attendance/', views.hr_view_employee_attendance,name='hr-view-attendance'),
    path('hr-approved/<slug:slug>/', views.hr_approved,name='hr-approved'),
    path('hr-unapproved/<slug:slug>/', views.hr_unapproved,name='hr-unapproved'),


    path('employee-dashboard/', views.employee_dashboard_view,name='employee-dashboard'),
    # path('profile/', views.employee_profile,name='employee-profile'),
    path('attendance/', views.employee_attendance,name='employee-attendance'),
    path('start-session/', views.start_session,name='start-session'),
    path('end-session/', views.end_session,name='end-session'),
    path('employee-absent/<slug:slug>/', views.employee_absent,name='employee_absent'),



    #edit profile portion

    path('edit-company-info/', views.edit_company_info,name='edit_company_info'),
    path('edit-personal-info/', views.edit_personal_info,name='edit_personal_info'),
    path('edit-education-info/', views.edit_education_info,name='edit_education_info'),
    path('edit-bank-info/', views.edit_bank_info,name='edit_bank_info'),


]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
