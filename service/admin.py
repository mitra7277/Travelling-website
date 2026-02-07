from django.contrib import admin
from .models import Service, ContactMessage

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_icon', 'service_title', 'service_des')
    

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

admin.site.register(Service, ServiceAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)

