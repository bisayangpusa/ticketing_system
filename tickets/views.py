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
        # Store old values for comparison
        old_values = {
            'worker': ticket.current_worker,
            'next_step': ticket.next_step,
            'impact': ticket.business_impact,
            'status': ticket.status,
            'urgency': ticket.urgency,
            'desc': ticket.description
        }
        
        form = TicketUpdateForm(request.POST, instance=ticket)
        
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            updated_ticket.update_count += 1
            updated_ticket.save()

            # Build detailed changes list
            changes_list = []
            if old_values['worker'] != updated_ticket.current_worker:
                changes_list.append(f"Worker: {updated_ticket.current_worker}")
            
            if old_values['next_step'] != updated_ticket.next_step:
                changes_list.append(f"Next Step: {updated_ticket.next_step}")

            if old_values['impact'] != updated_ticket.business_impact:
                changes_list.append(f"Impact: {updated_ticket.business_impact}")

            if old_values['status'] != updated_ticket.status:
                changes_list.append(f"Status: {updated_ticket.get_status_display()}")

            if old_values['urgency'] != updated_ticket.urgency:
                changes_list.append(f"Urgency: {updated_ticket.urgency}")

            if old_values['desc'] != updated_ticket.description:
                changes_list.append("Description updated")
            
            # Fallback if nothing specific changed
            if not changes_list:
                changes_list.append("General details updated")

            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                changes="\n".join(changes_list) # Changed " | " to "\n"
            )
                
            return redirect('dashboard')
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})