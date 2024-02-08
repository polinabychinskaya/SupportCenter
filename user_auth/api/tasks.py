from celery import shared_task
from django.core.mail import send_mail
from project import settings
from user_auth.models import Tickets
from datetime import datetime, timedelta

@shared_task
def email_by_completion(to_email):
    mail_subject = 'Ticket'
    message = 'Your ticket has been processed. Check your personal page for additional information.'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False
    )
    return 'Done'

@shared_task
def delete_by_completion():
    tickets_queryset = Tickets.objects.filter(status='Done')
    tickets_queryset.delete()
    return None

@shared_task
def email_reminder():
    tickets_queryset = Tickets.objects.filter(status='New').select_related('supporter__user')
    for ticket in tickets_queryset:
        time_passed = datetime.now() - ticket.created_at.replace(tzinfo=None)
        difference = timedelta(hours=1)
        if time_passed.total_seconds() > difference.total_seconds():
            mail_subject = 'Ticket'
            message = f'The ticket #{ticket.pk} is waiting for you to respond.'
            to_email = ticket.supporter.user.email
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False)
    return None