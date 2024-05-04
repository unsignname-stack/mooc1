from django.db import models
from courses.models import Lesson, Course


#题库
class Questions(models.Model):
    """题库"""
    LEVEL_CHOICES = (('1', '入门'),('2', '简单'),('3', '普通'),('4', '较难'),('5', '困难'))
    TYPE_CHOICES = (('1', '单选题'),('2', '多选题'),('3', '判断题'),('4', '填空题'),('5', '简答题'),
                    ('6', '问答题'),('7', '编程题'),('8', '其他客观题'),('9', '其他主观题'))

    question = models.TextField("题目",)
    right_answer = models.TextField("参考答案",)
    analysis = models.TextField("解析", default="暂无")
    question_type = models.CharField("题型", max_length=1, choices=TYPE_CHOICES)
    level = models.CharField("难度等级", max_length=1, choices=LEVEL_CHOICES, default='1')
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'questions', verbose_name=u'老师')
    score = models.PositiveSmallIntegerField("分值", )
    auto_judge = models.BooleanField(verbose_name='是否机评')

    class Meta:
        ordering = ['id']
        verbose_name = '题库'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.question

class QuestionsPicture(models.Model):
        """题目插图"""
        question = models.ForeignKey(Questions, on_delete=models.CASCADE, db_constraint=False,
                                    related_name=u'question_picture', verbose_name=u'题目')
        picture_name = models.CharField("插图名字", max_length=20,)
        picture = models.ImageField(upload_to="question/picture/", verbose_name=u"插图", blank=True,
                                   null=True,max_length=200)
        class Meta:
            ordering = ['id']
            verbose_name = '题目插图'
            verbose_name_plural = verbose_name
        def __str__(self):
            return self.picture_name


class Quiz(models.Model):
    """作业模型类"""
    name = models.CharField("作业名称", max_length=40)
    tips = models.TextField("作业说明", default="暂无")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, db_constraint=False,
                               related_name=u'quiz', verbose_name=u'课时')
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'quizs', verbose_name=u'老师')
    public_date = models.DateTimeField ("发布日期时间")
    top_score = models.PositiveSmallIntegerField("总分", default=100)
    questions = models.ManyToManyField(Questions, blank=True, verbose_name=u'题目',
                                       related_name="quizs",related_query_name="quiz")
    show_result=models.BooleanField(default=False,verbose_name=u'公示评分结果')
    class Meta:
        ordering = ["id"]
        verbose_name = "作业"
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s') % (self.name)

class Exam(models.Model):
    """考试模型类"""
    name = models.CharField("考试名称", max_length=40)
    tips = models.TextField("考生须知", default="暂无")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_constraint=False,
                               related_name=u'exam', verbose_name=u'课程')
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'exams', verbose_name=u'老师')
    top_score = models.PositiveSmallIntegerField("总分", default=100)
    exam_date = models.DateTimeField("考试日期时间")
    total_time = models.PositiveSmallIntegerField("考试时长", default=120, help_text="时长按照分钟填写")
    questions = models.ManyToManyField(Questions, blank=True, verbose_name=u'题目',
                                       related_name="exams", related_query_name="exam")
    show_result = models.BooleanField(default=False, verbose_name=u'公示评分结果')

    class Meta:
        ordering = ["id"]
        verbose_name = "考试"
        verbose_name_plural = verbose_name

    def __str__(self):
        return ('%s %s') % (self.course,self.name)


class QuizAnswerSheet(models.Model):
    '''作业答卷'''
    student = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'quiz_answer_sheet', verbose_name=u'答题学生')
    quiz = models.ForeignKey(Quiz, verbose_name='作业', related_name='quiz_answer_sheet',
                             on_delete=models.CASCADE, db_constraint=False)
    teacher = models.CharField('归属老师',max_length=20,blank=True)
    all_score = models.PositiveSmallIntegerField("总分", blank=True, null=True)
    def save(self, *args, **kwargs):
        self.teacher = self.quiz.teacher.username
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['id']
        verbose_name = '作业答卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ('%s的答卷（作业：%s）') % (self.student,self.quiz,)
# class BookInfoManager(models.Manager):
#     pass
class QuizAnswerRecord(models.Model):
    '''作业答题记录模型'''
    question = models.ForeignKey(Questions, verbose_name="题目", related_name=u'quiz_answer_record',
                                 on_delete=models.CASCADE, db_constraint=False)
    stu_answer = models.TextField("学生的作答", null=True, blank=True)
    score = models.PositiveSmallIntegerField("得分", null=True, blank=True)
    student = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'quiz_answer_record', verbose_name=u'答题学生')
    quiz_answer_sheet = models.ForeignKey(QuizAnswerSheet, verbose_name='作业答卷', related_name='quiz_answer_record',
                                    on_delete=models.CASCADE, db_constraint=False)
    class Meta:
        ordering = ['id']
        verbose_name = '答题记录（作业）'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s答题记录" % self.student
class ExamAnswerSheet(models.Model):
    '''考试答卷'''
    student = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'exam_answer_sheet', verbose_name=u'答题学生')
    exam = models.ForeignKey(Exam, verbose_name='考试', related_name='exam_answer_sheet',
                             on_delete=models.CASCADE, db_constraint=False)
    teacher = models.CharField('归属老师',max_length=20,blank=True)
    all_score = models.PositiveSmallIntegerField("总分", blank=True,null=True)


    def save(self, *args, **kwargs):
        self.teacher = self.exam.teacher.username
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['id']
        verbose_name = '考试答卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ('%s的答卷（考试：%s）') % (self.student,self.exam,)
class ExamAnswerRecord(models.Model):
    '''考试答题记录模型'''
    stu_answer = models.TextField("学生的作答", null=True, blank=True)
    score = models.PositiveSmallIntegerField("得分", null=True, blank=True)
    student = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'exam_answer_record', verbose_name=u'答题学生')
    exam_answer_sheet = models.ForeignKey(ExamAnswerSheet, verbose_name='考试答卷', related_name='exam_answer_record',
                                    on_delete=models.CASCADE, db_constraint=False)
    question = models.ForeignKey(Questions, verbose_name="题目", related_name=u'exam_answer_record',
                              on_delete=models.CASCADE,db_constraint=False)
    class Meta:
        ordering = ['id']
        verbose_name = '答题记录（考试）'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.stu_answer