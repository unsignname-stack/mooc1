
import xadmin
from QuizAndExam.models import Quiz, Exam, Questions, QuizAnswerSheet, ExamAnswerSheet, QuizAnswerRecord, \
    ExamAnswerRecord
from xadmin.models import Log
from .models import *
from users.models import *
from comments.models import Topics
from xadmin.views import CommAdminView, BaseAdminView
from django.contrib.auth.models import Group,Permission
class GlobalSetting(object):
    # 全局设置
    site_title = '学生线上学习后台管理系统'
    site_footer = 'Design by Sunshaotian'
    # 菜单默认收缩
    menu_style = 'self_accordion'
    # menu_style = 'accordion'
    # 自定义菜单
    # 'self_default': 'xadmin/includes/self_sitemenu_default.html',
    # 'self_accordion': 'xadmin/includes/self_sitemenu_accordion.html',
    def get_site_menu(self):
        # /xadmin/courses/course/1/update/
        # 'url': self.get_model_url(Course, 'changelist')

        if self.request.user.is_superuser:
            return [
            {'title': '用户信息','icon': 'fa fa-linux','menus': (
                {'title': '个人用户','icon': 'fa fa-user','url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '组织机构','icon': 'fa fa-home','url': self.get_model_url(Organization, 'changelist')},
            )},
            {'title': '课程管理','icon': 'fa fa-book','menus': (
                {'title': '我的课程','icon': 'fa fa-caret-right','url': self.get_model_url(Course, 'changelist')},
                {'title': '我的学生','icon': 'fa fa-caret-right','url': self.get_model_url(UserLearningCourse, 'changelist')},
                {'title': '我的章节','icon': '	fa fa-caret-right','url': self.get_model_url(Chapter, 'changelist')},
                {'title': '我的课时','icon': 'fa fa-caret-right','url': self.get_model_url(Lesson, 'changelist')},
                {'title': '我的课件','icon': 'fa fa-caret-right','url': self.get_model_url(Courseware, 'changelist')},
                {'title': '我的讨论', 'icon': 'fa fa-comments', 'url': self.get_model_url(Topics, 'changelist')},
            )},
            {'title': '作业与考试','icon': 'fa fa-file-text','menus': (
                {'title': '作业','icon': 'fa fa-caret-right','url': self.get_model_url(Quiz, 'changelist')},
                {'title': '考试','icon': 'fa fa-caret-right','url': self.get_model_url(Exam, 'changelist')},
                {'title': '题库','icon': 'fa fa-caret-right','url': self.get_model_url(Questions, 'changelist')},
                {'title': '作业答卷','icon': 'fa fa-caret-right','url': self.get_model_url(QuizAnswerSheet, 'changelist')},
                {'title': '考试答卷','icon': 'fa fa-caret-right','url': self.get_model_url(ExamAnswerSheet, 'changelist')},
                {'title': '答题记录（作业）','icon': 'fa fa-caret-right','url': self.get_model_url(QuizAnswerRecord, 'changelist')},
                {'title': '答题记录（考试）','icon': 'fa fa-caret-right','url': self.get_model_url(ExamAnswerRecord, 'changelist')},
            )},
            {'title': '相关设置','icon': 'fa fa-gears','menus': (
                {'title': '课程类别','icon': 'fa fa-th','url': self.get_model_url(CourseCategory, 'changelist')},
                {'title': '轮播课程','icon': 'fa fa-desktop','url': self.get_model_url(Banner, 'changelist')},
                {'title': '学习团队','icon': 'fa fa-group','url': self.get_model_url(Team, 'changelist')},
            )},
            {'title': '系统管理','icon': 'fa fa-gear','menus': (
                {'title': '组别','icon': 'fa fa-caret-right','url': self.get_model_url(Group, 'changelist')},
                {'title': '权限','icon': 'fa fa-caret-right','url': self.get_model_url(Permission, 'changelist')},
                {'title': '日志记录','icon': 'fa fa-caret-right','url': self.get_model_url(Log, 'changelist')},

            )},

        ]
        else:
            # course_list = Course.objects.all().values('id', 'name')
            # course_turple = []
            # for course in course_list:
            #     # /xadmin/courses/chapter/1/ update /
            #     chapter_list = Chapter.objects.filter(course_id=course['id']).values('id', 'name')
            #     chapter_turple = []
            #     for chapter in chapter_list:
            #         lesson_list = Lesson.objects.filter(chapter_id=chapter['id']).values('id', 'name')
            #         lesson_turple = []
            #         # /xadmin/courses/lesson/1/update/
            #         for lesson in lesson_list:
            #             lesson_turple.append({'title': lesson['name'],
            #                                   'url': '/xadmin/courses/lesson/{id}/update/'.format(id=lesson['id'])})
            #         chapter_turple.append({'title': chapter['name'],
            #                                # 'url': '/xadmin/courses/chapter/{id}/update/'.format(id=chapter['id']),
            #                                'menus': tuple(lesson_turple)})
            #     course_turple.append({'title': course['name'], 'icon': 'fa fa-caret-right',
            #                           # 'url': '/xadmin/courses/course/{id}/update/'.format(id=course['id']),
            #                           'menus': tuple(chapter_turple)})
            return [
                {'title': '用户信息','icon': 'fa fa-linux', 'menus': (
                    {'title': '个人用户','icon': 'fa fa-user','url': self.get_model_url(UserProfile, 'changelist')},
                )},
                # {'title': '我的课程', 'icon': 'fa fa-gear', 'menus': tuple(course_turple)},
                {'title': '课程管理','icon': 'fa fa-book', 'menus': (
                    {'title': '我的课程','icon': 'fa fa-caret-right','url': self.get_model_url(Course, 'changelist')},
                    {'title': '在学学生','icon': 'fa fa-caret-right','url': self.get_model_url(UserLearningCourse, 'changelist')},
                    {'title': '我的章节','icon': '	fa fa-caret-right','url': self.get_model_url(Chapter, 'changelist')},
                    {'title': '我的课时','icon': 'fa fa-caret-right','url': self.get_model_url(Lesson, 'changelist')},
                    {'title': '我的课件','icon': 'fa fa-caret-right','url': self.get_model_url(Courseware, 'changelist')},
                    {'title': '我的讨论', 'icon': 'fa fa-comments', 'url': self.get_model_url(Topics, 'changelist')},
                )},
                {'title': '作业与考试','icon': 'fa fa-file-text','menus': (
                    {'title': '作业','icon': 'fa fa-caret-right','url': self.get_model_url(Quiz, 'changelist')},
                    {'title': '考试','icon': 'fa fa-caret-right','url': self.get_model_url(Exam, 'changelist')},
                    {'title': '题库','icon': 'fa fa-caret-right','url': self.get_model_url(Questions, 'changelist')},
                    {'title': '作业答卷','icon': 'fa fa-caret-right','url': self.get_model_url(QuizAnswerSheet, 'changelist')},
                    {'title': '考试答卷','icon': 'fa fa-caret-right','url': self.get_model_url(ExamAnswerSheet, 'changelist')},
                    {'title': '答题记录（作业）','icon': 'fa fa-caret-right','url': self.get_model_url(QuizAnswerRecord, 'changelist')},
                    {'title': '答题记录（考试）','icon': 'fa fa-caret-right','url': self.get_model_url(ExamAnswerRecord, 'changelist')},
                )},
                {'title': '课程类别','icon': 'fa fa-gears',
                    'url': self.get_model_url(CourseCategory, 'changelist')
                },

            ]


xadmin.site.register(CommAdminView, GlobalSetting)

class BaseSetting(object):
    pass
    # 启动主题管理器
    # enable_themes = True
    # 使用主题
    # use_bootswatch = True

# xadmin.site.register(Grade, GradeAdmin)






def AdminFilter(admin,self):
    qs = super(admin, self).queryset()
    if self.request.user.is_superuser:  # 超级用户可查看所有数据
        return qs
    else:
        return qs.filter(teacher=self.request.user)  # teacher是Course Model的用户字段
class ChapterInline(object):
    model = Chapter
    fields = ['order','name','teacher']
    readonly_fields = []
    ordering=['order']
    exclude=[ ]
    style = 'accordion' #one，accordion，tab，stacked，table
    # can_delete = False
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user.username)
        return super(ChapterInline, self).formfield_for_dbfield(db_field, **kwargs)
