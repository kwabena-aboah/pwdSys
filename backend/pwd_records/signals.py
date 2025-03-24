from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PWDRecord
from auditlog.registry import auditlog

@receiver(post_save, sender=PWDRecord)
def create_update_audit_log(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    # In a real scenario, capture the request user via middleware or context.
    auditlog.objects.create(
        user=None,  # Replace with actual user info if available
        action=action,
        record=instance,
        details=f"Record {action} at {instance.updated_at}"
    )

@receiver(post_delete, sender=PWDRecord)
def delete_audit_log(sender, instance, **kwargs):
    auditlog.objects.create(
        user=None,
        action='DELETE',
        record=instance,
        details="Record deleted"
    )
