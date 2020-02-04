from django.contrib import admin

from .models import User, Favourite


admin.site.register(User)
admin.site.register(Favourite)