class CourseGroupInline(object):
    model=CourseGroup
    fields = ['member', 'number', 'name',]
    readonly_fields = []
    ordering = ['number']
    exclude = []
    # style_fields = { 'member': 'm2m_transfer', }#此句会报错，不知原因
    style = 'accordion'
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "member":
                #以下查询返回的选课表中选了此门课程的用户字段的用户id元组
                user_id_list = UserLearningCourse.objects.filter(course=self.org_obj).values_list('user',flat=True)
                kwargs["queryset"] = UserProfile.objects.filter(id__in=user_id_list)
        return super(CourseGroupInline, self).formfield_for_dbfield(db_field, **kwargs)

class LearningStudentInline(object):
    model = UserLearningCourse
    style = 'accordion'  # one，accordion，tab，stacked，table
    # can_delete = False
    extra = 0
    can_delete = True
class ExamInline(object):
    model = Exam
    fields = ['name','tips','teacher','exam_date', 'top_score','questions']
    readonly_fields = []
    ordering=['exam_date']
    exclude=[ ]
    style_fields = { 'questions': 'm2m_transfer', }
    style = 'accordion' #one，accordion，tab，stacked，table
    # can_delete = False
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "questions":
                kwargs["queryset"] = Questions.objects.filter(teacher=self.request.user)
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user)
        return super(ExamInline, self).formfield_for_dbfield(db_field, **kwargs)
