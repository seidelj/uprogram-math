from django.contrib import admin
from django.contrib.auth.models import User, Student
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from mathtutor.models import Student

# Register your models here.

class StudentInline(admin.TabularInline):
    model = Student

class UserAdmin(OriginalUserAdmin):
    inlines = [StudentInline,]

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('get_username', "quizzes_passed")
    list_display = ('stuid', 'quizzes_passed')
    search_fields = ['stuid__username']
    def get_username(self, obj):
        return obj.stuid.username
    def quizzes_passed(self, obj):
        return obj.get_quiz_info()['passed']

admin.site.register(Student, StudentAdmin)

try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, UserAdmin)
