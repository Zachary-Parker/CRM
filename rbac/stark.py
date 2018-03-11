from stark.service import v1
from . import models
class UserConfig(v1.StarkConfig):
    list_display = ['id','username','email']
    edit_link = ['username']
v1.site.register(models.User,UserConfig)


class RoleConfig(v1.StarkConfig):
    list_display = ['id','title',]
    edit_link = ['title']

v1.site.register(models.Role,RoleConfig)




class PermissionConfig(v1.StarkConfig):
    list_display = ['id','title','url','menu_gp','code']
v1.site.register(models.Permission,PermissionConfig)


class GroupConfig(v1.StarkConfig):
    list_display = ['id','caption','menu']
    edit_link = ['caption']
v1.site.register(models.Group,GroupConfig)


class MenuConfig(v1.StarkConfig):
    list_display = ['id','title']
    edit_link = ['title']
v1.site.register(models.Menu,MenuConfig)