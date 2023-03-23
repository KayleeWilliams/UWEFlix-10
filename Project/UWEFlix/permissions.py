from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(ContentType)

# Define the groups and permissions
groups = {"Student": ["debit_account", "test"], "ClubRep": ["debit_account"]}


# Loop through the groups and add the permissions
for group in groups.keys():
    if not Group.objects.filter(name='Student').exists():
        Group.objects.create(name=group)

    for p in groups[group]:
        if not Permission.objects.filter(codename=p).exists():
            permission = Permission.objects.create(
                codename=p, name='Can ' + p, content_type=content_type,)
            Group.objects.get(name=group).permissions.add(permission)
