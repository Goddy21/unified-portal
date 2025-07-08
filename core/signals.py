# core/signals.py
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import File, Profile
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if not User.objects.filter(username='john').exists():
        user = User.objects.create_user(username='john', email='john@example.com')
        user.set_password('securePassword123')
        user.save()


@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    from django.core.exceptions import ObjectDoesNotExist

    content_type = ContentType.objects.get_for_model(File)

    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    viewer_group, _ = Group.objects.get_or_create(name='Viewer')
    customer_group, _ = Group.objects.get_or_create(name='Customer')

    try:
        # Get built-in file model permissions
        view_perm = Permission.objects.get(codename='view_file')
        edit_perm = Permission.objects.get(codename='change_file')
        delete_perm = Permission.objects.get(codename='delete_file')
    except ObjectDoesNotExist:
        return

    # Optional custom permission
    can_edit_file_perm, _ = Permission.objects.get_or_create(
        codename='can_edit_file',
        name='Can edit file',
        content_type=content_type
    )

    # Assign permissions
    admin_group.permissions.set([view_perm, edit_perm, delete_perm, can_edit_file_perm])
    editor_group.permissions.set([view_perm, edit_perm])
    viewer_group.permissions.set([view_perm])
    customer_group.permissions.set([view_perm])  


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.is_superuser:
            admin_group = Group.objects.get(name='Admin')
            instance.groups.add(admin_group)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

