from django.contrib import admin

# Register your models here.
from biz.models import *


class BusinessAdmin(admin.ModelAdmin):
    readonly_fields=('cached',)

admin.site.register(Business, BusinessAdmin)