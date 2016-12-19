from django.contrib import admin

from .models import Team, Employee, Pair, PairCall, TimeLapse

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'availability')
    list_editable = ('name', 'availability')
    list_filter = ('team', 'availability')

class PairAdmin(admin.ModelAdmin):
    list_display = ('employee_one', 'employee_two')

class PairCallAdmin(admin.ModelAdmin):
    list_display = ('pair', 'is_done', 'date')
    list_filter = ('is_done', 'date')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_editable = ('name',)

class TimeLapseAdmin(admin.ModelAdmin):
    list_display = ('primary_employee', 'secondary_employee', 'is_same_team', 'time_lapse_in_days')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(PairCall, PairCallAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TimeLapse, TimeLapseAdmin)
from django.contrib import admin

# Register your models here.
