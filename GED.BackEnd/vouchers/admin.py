from django.contrib import admin
from .models import Voucher
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateRangeFilterBuilder

# Register your models here.

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_canje', 'fecha_emision', 'fecha_vencimiento', 'jugador','cancha','codigo')
    search_fields = ('jugador__user__first_name', 'cancha__cancha__nombre','cancha__cancha__deporte__descripcion','codigo')
    list_filter = (
        ('cancha__cancha', RelatedDropdownFilter),
        ('jugador', RelatedDropdownFilter),
        ("fecha_canje", DateRangeFilterBuilder(title="Fecha de canje")),
        ("fecha_emision", DateRangeFilterBuilder(title="Fecha de emisión")),
        ("fecha_canje", admin.EmptyFieldListFilter)

    )
admin.site.register(Voucher, VoucherAdmin)
