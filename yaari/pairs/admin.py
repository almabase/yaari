from django.contrib import admin

from .models import Team, Employee, Pair, PairCall

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'availability')
    list_filter = ('team', 'availability')

class PairAdmin(admin.ModelAdmin):
    list_display = ('employee_one', 'employee_two')

class PairCallAdmin(admin.ModelAdmin):
    list_display = ('pair', 'is_done', 'date')
    list_filter = ('is_done', 'date')

admin.site.register(Team)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(PairCall, PairCallAdmin)
from django.contrib import admin

# Register your models here.
