from django.db import models
from courses.models import  Course
import uuid
class Topics(models.Model):
    """课程讨论帖子"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'topic', verbose_name=u'发布者')
    course=models.ForeignKey(Course, on_delete=models.CASCADE, db_constraint=False,
                                related_name=u'topic', verbose_name=u'归属课程')
    title=models.CharField(verbose_name=u'标题',max_length=30)
    content = models.TextField(verbose_name=u"内容", )
    public_date_time = models.DateTimeField("发布日期时间")
    class Meta:
        ordering = ['public_date_time']
        verbose_name = '话题'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class TopicPicture(models.Model):
    """Topic插图"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, db_constraint=False,
                                 related_name='topic_picture', verbose_name=u'归属话题')
    picture_name = models.CharField("插图名字", max_length=20, )
    picture = models.ImageField(upload_to="comments/pictures/", verbose_name=u"插图", blank=True,
                                null=True,)
    class Meta:
        ordering = ['id']
        verbose_name = '话题插图'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.picture_name

class LevelOneReply(models.Model):
    '''一级回帖'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                              related_name='level_one_reply', verbose_name=u'回复者')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, db_constraint=False,
                              related_name='level_one_reply', verbose_name=u'话题')
    content = models.TextField(verbose_name=u"内容", )
    public_date_time = models.DateTimeField("发布日期时间")
    class Meta:
        ordering = ['public_date_time']
        verbose_name = '一级回帖'
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s %s') % (self.owner,self.public_date_time)


class LevelTwoReply(models.Model):
    '''二级回帖'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, db_constraint=False,
                              related_name='level_two_reply', verbose_name=u'回复者')
    level_one_reply = models.ForeignKey(LevelOneReply, on_delete=models.CASCADE, db_constraint=False,
                              related_name='level_one_reply', verbose_name=u'一级回帖')
    content = models.TextField(verbose_name=u"内容", )
    public_date_time = models.DateTimeField("发布日期时间")
    class Meta:
        ordering = ['public_date_time']
        verbose_name = '二级回帖'
        verbose_name_plural = verbose_name
    def __str__(self):
        return ('%s %s') % (self.owner,self.public_date_time)