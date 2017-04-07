from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class GrabBagAdminSite(AdminSite):
    site_header = 'Grab Bag Administration'
    site_title = 'Grab Bag Django Admin Panel'
    index_title = 'Home'
    site_url = '/'


site_admin = GrabBagAdminSite(name='grab_bag_admin')
site_admin.register(User, UserAdmin)
site_admin.register(Group, GroupAdmin)


