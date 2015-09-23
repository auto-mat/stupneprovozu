# -*- coding: utf-8 -*-

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.utils.safestring import mark_safe
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

def show_levels(modeladmin, request, queryset):
    levels = dict(queryset.values('level').annotate(level_count = Count('id')).order_by().values_list('level', 'level_count'))
    count = queryset.count()
    level4 = levels[4] if 4 in levels else 0
    level5 = levels[5] if 5 in levels else 0
    congest_rate = (float(level4 + level5) / count) * 100.0
    modeladmin.message_user(request, mark_safe("Stupně provozu: %s<br/>Počet: %s<br/>Podíl zácpy: %.2f%%" % (levels, count, congest_rate)))
show_levels.short_description = "Ukázat stupně provozu"


class ProvozAdmin(admin.ModelAdmin):
    list_display = ('location', 'level', 'time_generated', 'time_start', 'time_stop')
    list_filter = (LocationFilter, TimeFilter, ('time_start', DateRangeFilter), 'level')
    search_fields = ('location__name',)
    actions = (show_levels,)


class LokaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'favourite',)
    search_fields = ('name',)
    list_filter = ('favourite',)

admin.site.register(Lokace, LokaceAdmin)
admin.site.register(Provoz, ProvozAdmin)
