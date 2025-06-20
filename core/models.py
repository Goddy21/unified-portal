from django.db import models
from django.contrib.auth.models import User

# File Management Models
class FileCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/files/')
    category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    access_level = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('operator', 'Operator')])

    def __str__(self):
        return self.title

class FileAccessLog(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    accessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access_time = models.DateTimeField(auto_now_add=True)

# Ticketing System Models
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='created_tickets', on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commented_by} on {self.ticket}"
