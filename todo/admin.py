from django.contrib import admin
from .models import Todo, Category
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.register(Todo)

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
