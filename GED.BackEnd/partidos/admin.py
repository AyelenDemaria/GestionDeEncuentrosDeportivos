from django.contrib import admin
from .models import Partido

# Register your models here.
admin.site.register(Partido)

"""class MyAdminView(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)"""
