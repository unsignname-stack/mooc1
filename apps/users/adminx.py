import xadmin
from courses.models import Course, Team
from .models import *
from django.contrib.auth import get_user_model
import xadmin


from .models import UserProfile
from xadmin.plugins import auth
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _



class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username', 'mobile', 'org', 'date_joined','category']
    readonly_fields = ['last_login', 'date_joined','groups','is_active',
                       'is_staff', 'is_superuser','user_permissions','org',
                       'category','add_time','username']
    # exclude = ['user_permissions',  ]
    search_fields = ('username','mobile')
    style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}
    def get_readonly_fields(self, **kwargs):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        # print(self.org_obj)
        if self.user.is_superuser:
            self.readonly_fields = ['last_login', 'date_joined']
        return self.readonly_fields

    # 表单根据用户显示不同的字段内容
    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.fields = ['username', 'mobile', 'is_staff']

        return super().get_model_form(**kwargs)

#
xadmin.site.unregister(get_user_model())
xadmin.site.register(UserProfile, UserAdmin)


class CourseInline(object):
    model=Course
    fields = []
    readonly_fields = []
    ordering = []
    exclude = []
    style_fields = { }
    style = 'accordion'  # one，accordion，tab，stacked，table
    extra = 0
    can_delete = True
class UserInline(object):
    model=UserProfile
    fields = []
    readonly_fields = []
    ordering = []
    exclude = []
    style_fields = { }
    style = 'accordion'  # one，accordion，tab，stacked，table
    extra = 0
    can_delete = True
class OrganizationAdmin(object):
    list_display = ['id', 'name',  'category', 'image','students']
    readonly_fields = ['students','course_nums','add_time']
    inlines=[UserInline,CourseInline]
        # name = desc = category = image = address
        # students = course_nums = add_time



xadmin.site.register(Organization, OrganizationAdmin)
