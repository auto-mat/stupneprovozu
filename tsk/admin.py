# -*- coding: utf-8 -*-

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Lokace, Provoz

class LocationFilter(SimpleListFilter):
    title = "Lokace"
    parameter_name = "locations"

    def lookups(self, request, model_admin):
        list_tuple = []
        for location in Lokace.objects.filter(favourite=True):
            list_tuple.append((location.id, location.name))
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(location__id=self.value())
        else:
            return queryset


class TimeFilter(SimpleListFilter):
    title = "Časové období"
    parameter_name = "time"

    def lookups(self, request, model_admin):
        list_tuple = []
        for location in Lokace.objects.filter(favourite=True):
            list_tuple.append((location.id, location.name))
        return [
            ('rano', 'ráno (8-9)'),
            ('odpoledne', 'odpoledne (17-18)'),
            ]


    def queryset(self, request, queryset):
        if self.value() == 'rano':
            return queryset.filter(time_start__hour=8)
        elif self.value() == 'odpoledne':
            return queryset.filter(time_start__hour=17)
        else:
            return queryset


class ProvozAdmin(admin.ModelAdmin):
    list_display = ('location', 'level', 'time_generated', 'time_start', 'time_stop')
    list_filter = (LocationFilter, TimeFilter, ('time_start', DateRangeFilter))


class LokaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'favourite',)
    list_filter = ('favourite',)

admin.site.register(Lokace, LokaceAdmin)
admin.site.register(Provoz, ProvozAdmin)
