from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # Change 'name' to 'title' and remove 'issue' (since title covers it)
        fields = ['title', 'status', 'urgency', 'description']