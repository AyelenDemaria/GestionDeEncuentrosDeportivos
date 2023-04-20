from django.contrib import admin
from .models import Voucher
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateRangeFilterBuilder

# Register your models here.

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_canje', 'fecha_emision', 'fecha_vencimiento', 'jugador','cancha')
    search_fields = ('jugador__user__first_name', 'cancha__nombre','cancha__deporte__descripcion')
    list_filter = (
        ('cancha', RelatedDropdownFilter),
        ('jugador', RelatedDropdownFilter),
        ("fecha_canje", DateRangeFilterBuilder(title="Fecha de canje")),
        ("fecha_emision", DateRangeFilterBuilder(title="Fecha de emisión")),
    )
admin.site.register(Voucher, VoucherAdmin)
