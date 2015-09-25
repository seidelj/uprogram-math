from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from mathtutor.models import Student

# Register your models here.

class StudentInline(admin.TabularInline):
    model = Student

class UserAdmin(OriginalUserAdmin):
    inlines = [StudentInline,]

try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, UserAdmin)
