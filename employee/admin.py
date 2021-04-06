from django.contrib import admin
from .models import Hr,Employee,Persional_Info,Bank_Info,Education_Info, Attendance, Hr_Attendance,Task,Task_Media, Task_Comment

# Register your models here.
class HrAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hr, HrAdmin)
class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employee, EmployeeAdmin)

class PersionalinfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Persional_Info, PersionalinfoAdmin)

class Bank_InfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bank_Info, Bank_InfoAdmin)

class Education_InfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Education_Info, Education_InfoAdmin)

class Attendance_InfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, Attendance_InfoAdmin)

class Hr_Attendance_InfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Hr_Attendance, Hr_Attendance_InfoAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task, TaskAdmin)

class TaskMediaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task_Media, TaskMediaAdmin)

class TaskCommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task_Comment, TaskCommentAdmin)
