from django.contrib import admin
from .models import User
from guardian.admin import GuardedModelAdmin


@admin.register(User)
class UserAdmin(GuardedModelAdmin):
    pass


# admin.site.register(User)
