# core/tasks.py
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from core.utilss.escalation_constants import ESCALATION_TIME_LIMITS
from core.utilss.escalation_rules import escalate_ticket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.models import Ticket

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def run_auto_escalation(self):
    """
    Periodic task that escalates tickets automatically based on
    priority and creation time thresholds.
    """
    now = timezone.now()
    tickets = Ticket.objects.filter(status__in=['open', 'in_progress'])

    print(f"Found {tickets.count()} tickets to process.")
    print(f"Running auto escalation task at {timezone.now()}")

    for t in tickets:
        print(f"Processing Ticket ID: {t.id}, Priority: {t.priority}, Created At: {t.created_at}")
        if not t.priority or not t.created_at:
            print(f"Skipping Ticket ID: {t.id} - Missing Priority or Created At")
            continue

        # Process critical priority tickets
        if t.priority.lower() == 'critical':
            with transaction.atomic():
                t.refresh_from_db()
                escalate_ticket(t)
                send_escalation_notification(t)
            continue

        # Process other tickets based on threshold
        threshold_hours = ESCALATION_TIME_LIMITS.get(t.priority.lower())
        if not threshold_hours:
            print(f"Ticket ID: {t.id}, Threshold for {t.priority} is {threshold_hours} hours")
            continue

        if now - t.created_at > timedelta(hours=threshold_hours):
            print(f"Ticket ID: {t.id} exceeds threshold, escalating now")
            try:
                with transaction.atomic():
                    t.refresh_from_db()
                    escalate_ticket(t)
                    send_escalation_notification(t)
            except Exception as e:
                print(f"Error escalating Ticket ID: {t.id} - {str(e)}")


def send_escalation_notification(ticket):
    """
    Send a WebSocket notification to notify users about ticket escalation.
    """
    channel_layer = get_channel_layer()

    # Prepare the message data
    message = {
        "ticket_id": ticket.id,
        "title": ticket.title,
        "priority": ticket.priority,
        "escalated_at": ticket.escalated_at.strftime("%Y-%m-%d %H:%M") if ticket.escalated_at else "",
    }

    # Broadcast the escalation message to the WebSocket group
    async_to_sync(channel_layer.group_send)(
        "escalations",  # Group name
        {
            "type": "escalation_message",
            "message": message
        }
    )