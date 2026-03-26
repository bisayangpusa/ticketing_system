from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Ticket, TicketHistory
from .forms import TicketForm


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    urgency_filter = request.GET.get('urgency', '')
    status_filter = request.GET.get('status', '')

    tickets = Ticket.objects.all().order_by('-created_at')
    
    # Text Search (Title, UUID, Description)
    if query:
        tickets = tickets.filter(
            Q(title__icontains=query) | 
            Q(ticket_id__icontains=query) |
            Q(description__icontains=query)
        )

    # Specific Dropdown Filters
    if urgency_filter:
        tickets = tickets.filter(urgency=urgency_filter)
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    return render(request, 'dashboard.html', {
        'tickets': tickets, 
        'query': query,
        'urgency_filter': urgency_filter,
        'status_filter': status_filter
    })
   
@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        old_desc = ticket.description
        new_desc = request.POST.get('description')
        new_status = request.POST.get('status')
        
        # Determine what changed for the log
        changes_list = []
        if old_desc != new_desc:
            changes_list.append(f"Description changed from '{old_desc[:30]}...' to '{new_desc[:30]}...'")
        if ticket.status != new_status:
            changes_list.append(f"Status changed to {new_status}")

        ticket.description = new_desc
        ticket.status = new_status
        ticket.urgency = request.POST.get('urgency')
        ticket.save()

        if changes_list:
            TicketHistory.objects.create(
                ticket=ticket,
                user=request.user,
                changes=" | ".join(changes_list)
            )
        return redirect('dashboard')

    return render(request, 'edit_ticket.html', {'ticket': ticket})