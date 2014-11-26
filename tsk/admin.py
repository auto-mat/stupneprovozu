from django.contrib import admin

from .models import Lokace, Provoz

class ProvozAdmin(admin.ModelAdmin):
    list_display = ('location', 'level', 'time_generated',)
    list_filter = ('location',)

admin.site.register(Lokace)
admin.site.register(Provoz, ProvozAdmin)
