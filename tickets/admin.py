from django.contrib import admin
from .models import Ticket, TicketHistory

admin.site.register(Ticket)

@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user','changes', 'timestamp')