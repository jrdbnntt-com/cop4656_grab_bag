"""
    Group access utility for group-based acl. Extend to add new groups
"""

from django.contrib.auth.models import User, Group


class GroupManager(object):
    USER = 'user'
    ADMIN = 'admin'

    def __init__(self, db_groups: list, extra_groups: list):
        self.db_groups = db_groups
        self.extra_groups = extra_groups

    def is_group(self, group_name: str) -> bool:
        return group_name in self.db_groups or group_name in self.extra_groups

    def validate_db_group(self, group_name: str):
        if group_name not in self.db_groups:
            raise ValueError('Group "{}" is not a database group'.format(group_name))

    def validate_db_groups(self, group_names: list):
        for name in group_names:
            self.validate_db_group(name)

    def add_user_to_group(self, user: User, group_name: str):
        """ Adds user to a single group if not already in it """
        self.validate_db_group(group_name)
        group_to_add = Group.objects.get(name=group_name)
        if not user.groups.filter(name=group_to_add).exists():
            user.groups.add(group_to_add)
        user.save()

    def remove_user_from_group(self, user: User, group_name: str):
        """ Removes user from a single group if in it """
        self.validate_db_group(group_name)
        matched_group = user.groups.filter(name=group_name)
        if matched_group.exists():
            user.groups.remove(matched_group[0])
        user.save()

    def add_user_to_groups(self, user: User, group_names: list):
        """ Adds user to multiple groups if not already in them """
        self.validate_db_groups(group_names)
        groups_to_add = Group.objects.filter(name__in=[group_names])
        if groups_to_add.exists():
            for group in groups_to_add:
                if not user.group.filter(id=group.id).exists():
                    user.groups.add(group)
        user.save()

    def remove_user_from_groups(self, user: User, group_names: list):
        """ Removes user from multiple groups if in them """
        self.validate_db_groups(group_names)
        matched_groups = user.groups.filter(name__in=group_names)
        if matched_groups.exists():
            for group in matched_groups:
                user.groups.remove(group)
        user.save()
