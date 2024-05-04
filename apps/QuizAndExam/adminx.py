from django.http import HttpResponse, HttpResponseRedirect

import xadmin
from QuizAndExam.models import Questions, QuizAnswerSheet, Quiz, QuizAnswerRecord, ExamAnswerSheet, Exam, \
    ExamAnswerRecord, QuestionsPicture
from users.models import UserProfile
from courses.adminx import AdminFilter, CourseAdmin
from import_export import resources
from xadmin.plugins.actions import BaseActionView
from django.utils.translation import ugettext as _




class QuestionsResource(resources.ModelResource):
    class Meta:
        model = Questions
        fields = ('id', 'question', 'right_answer', 'analysis', 'score',
                    'question_type','auto_judge','level','teacher')
class PictureInline(object):
    model = QuestionsPicture
    fields = ['picture_name','picture',]
    readonly_fields = []
    exclude=[]
    style = 'accordion'
    can_delete = True
    extra = 0

class QuestionsAdmin(object):
    list_display = ['id', 'question', 'right_answer', 'analysis', 'score',
                    'question_type','auto_judge','level','teacher']
    list_filter = ['level']
    search_fields = ['id', 'question']
    list_display_links = ['question']
    list_per_page = 10
    inlines=[PictureInline,]
    # list_editable = ['question']
    model_icon = 'fa fa-dot-circle-o'
    import_export_args = {'import_resource_class': QuestionsResource}
    def get_context(self):
        context = super(QuestionsAdmin, self).get_context()
        if 'form' in context:
            if self.request.user.is_superuser:
                context['form'].fields['teacher'].queryset = UserProfile.objects.all()
            else:
                context['form'].fields['teacher'].queryset = UserProfile.objects.filter(username=self.request.user)
        return context

    def queryset(self):
        return AdminFilter(QuestionsAdmin, self)

xadmin.site.register(Questions, QuestionsAdmin)

class QuizAnswerSheetInline(object):
    model = QuizAnswerSheet
    fields = ['student',]
    readonly_fields = ['student',]
    exclude=['teacher']
    style = 'table'
    can_delete = False
    # raw_id_fields = ('id',)
    extra = 0

