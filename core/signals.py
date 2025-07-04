# core/signals.py
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import File, Profile

@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(File)

    admin_group, _ = Group.objects.get_or_create(name='Admin')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    viewer_group, _ = Group.objects.get_or_create(name='Viewer')

    # Core permissions
    view_perm = Permission.objects.get(codename='view_file')
    edit_perm = Permission.objects.get(codename='change_file')
    delete_perm = Permission.objects.get(codename='delete_file')

    # Optional custom permission
    Permission.objects.get_or_create(
        codename='can_edit_file',
        name='Can edit file',
        content_type=content_type
    )

    # Assign permissions
    editor_group.permissions.set([view_perm, edit_perm])
    admin_group.permissions.set([view_perm, edit_perm, delete_perm])
    viewer_group.permissions.set([view_perm])

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
