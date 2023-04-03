from django.contrib import admin
from marketing.models import SubscribedEmail

@admin.register(SubscribedEmail)
class SubscribedEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp']