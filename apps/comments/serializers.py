from rest_framework import serializers

from comments.models import Topics, TopicPicture, LevelOneReply
from users.models import UserProfile
from users.serializers import UserInfoListSerializer
import datetime

class TopicPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicPicture
        fields = '__all__'

class LevelOneReplySerializer(serializers.ModelSerializer):
    owner = UserInfoListSerializer()
    class Meta:
        model = LevelOneReply
        fields = ('id', "owner", "topic", 'content', 'public_date_time',)

class LevelOneReplyCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    public_date_time = serializers.HiddenField(
        default=datetime.datetime.now()
    )
    class Meta:
        model = LevelOneReply
        fields = ("owner", "topic", 'content', 'public_date_time',)

class UserSerializer(serializers.ModelSerializer):
    '''用于公共展示教师或者学生信息'''
    org_name=serializers.ReadOnlyField(source='org.name')
    class Meta:
        model = UserProfile
        fields = ["id","nick_name",'image','category','org','org_name']
class TopicsSerializer(serializers.ModelSerializer):
    topic_picture = TopicPictureSerializer(many=True)
    level_one_reply=LevelOneReplySerializer(many=True,read_only=True)
    owner=UserInfoListSerializer()
    class Meta:
        model = Topics
        fields = ('id',"owner","course",'title','content','public_date_time',
                  'topic_picture','level_one_reply',)#
