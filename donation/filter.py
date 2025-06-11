from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class DateRangeFilter(admin.SimpleListFilter):
    title = _('Período')
    parameter_name = None  # definir em subclasses
    template = 'admin/date_range_filter.html'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.value_display = request.GET.get(self.parameter_name, "")
        self.request = request  # armazenar para usar em queryset()

    def lookups(self, request, model_admin):
        return [("-", "-")]

    def choices(self, changelist):
        yield {
            'selected': False,
            'query_parts': changelist.get_filters_params(),
        }

    def queryset(self, request, queryset):
        raw = request.GET.get(self.parameter_name)
        if raw:
            try:
                start_str, end_str = raw.split(' - ')
                start_date = datetime.strptime(start_str.strip(), '%d/%m/%Y')
                end_date = datetime.strptime(end_str.strip(), '%d/%m/%Y')

                if start_date > end_date:
                    messages.error(self.request, _("A data inicial não pode ser maior que a final."))
                    return queryset.none()  # ou return queryset se quiser ignorar silenciosamente

                return queryset.filter(**{
                    f"{self.parameter_name}__range": (start_date, end_date)
                })
            except ValueError:
                messages.warning(self.request, _("Período inválido. Formato esperado: DD/MM/AAAA - DD/MM/AAAA"))

        return queryset
