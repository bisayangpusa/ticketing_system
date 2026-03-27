from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'status', 'urgency', 'description']

# --- NEW FORM ---
class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'current_worker', 
            'next_step', 
            'business_impact', 
            'status', 
            'urgency', 
            'description', 
            'is_completed'
        ]
        widgets = {
            'next_step': forms.Textarea(attrs={'rows': 2}),
            'business_impact': forms.Textarea(attrs={'rows': 2}),
        }