class CourseAdmin(object):
    list_display = ['id','name','learn_times','degree','stu_num',
                 'category','tag','add_time','teacher','is_hide']
    search_fields = ['name', ]
    readonly_fields =['stu_num','fav_nums','click_nums','add_time',]
    model_icon = 'fa fa-angle-double-right'

    ordering = ['add_time','id']
    inlines = [LearningStudentInline,CourseGroupInline,ChapterInline,ExamInline]
    # LearningStudentInline.short_description = "学生",无效
    #list_editable = ["is_hot", 'is_new']
    list_filter = ["name", "add_time"]
    list_editable = ['name','learn_times','degree',
                 'category','tag','is_hide']
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user)
            if db_field.name == "org":
                    kwargs["queryset"] = Organization.objects.filter(name=self.request.user.org)
        return super(CourseAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def queryset(self):
        return AdminFilter(CourseAdmin, self)
class LessonInline(object):
    model = Lesson
    fields = ['order','name','chapter','teacher']
    readonly_fields = []
    ordering=['order']
    exclude=[ ]
    style = 'accordion' #one，accordion，tab，stacked，table
    # can_delete = False
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user.username)
        return super(LessonInline, self).formfield_for_dbfield(db_field, **kwargs)
class ChapterAdmin(object):
    list_display = ['order','name','course']
    search_fields = ['order','name','course']
    list_editable = ['order','name','course']
    list_filter =['order','name','course']
    row_id_fields =['course',]
    ordering = ['course','order']
    inlines = [LessonInline]
    model_icon = 'fa fa-angle-double-right'
    #post请求时对关联外键进行过滤
    def get_context(self):
        context = super(ChapterAdmin, self).get_context()
        if 'form' in context:
            if not self.request.user.is_superuser:
                context['form'].fields['course'].queryset = context['form'].fields['course'].queryset.filter(teacher=self.request.user)
                context['form'].fields['teacher'].queryset = context['form'].fields['teacher'].queryset.filter(username=self.request.user)
        return context

    def queryset(self):   #过滤list
        return AdminFilter(ChapterAdmin, self)
class CoursewareInline(object):
    model = Courseware
    fields = ['teacher','name','file_type','url', 'order']
    readonly_fields = []
    ordering=['order']
    exclude=[ ]
    style = 'accordion' #one，accordion，tab，stacked，table
    # can_delete = False
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user.username)
        return super(CoursewareInline, self).formfield_for_dbfield(db_field, **kwargs)
