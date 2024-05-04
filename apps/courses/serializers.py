from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator

from courses.models import CourseCategory, Courseware, Lesson, Chapter, Course, Banner, UserLearningCourse, CourseGroup
from users.models import UserProfile
from users.serializers import UserInfoListSerializer


class CategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer1(many=True)
    class Meta:
        model = CourseCategory
        fields = "__all__"

class CoursewareSerializer(serializers.ModelSerializer):
    class Meta :
        model = Courseware
        fields ='__all__'
class LessonSerializer(serializers.ModelSerializer):
    # coursewares = CoursewareSerializer(many=True)#课件
    # coursewares = serializers.StringRelatedField(many=True)
    # test = TestSerializer(many=True)#课后练习
    class Meta :
        model = Lesson
        fields ='__all__'
    def create(self, validated_data):
        coursewares_data = validated_data.pop('coursewares')
        lesson = Chapter.objects.create(**validated_data)
        for courseware_data in coursewares_data:
            Lesson.objects.create(lesson=lesson, **courseware_data)
        return lesson
class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    class Meta :
        model = Chapter
        fields ='__all__'

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        chapter = Chapter.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Chapter.objects.create(chapter=chapter, **lesson_data)
        return chapter
#课程视图
class CourseDetailSerializer(serializers.ModelSerializer):#Hyperlinked ,'url'
    category =CategorySerializer()
    teacher_nick_name = serializers.ReadOnlyField(source='teacher.nick_name')
    org_name = serializers.ReadOnlyField(source='teacher.org.name')
    # examination =ExaminationSerializer(many=True)
    # chapters = serializers.HyperlinkedRelatedField(many=True,view_name='chapter-detail',
    #                                              queryset=Chapter.objects.all())
    chapters = ChapterSerializer(many=True)
    class Meta :
        model = Course
        fields =['id','name','desc','target','teacher','teacher_nick_name','learn_times','degree','stu_num',
                 'fav_nums','image','click_nums','category','tag','readme',
                 'org','org_name','teacher_tell','add_time','chapters']
class CourseListSerializer(serializers.ModelSerializer):#Hyperlinked ,'url'
    teacher_nick_name = serializers.ReadOnlyField(source='teacher.nick_name')
    org_name = serializers.ReadOnlyField(source='teacher.org.name')

    class Meta :
        model = Course
        fields =['id','name','teacher','teacher_nick_name','degree','stu_num',
                 'fav_nums','image','click_nums',
                 'org','org_name','add_time',]
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class UserAllLearningCoursesSerializer(serializers.ModelSerializer):
    course = CourseListSerializer()
    class Meta:
        model = UserLearningCourse
        fields = ("course","id")

class UserIsLearningSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLearningCourse
        fields = ("course","id","user")
class AllLearningUsersSerializer(serializers.ModelSerializer):
    user=UserInfoListSerializer()
    #与UserFavSerializer差异在于我们的goods商品的详细信息
    class Meta:
        model = UserLearningCourse
        fields = ('user',)
class UserLearningCourseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserLearningCourse
        validators = [
            UniqueTogetherValidator(
                queryset=UserLearningCourse.objects.all(),
                fields=('user', 'course'),
                message="已经收藏"
            )
        ]
        fields = ("user", "course", "id")

class MemberSerializer(serializers.ModelSerializer):
    '''用于公共展示教师或者学生信息'''
    # org_name=serializers.ReadOnlyField(source='org.name')
    class Meta:
        model = UserProfile
        fields = ["id","nick_name",]
class CourseGroupSerializer(serializers.ModelSerializer):
    member = MemberSerializer(many=True)
    #与UserFavSerializer差异在于我们的goods商品的详细信息
    class Meta:
        model = CourseGroup
        fields = ('id',"course","member",'number','name','maxNum')


class CourseGroupUpdateSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),write_only=True
    )
    join_or_out=serializers.CharField(write_only=True,help_text='填写: join 或 out')
    class Meta:
        model = CourseGroup
        fields = ['student','join_or_out']
    def update(self, instance, validated_data):
        student = validated_data.pop('student')
        join_or_out=validated_data.pop('join_or_out')
        if join_or_out=='join':
            ret=instance.member.add(student)
            print(ret)
        if join_or_out == 'out':
            ret=instance.member.remove(student)
            print(ret)
        return instance