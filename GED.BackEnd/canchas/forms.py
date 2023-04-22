from django import forms
from datetime import date

class ReporteMesAnio(forms.Form):
    y = int(date.today().year)
    y1 = y - 1
    y2 = y - 2
    year_selection = (
        (y, y),
        (y1, y1),
        (y2, y2),
    )

    months_selection = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')
    )

    anio = forms.ChoiceField(label="Seleccione año", choices=year_selection)
    mes = forms.ChoiceField(label="Seleccione mes", choices=months_selection)


class ReporteAnio(forms.Form):
    y = int(date.today().year)
    y1 = y - 1
    y2 = y - 2
    year_selection = (
        (y, y),
        (y1, y1),
        (y2, y2),
    )

    anio = forms.ChoiceField(label="Seleccione año", choices=year_selection)
