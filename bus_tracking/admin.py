
from django.contrib import admin
from .models import User, Bus, Student, DriverInfo, Attendance, BusLocation

admin.site.register(User)
admin.site.register(Bus)
admin.site.register(Student)
admin.site.register(DriverInfo)
admin.site.register(Attendance)
admin.site.register(BusLocation)
