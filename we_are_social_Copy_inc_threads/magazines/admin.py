from django.contrib import admin
from .models import Magazine
from .models import Purchase

# Register your models here so they can be used in the admin.
admin.site.register(Magazine)
admin.site.register(Purchase)
