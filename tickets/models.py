import uuid
from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES = [('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')]
    URGENCY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]

    # 2d. UUID (Automatically created)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # 2a. Ticket Name
    title = models.CharField(max_length=200) 
    # 2b. Creator (Automatically noted from logged-in user)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    #email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='MEDIUM')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.ticket_id} - {self.title}"

# 2c. History and Time Logs
class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changes = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True)