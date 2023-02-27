from django.contrib import admin
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'parent')


admin.site.register(Menu, MenuAdmin)
