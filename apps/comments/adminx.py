
import xadmin
from comments.models import Topics, TopicPicture, LevelOneReply
from courses.models import Course
from users.models import UserProfile


def AdminFilter(admin,self):
    qs = super(admin, self).queryset()
    if self.request.user.is_superuser:  # 超级用户可查看所有数据
        return qs
    else:
        return qs.filter(owner=self.request.user)  # teacher是Course Model的用户字段

class TopicPictureInline(object):
    model = TopicPicture
    fields = ['picture_name', 'picture', ]
    readonly_fields = []
    exclude = []
    style = 'accordion'
    can_delete = True
    extra = 0

class LevelOneReplyInline(object):
    model = LevelOneReply
    fields = ['owner', 'public_date_time','content' ]
    # readonly_fields = ['owner', 'public_date_time','content' ]
    exclude = []
    style = 'accordion'
    can_delete = True
    extra = 0

class TopicsAdmin(object):
    list_display = ['id', 'title', 'public_date_time','owner','course'  ]
    model_icon = 'fa fa-comments'
    def queryset(self):
        return AdminFilter(TopicsAdmin, self)
    inlines = [TopicPictureInline,LevelOneReplyInline ]
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "course":
                kwargs["queryset"] = Course.objects.filter(teacher=self.request.user)
            if db_field.name == "owner":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user)
        return super(TopicsAdmin, self).formfield_for_dbfield(db_field, **kwargs)

xadmin.site.register(Topics, TopicsAdmin)