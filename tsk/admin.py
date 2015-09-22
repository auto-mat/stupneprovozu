# -*- coding: utf-8 -*-

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


class ProvozAdmin(admin.ModelAdmin):
    list_display = ('location', 'level', 'time_generated',)
    list_filter = (LocationFilter,)


class LokaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'favourite',)
    list_filter = ('favourite',)

admin.site.register(Lokace, LokaceAdmin)
admin.site.register(Provoz, ProvozAdmin)
