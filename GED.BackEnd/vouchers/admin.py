from django.contrib import admin
from .models import Voucher

# Register your models here.

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_canje', 'fecha_emision', 'fecha_vencimiento', 'jugador','cancha')
    list_filter = ('cancha', 'jugador','fecha_emision','fecha_canje')

admin.site.register(Voucher, VoucherAdmin)
