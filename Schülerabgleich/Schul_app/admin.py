from django.contrib import admin
from .models import Student, Teacher, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matrikelnummer', 'user', 'klasse', 'telefon')
    search_fields = ('matrikelnummer', 'user__first_name', 'user__last_name')
    list_filter = ('klasse', 'created_at')

admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('personalnummer', 'user', 'fachbereich', 'zimmer')
    search_fields = ('personalnummer', 'user__first_name', 'user__last_name')
    list_filter = ('klasse', 'created_at')

admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('datum', 'student', 'teacher', 'anwesend')
    list_filter = ('datum', 'anwesend')
    date_hierarchy = 'datum'
