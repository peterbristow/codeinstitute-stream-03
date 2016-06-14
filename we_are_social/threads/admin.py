from django.contrib import admin
from .models import Subject, Thread, Posts


# Register your models here.
admin.site.register(Subject)
admin.site.register(Thread)
admin.site.register(Posts)
