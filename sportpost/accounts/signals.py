from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Notification,Like
from accounts.models import Follow
@receiver(post_save, sender=Post)
def noti_on_reply(sender, instance, created, **kwargs):
    if created and instance.parent_post:
        parent_owner = instance.parent_post.user
        if parent_owner != instance.user:
           Notification.objects.create(
            receiver=parent_owner,
            sent=instance.user,
            reply=instance
        )
@receiver(post_save,sender=Post)
def noti_on_repost(sender,instance,created,**kwargs):
    if created and instance.repost_of:
        post_owner=instance.repost_of.user
        if post_owner!=instance.user:
            Notification.objects.create(
            receiver=post_owner,
            sent=instance.user,
            repost=instance
        )

@receiver(post_save, sender=Like)
def noti_on_like(sender, instance, created, **kwargs):
    if created:
        post_owner = instance.post.user
        like_user=instance.user
        if post_owner != instance.user:
           Notification.objects.create(
            receiver=post_owner,
            sent=like_user,
            like=instance
        )
           print(1)
    
@receiver(post_save, sender=Follow)
def noti_on_Follow(sender, instance, created, **kwargs):
    if created:
        followed_user = instance.following
        following_user=instance.follower
        if followed_user != following_user:
           Notification.objects.create(
            receiver=followed_user,
            sent=following_user,
            follow=instance
        )