class QuizInline(object):
    model = Quiz
    fields = ['name','tips','teacher','public_date', 'top_score','questions']
    readonly_fields = []
    ordering=['public_date']
    exclude=[ ]
    style_fields = {'teacher': 'm2m_transfer', 'questions': 'm2m_transfer', }
    style = 'accordion' #one，accordion，tab，stacked，table
    extra = 0
    can_delete = True
    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "questions":
                kwargs["queryset"] = Questions.objects.filter(teacher=self.request.user)
            if db_field.name == "teacher":
                kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user)
        return super(QuizInline, self).formfield_for_dbfield(db_field, **kwargs)
class LessonAdmin(object):
    def belong_course(self,obj):
        return ("《%s》")%(obj.chapter.course)

    belong_course.short_description = "所属课程"

    list_display = ['order','name','chapter','belong_course']
    search_fields = ['order','name','chapter']
    list_editable = ['order','name',]
    list_filter = []
    ordering = ['chapter','order']
    readonly_fields = ['chapter','belong_course','teacher']
    model_icon = 'fa fa-angle-double-right'
    inlines = [CoursewareInline,QuizInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        # if not self.request.user.is_superuser:
            # if db_field.name == "teacher":
            #     kwargs["queryset"] = UserProfile.objects.filter(username=self.request.user.username)
        return super(LessonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    #以上方法更简单
    # def get_context(self):
    #     context = super(LessonAdmin, self).get_context()
    #     if 'form' in context:
    #         if not self.request.user.is_superuser:
    #             # context['form'].fields['chapter'].queryset = context['form'].fields['chapter'].queryset.filter(teacher=self.request.user)
    #             context['form'].fields['teacher'].queryset = context['form'].fields['teacher'].queryset.filter(username=self.request.user.username)
    #     return context

    def queryset(self):
        return AdminFilter(LessonAdmin, self)
    #style_fields = {"goods_desc": "ueditor"}
class CoursewareAdmin(object):
    def belong_course(self,obj):
        return ("《%s》")%(obj.lesson.chapter.course)

    belong_course.short_description = "所属课程"
    list_display = ['order','name','file_type','url','lesson','belong_course']
    search_fields = ['order','name','file_type','lesson']
    list_editable = ['order','name','file_type','lesson','url']
    list_filter = ['order','name','file_type','lesson']
    readonly_fields = ['lesson', 'teacher','belong_course']
    model_icon = 'fa fa-angle-double-right'
    ordering = ['lesson', 'order']
    #style_fields = {"goods_desc": "ueditor"}
    def get_context(self):
        context = super(CoursewareAdmin, self).get_context()
        # if 'form' in context:
        #     if not self.request.user.is_superuser:
        #         context['form'].fields['lesson'].queryset = context['form'].fields['lesson'].queryset.filter(teacher=self.request.user)
        #         context['form'].fields['teacher'].queryset = context['form'].fields['teacher'].queryset.filter(username=self.request.user.username)
        return context

    def queryset(self):
        return AdminFilter(CoursewareAdmin, self)

class BannerCourseAdmin(object):
    list_display = ["course", "image", "index"]

class CourseCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time",'is_tab']
    list_editable =['is_tab',]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]

class UserLearningCourseAdmin(object):
    list_display = ['id',"user", "course", "add_time", 'isDelete']
    list_editable = ['isDelete']
    list_filter = ["user", "course"]
    search_fields = ["user", "course"]


class TeamAdmin(object):
    model=Team
    list_display = ['id','member', 'number', 'name','introduction']
    fields = ['member', 'number', 'name','introduction']
    readonly_fields = []
    ordering = ['number']
    exclude = []
    style_fields = { 'member': 'm2m_transfer', }#此句会报错，不知原因

xadmin.site.register(Team, TeamAdmin)


xadmin.site.register(Banner,BannerCourseAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Courseware, CoursewareAdmin)
xadmin.site.register(CourseCategory,CourseCategoryAdmin)
xadmin.site.register(UserLearningCourse,UserLearningCourseAdmin)
