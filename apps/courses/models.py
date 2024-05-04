import os

from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe

from mooc1 import settings
from users.models import UserProfile


class CourseCategory(models.Model):
    """
课程类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),

    )
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",related_name="sub_cat",on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Course(models.Model):
    category = models.ForeignKey(CourseCategory, default=1, verbose_name="课程类别", on_delete=models.CASCADE, )
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300,default='', verbose_name='课程概述', null=True, blank=True)
    target = models.TextField(verbose_name='课程目标', null=True, blank=True)
    teacher = models.ForeignKey('users.UserProfile', on_delete = models.CASCADE,db_constraint=False,
                                related_name=u'courses',verbose_name=u'老师')
    org = models.ForeignKey('users.Organization', on_delete = models.CASCADE,related_name='courses')
    degree = models.CharField(verbose_name='难度',choices=(('primary','初级'),('middle','中级'),('high','高级')),max_length=10)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)', null=True, blank=True)
    stu_num = models.IntegerField(default=0, verbose_name='学习人数', null=True, blank=True)
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数', null=True, blank=True)
    image = models.ImageField(upload_to="courses/images/", null=True, blank=True, verbose_name="封面图")
    #video_file=models.FileField(verbose_name=u'视频',name=u'本视频',upload_to="courses/files/",null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name='点击数', null=True, blank=True)
    # category = models.CharField(default=u'后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='',verbose_name='课程标签',max_length=10, null=True, blank=True)
    readme = models.CharField(default='', max_length=300, verbose_name='课程须知', null=True, blank=True)
    teacher_tell = models.CharField(default='',max_length=300, verbose_name='老师告诉你', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    is_hide = models.BooleanField(verbose_name='是否隐藏')
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    def show_image(self):
        return mark_safe("<img src='{}'>".format(self.image.url))

#课件类
class Chapter(models.Model):
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'chapters', verbose_name=u'老师')
    order = models.PositiveSmallIntegerField(verbose_name=u"序号", blank=False)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    course = models.ForeignKey(Course, on_delete = models.CASCADE,db_constraint=False,
                               related_name=u'chapters',verbose_name=u'课程')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s') % (self.name)

class Lesson(models.Model):
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'lessons', verbose_name=u'老师')
    order = models.PositiveSmallIntegerField(verbose_name=u"序号", blank=False)
    name = models.CharField(max_length=100, verbose_name=u'课时名')
    chapter = models.ForeignKey(Chapter, on_delete = models.CASCADE,verbose_name=u'章节',
                               db_constraint=False, related_name=u'lessons')

    class Meta:
        verbose_name = u'课时'
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s %s') % (self.order,self.name)

class Courseware(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=u"序号", blank=False)
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE,db_constraint=False,
                               related_name=u'coursewares',verbose_name=u'课时')
    teacher = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'coursewares', verbose_name=u'老师')
    file_type = models.CharField(verbose_name=u'文件类型', max_length=10,
                                 choices=(('video', u'视频(mp4)'), ('ppt', u'PPT(ppt、pptx)'), ('document', u'其他文档(pdf、doc、docx、xlsx、xls、jpg、png)')))
    url = models.FileField(max_length=200, verbose_name=u'上传课件', upload_to="courses/files/%Y/%m")

    name = models.CharField(max_length=100, verbose_name=u'课件名')
    class Meta:
        verbose_name = u'课件'
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s %s %s') % (self.order,self.name,self.file_type)

    # 重新save,实现删除对象和数据库时删除media对应的资源文件
    def save(self, *args, **kwargs):
        isUpadte=self.id
        oldURL=''
        if isUpadte:#如果是跟新，先查看保存原先的url
            oldURL=Courseware.objects.get(id=self.id).url
        res = super(Courseware, self).save(*args, **kwargs)
        if isUpadte:
            if self.url != oldURL :
                try:
                    os.remove(oldURL.path)
                    print('文件删除成功')
                except:
                    print('文件不存在')
        return res
    #重新delete,实现删除对象和数据库时删除media对应的资源文件
    def delete(self,*args, **kwargs):
        print(self.url.path)
        filePath=self.url.path
        res=super(Courseware, self).delete(*args, **kwargs)
        # 成功返回一个元组(删除数目，{'appname.modelname': 1)(1, {'courses.Courseware': 1})
        #失败 (0,{‘courses.Courseware’:0})
        if res[0]:
            try:
                os.remove(filePath)
                print('文件删除成功')
            except:
                print('文件不存在')
        return res


class Banner(models.Model):
    """
    轮播的课程
    """
    course = models.ForeignKey(Course, verbose_name="课程",on_delete = models.CASCADE,)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name

User = get_user_model()
#用户学习课程模型
class UserLearningCourseManager(models.Manager):
    pass

class UserLearningCourse(models.Model):
    """
    用户在学课程
    """
    user = models.ForeignKey(User, verbose_name="用户",on_delete = models.CASCADE,related_query_name="learn_courses")
    course = models.ForeignKey(Course, verbose_name="课程", help_text="课程id",on_delete = models.CASCADE,related_query_name="learn_students")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    #软删除标记
    isDelete = models.BooleanField(default=False)
    # objects = UserLearningCourseManager()
    class Meta:
        verbose_name = '选课表'
        verbose_name_plural = verbose_name
        unique_together = ("user", "course")

    def __str__(self):
        #放回选课学生和课程名
        return self.user.nick_name


class CourseGroup(models.Model):
    """
    课程学习小组
    """
    course = models.ForeignKey(Course, verbose_name=u"课程", help_text=u"课程",
                               on_delete=models.CASCADE, )
    member = models.ManyToManyField(UserProfile, verbose_name=u"组员",
                                    related_name="course_groups", related_query_name="course_group")
    number = models.PositiveSmallIntegerField(verbose_name=u"组号", blank=True,null=True)
    name = models.CharField(max_length=100, verbose_name=u'组名',)
    maxNum=models.PositiveSmallIntegerField(verbose_name=u"小组人数上限", blank=True,null=True)

    class Meta:
        verbose_name = '学习小组'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Team(models.Model):
    """
    学习团队
    """
    member = models.ManyToManyField(User, verbose_name=u"队员",
                                    related_name="teams", related_query_name="team")
    number = models.PositiveSmallIntegerField(verbose_name=u"队号", blank=True,null=True)
    name = models.CharField(max_length=100, verbose_name=u'队名',unique=True,help_text='队伍唯一标识')
    introduction=models.TextField(max_length=500, verbose_name=u'团队简介')
    class Meta:
        verbose_name = '学习团队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
