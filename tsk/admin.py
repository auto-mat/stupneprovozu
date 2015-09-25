# -*- coding: utf-8 -*-

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Lokace, Provoz, SkupinaLokaci

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


class WeekDayFilter(SimpleListFilter):
    title = "Den v týdnu"
    parameter_name = "weekday"

    def lookups(self, request, model_admin):
        list_tuple = []
        for location in Lokace.objects.filter(favourite=True):
            list_tuple.append((location.id, location.name))
        return [
            ('vsedni', 'Všední den'),
            ('vikend', 'Víkend'),
            ('pondeli', 'Pondělí'),
            ('utery', 'Úterý'),
            ('streda', 'Středa'),
            ('ctvrtek', 'Čtvrtek'),
            ('patek', 'Pátek'),
            ('sobota', 'Sobota'),
            ('nedele', 'Neděle'),
            ]


    def queryset(self, request, queryset):
        if self.value() == 'vsedni':
            return queryset.exclude(Q(time_start__week_day=1) | Q(time_start__week_day=7))
        elif self.value() == 'vikend':
            return queryset.filter(Q(time_start__week_day=1) | Q(time_start__week_day=7))
        elif self.value() == 'pondeli':
            return queryset.filter(time_start__week_day=2)
        elif self.value() == 'utery':
            return queryset.filter(time_start__week_day=3)
        elif self.value() == 'streda':
            return queryset.filter(time_start__week_day=4)
        elif self.value() == 'ctvrtek':
            return queryset.filter(time_start__week_day=5)
        elif self.value() == 'patek':
            return queryset.filter(time_start__week_day=6)
        elif self.value() == 'sobota':
            return queryset.filter(time_start__week_day=7)
        elif self.value() == 'nedele':
            return queryset.filter(time_start__week_day=1)
        else:
            return queryset

def show_levels(modeladmin, request, queryset):
    levels = dict(queryset.values('level').annotate(level_count = Count('id')).order_by().values_list('level', 'level_count'))
    count = queryset.count()
    level4 = levels[4] if 4 in levels else 0
    level5 = levels[5] if 5 in levels else 0
    congest_rate = (float(level4 + level5) / count) * 100.0
    modeladmin.message_user(request, mark_safe("Stupně provozu: %s<br/>Počet: %s<br/>Podíl zácpy: %.2f%%" % (levels, count, congest_rate)))
show_levels.short_description = "Ukázat stupně provozu"


class ProvozAdmin(ImportExportModelAdmin):
    list_display = ('location', 'level', 'time_generated', 'time_start', 'time_stop')
    list_filter = (TimeFilter, ('time_start', DateRangeFilter), 'level', 'location__favourite', WeekDayFilter, LocationFilter, 'location__skupinalokaci__name')
    search_fields = ('location__name',)
    actions = (show_levels,)


class LokaceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'favourite',)
    search_fields = ('name',)
    list_filter = ('favourite',)


class SkupinaLokaciAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('lokace',)


admin.site.register(SkupinaLokaci, SkupinaLokaciAdmin)
admin.site.register(Lokace, LokaceAdmin)
admin.site.register(Provoz, ProvozAdmin)
