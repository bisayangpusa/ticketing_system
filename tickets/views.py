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
        # Store ALL old values before the form overwrites them
        old_values = {
            'description': ticket.description,
            'status': ticket.status,
            'worker': ticket.current_worker,
            'next_step': ticket.next_step,
            'impact': ticket.business_impact,
        }
        
        form = TicketUpdateForm(request.POST, instance=ticket)
        
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            updated_ticket.update_count += 1
            updated_ticket.save()

            changes_list = []
            
            # Compare and capture the NEW values
            if old_values['worker'] != updated_ticket.current_worker:
                changes_list.append(f"Worker: {updated_ticket.current_worker}")
            
            

            if old_values['impact'] != updated_ticket.business_impact:
                changes_list.append(f"\nImpact: {updated_ticket.business_impact}")

            if old_values['status'] != updated_ticket.status:
                changes_list.append(f"\nStatus: {updated_ticket.status}")

            if old_values['description'] != updated_ticket.description:
                # This shows the actual new description text
                changes_list.append(f"\n{updated_ticket.description}")
            
            if not changes_list:
                changes_list.append("No visible changes made")

            if old_values['next_step'] != updated_ticket.next_step:
                changes_list.append(f"\nNext Step: {updated_ticket.next_step}")

            # Save with NEWLINE (\n) so it displays as a list in the template
            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                changes="\n".join(changes_list)
            )
                
            return redirect('edit_ticket', pk=ticket.pk)
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})