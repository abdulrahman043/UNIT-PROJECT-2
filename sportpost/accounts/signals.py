from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Notification

@receiver(post_save, sender=Post)
def notify_on_reply(sender, instance, created, **kwargs):
    if created and instance.parent_post:
        parent_owner = instance.parent_post.user
        if parent_owner != instance.user:
           Notification.objects.create(
            receiver=parent_owner,
            sent=instance.user,
            reply=instance
        )
    
