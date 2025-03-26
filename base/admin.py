from django.contrib import admin
from .models import GuestEntry
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry



@admin.register(GuestEntry)
class GuestEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  # Columns in the admin panel
    search_fields = ('name', 'email', 'message')  # Search bar fields
    list_filter = ('created_at',)  # Filter by date
    ordering = ('-created_at',)  # Latest messages first

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Message Management"
admin.site.index_title = "Manage Guest Messages"



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    list_display = ('user', 'action_time', 'content_type', 'object_repr', 'change_message')
