from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Ticket, TicketHistory
from .forms import TicketForm, TicketUpdateForm


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Check if the user wants to see completed tickets
    show_completed = request.GET.get('show_completed') == 'true'
    query = request.GET.get('q', '')
    
    # Base queryset: Order by newest first
    tickets = Ticket.objects.all().order_by('-created_at')
    
    # NEW: Hide completed tickets by default
    if not show_completed:
        tickets = tickets.filter(is_completed=False)
    
    # Keep your existing search logic
    if query:
        tickets = tickets.filter(
            Q(title__icontains=query) | 
            Q(ticket_id__icontains=query) |
            Q(description__icontains=query)
        )

    # Keep your existing POST logic for creating tickets
    if request.method == 'POST':
        Ticket.objects.create(
            title=request.POST.get('title'), 
            description=request.POST.get('description'),
            urgency=request.POST.get('urgency'),
            creator=request.user
        )
        return redirect('dashboard')

    return render(request, 'dashboard.html', {
        'tickets': tickets, 
        'query': query,
        'show_completed': show_completed  # Pass this to the template
    })



@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        old_desc = ticket.description
        old_status = ticket.status
        
        form = TicketUpdateForm(request.POST, instance=ticket)
        
        if form.is_valid():
            # 1. Save the form first to get the new data
            updated_ticket = form.save(commit=False)
            
            # 2. Increment the count
            updated_ticket.update_count += 1
            updated_ticket.save()

            # 3. Build the changes list
            changes_list = []
            if old_desc != updated_ticket.description:
                changes_list.append("Description updated")
            if old_status != updated_ticket.status:
                changes_list.append(f"Status: {updated_ticket.status}")
            
            # If no specific desc/status changed, add a general label
            if not changes_list:
                changes_list.append("Ticket details/worker updated")

            # 4. ALWAYS create a history record if the form was saved
            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                changes=" | ".join(changes_list)
            )
                
            return redirect('dashboard')
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})