class QuizAdmin(object):
    def get_chapter(self,obj):
        return obj.lesson.chapter
    def get_course(self,obj):
        return obj.lesson.chapter.course
    def go_to_answer_sheet(self,obj):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='/xadmin/QuizAndExam/quizanswersheet/?_p_quiz__id__exact={id}'>查看答卷</a>".format(id=obj.id))

    go_to_answer_sheet.short_description = "学生答卷"
    get_chapter.short_description = "章节"
    get_course.short_description = "课程"
    list_display = ['name','get_course','get_chapter','lesson','show_result','teacher','top_score','go_to_answer_sheet']
    search_fields = ['id', 'name']
    list_editable = ['show_result']
    readonly_fields = ['get_course','get_chapter','lesson','teacher','go_to_answer_sheet']
    list_per_page = 10
    # list_editable = ['name']
    model_icon = 'fa fa-file-text'
    style_fields = {'teacher': 'm2m_transfer','questions': 'm2m_transfer', }
    inlines = [QuizAnswerSheetInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "questions":
                kwargs["queryset"] = Questions.objects.filter(teacher=self.request.user)
        return super(QuizAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def queryset(self):
        return AdminFilter(QuizAdmin, self)

xadmin.site.register(Quiz, QuizAdmin)

class QuizAnswerRecordInline(object):
    model = QuizAnswerRecord
    style = 'table'
    can_delete = False
    readonly_fields = ['stu_answer','question','student' ]
    extra = 0
class QuestionsInline(object):

    model = Questions
    # style = 'table'  #one，accordion，tab，stacked，table
    extra = 0
class ComputeAllScore(BaseActionView):
    # 这里需要填写三个属性
    action_name = "compute_all_score"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = _(u'统计所选 %(verbose_name_plural)s 总分')  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'  #: 该 Action 所需权限
    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        answer_records =[]
        for obj in queryset:
            obj.all_score=0
            if hasattr(obj,'quiz') :
                answer_records=QuizAnswerRecord.objects.filter(quiz_answer_sheet=obj)
            if hasattr(obj,'exam'):
                answer_records = ExamAnswerRecord.objects.filter(exam_answer_sheet=obj)
            for record in answer_records:
                obj.all_score += int(record.score or 0)  # 累计总分
                # if(record.score):
                #     obj.all_score += int(record.score)  #累计总分
            obj.save()

        # 返回 HttpResponse
        return HttpResponseRedirect(self.request.get_full_path())

class QuizAnswerSheetAdmin(object):
    '''作业答卷'''

    def quiz_choices(self, field, request, params, model, model_admin, field_path):
        # 目的，是使过滤器只显示用户老师自己的作业。以下这种修改方式要先修改xadmin/filters.py
        #此方法是为此类新增的一个方法属性，供xadmin/filters.py 里类：RelatedFieldListFilter调用
        # 如果是超级用户不做控制
        #方法名是由list_filter = ['quiz']里的qiuz 和_choices,主要是要和RelatedFieldListFilter保持一致
        if self.request.user.is_superuser:
            return field.get_choices(include_blank=False)#这是原本的默认调用方法

        # 这里就是自己写条件，从数据库中查询出需要显示的考试
        owner_quiz = Quiz.objects.filter(teacher=self.request.user).order_by('id')
        # store_lst = self.get_query_set(model.objects).values('store__title').distinct().order_by('id')
        # 返回格式 [('pk','标题'),]
        return list(((quiz.id, quiz.name) for quiz in owner_quiz))


    list_display = ['student', 'quiz','teacher','all_score']
    list_filter = ['quiz','student']
    readonly_fields =['student', 'quiz','teacher',]
    actions = [ComputeAllScore, ]
    inlines = [QuizAnswerRecordInline]
    list_per_page = 10

    def get_readonly_fields(self, **kwargs):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields
    def queryset(self):
        teacher_quizs=Quiz.objects.filter(teacher=self.request.user)
        qs = super(QuizAnswerSheetAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(teacher=self.request.user)  # teacher是Course Model的用户字段
xadmin.site.register(QuizAnswerSheet,QuizAnswerSheetAdmin)

class QuizAnswerRecordAdmin(object):

    def get_question(self, obj, ):
        LEVEL_CHOICES = {'1': '入门', '2': '简单', '3': '普通', '4': '较难', '5': '困难'}
        TYPE_CHOICES = {'1': '单选题', '2': '多选题', '3': '判断题', '4': '填空题', '5': '简答题',
                        '6': '问答题', '7': '编程题', '8': '其他客观题', '9': '其他主观题'}
        ques="%s(分值：%s分) 问题：%s 正确答案：%s 难度：%s 解析：%s "%(
            TYPE_CHOICES[obj.question.question_type],obj.question.score,
            obj.question.question,obj.question.right_answer,
            LEVEL_CHOICES[obj.question.level],obj.question.analysis)
        return str(ques)

    list_display = ['id','stu_answer', 'score','student','quiz_answer_sheet']
    list_filter = []
    readonly_fields = ['get_question','question','stu_answer', 'student','quiz_answer_sheet']
    get_question.short_description = '原题'
    # exclude = ['question']

    list_per_page = 10
    # list_editable = ['question']
    model_icon = 'fa fa-dot-circle-o'
    def get_readonly_fields(self, **kwargs):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields
xadmin.site.register(QuizAnswerRecord, QuizAnswerRecordAdmin)

class ExamAnswerSheetInline(object):
    model = ExamAnswerSheet
    fields = ['student', ]
    readonly_fields = ['student', ]
    exclude=[ 'teacher']
    style = 'table'
    can_delete = False
    # raw_id_fields = ('id',)
    extra = 0
class ExamAdmin(object):
    def go_to_answer_sheet(self,obj):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='/xadmin/QuizAndExam/examanswersheet/?_p_exam__id__exact={id}'>查看答卷</a>".format(id=obj.id))
    go_to_answer_sheet.short_description = "学生答卷"
    list_display = ['id', 'name', 'tips','course','exam_date','show_result','teacher','top_score','go_to_answer_sheet']
    list_filter = ['course']
    list_editable = ['show_result']
    readonly_fields = ['course','teacher','go_to_answer_sheet']
    search_fields = ['id', 'name']
    list_per_page = 10
    model_icon = 'fa fa-file-text'
    style_fields = {'teacher': 'm2m_transfer','questions': 'm2m_transfer', }
    inlines = [ExamAnswerSheetInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == "questions":
                kwargs["queryset"] = Questions.objects.filter(teacher=self.request.user)
        return super(ExamAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def queryset(self):
        return AdminFilter(ExamAdmin, self)

xadmin.site.register(Exam, ExamAdmin)

class ExamAnswerRecordInline(object):
    model = ExamAnswerRecord
    style = 'table'
    can_delete = False
    readonly_fields = ['stu_answer','question','student' ]
    extra = 0


class ExamAnswerSheetAdmin(object):
    '''考试答卷'''

    def exam_choices(self, field, request, params, model, model_admin, field_path):
        if self.request.user.is_superuser:
            return field.get_choices(include_blank=False)#这是原本的默认调用方法

        owner_exam = Exam.objects.filter(teacher=self.request.user).order_by('id')

        return list(((exam.id, exam.name) for exam in owner_exam))


    list_display = ['student', 'exam','teacher','all_score']
    list_filter = ['exam','student']
    readonly_fields =['student', 'exam','teacher',]
    actions = [ComputeAllScore, ]
    inlines = [ExamAnswerRecordInline]
    list_per_page = 10

    def get_readonly_fields(self, **kwargs):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields
    def queryset(self):

        qs = super(ExamAnswerSheetAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(teacher=self.request.user)

xadmin.site.register(ExamAnswerSheet,ExamAnswerSheetAdmin)


class ExamAnswerRecordAdmin(object):

    def get_question(self, obj, ):
        LEVEL_CHOICES = {'1': '入门', '2': '简单', '3': '普通', '4': '较难', '5': '困难'}
        TYPE_CHOICES = {'1': '单选题', '2': '多选题', '3': '判断题', '4': '填空题', '5': '简答题',
                        '6': '问答题', '7': '编程题', '8': '其他客观题', '9': '其他主观题'}
        ques="%s(分值：%s分) 问题：%s 正确答案：%s 难度：%s 解析：%s "%(
            TYPE_CHOICES[obj.question.question_type],obj.question.score,
            obj.question.question,obj.question.right_answer,
            LEVEL_CHOICES[obj.question.level],obj.question.analysis)
        return str(ques)

    list_display = ['id','stu_answer', 'score','student','exam_answer_sheet']
    list_filter = []
    readonly_fields = ['get_question','stu_answer', 'question','student','exam_answer_sheet']
    get_question.short_description = '原题'
    # exclude = ['question']

    list_per_page = 10
    # list_editable = ['question']
    model_icon = 'fa fa-dot-circle-o'
    def get_readonly_fields(self, **kwargs):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


xadmin.site.register(ExamAnswerRecord, ExamAnswerRecordAdmin)
