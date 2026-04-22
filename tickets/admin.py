from django.contrib import admin
from .models import Ticket, TicketHistory

admin.site.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # This shows these columns in the main list view
    list_display = ('ticket_id', 'title', 'status', 'urgency', 'creator', 'created_at')
    
    # This allows you to filter by status or date in the right sidebar
    list_filter = ('status', 'urgency', 'created_at')
    
    # This makes the created_at field appear in the edit form so you can change it
    fields = ('title', 'creator', 'status', 'urgency', 'description', 'current_worker', 'next_step', 'business_impact', 'is_completed', 'update_count', 'created_at')


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user','changes', 'timestamp')