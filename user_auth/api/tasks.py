from celery import shared_task
from django.core.mail import send_mail
from project import settings
from user_auth.models import Tickets

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