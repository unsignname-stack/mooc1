
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  viewsets,permissions,filters, mixins
from .serializers import *
from .filters import CourseFilter, CategoryFilter, CoursewareFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from courses.models import Course
from rest_framework.response import Response

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 只有该course的所有者才允许读写写权限。
        return obj.teacher == request.user
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
class CoursewareViewSet(viewsets.ReadOnlyModelViewSet):#CacheResponseMixin,viewsets.ReadOnlyModelViewSet
    queryset = Courseware.objects.all().order_by('id')
    serializer_class = CoursewareSerializer
    filter_class = CoursewareFilter

    def get_queryset(self):
        lesson = self.request.query_params.get("lesson_id")
        if lesson:
            self.queryset = Courseware.objects.filter(lesson=lesson).order_by('order')
        return self.queryset

class LessonViewSet(viewsets.ReadOnlyModelViewSet):#viewsets.ReadOnlyModelViewSet
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):#viewsets.ReadOnlyModelViewSet
    queryset = Chapter.objects.all().order_by('id')
    serializer_class = ChapterSerializer

class CoursePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100

#所有课程视图
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_hide=False).order_by('id')
    pagination_class = CoursePagination
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filter_class = CourseFilter
    search_fields = ['name', ]
    ordering_fields = ['id', 'add_time']
    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer
    def retrieve(self, request, *args, **kwargs):
        #通过get_object可以拿到course的实例（模型类对象）
        instance = self.get_object()
        instance.click_nums += 1#对点击数加1并保存
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        课程分类列表数据
    retrieve:
        获取课程分类详情
    """
    queryset = CourseCategory.objects.all().order_by('id')#filter(category_type=1)
    serializer_class = CategorySerializer
    filter_class = CategoryFilter

class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer
#用户在学课程视图
# Create your views here.
#CreateModelMixin是搞添加收藏，DestroyModelMixin是搞删除收藏
class UserLearningCourseViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
    list:获取用户收藏列表
    retrieve:判断某个课程是否已经收藏
    create:收藏课程
    '''
    queryset = UserLearningCourse.objects.all().order_by('id')  #查询数据集合
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly) #验证是否登录
    # lookup_field = "course_id" #定义pk
    def get_queryset(self):
        # return UserLearningCourse.objects.all().order_by('id')
        course_id = self.request.query_params.get("course_id")
        if course_id:
            get_all_users = self.request.query_params.get("get_all_users")
            if get_all_users:#查看该课程所有学生
                return UserLearningCourse.objects.filter(course_id=course_id).order_by('id')  # 查看该课程所有用户
            # 用于检测该用户是否关注该课程
            return UserLearningCourse.objects.filter(course_id=course_id,user = self.request.user).order_by('id')
        else:#返回该用户所有关注课程
            return UserLearningCourse.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        instance = serializer.save()#得到serializer
        course = instance.course
        course.fav_nums += 1#对收藏数加1
        course.stu_num +=1 #学习人数加一
        course.save()
    def perform_destroy(self, instance):
        course = instance.course
        course.fav_nums -= 1  # 对收藏数减1
        course.save()
        instance.delete()

    def get_serializer_class(self):
        if self.action == "list":
            course_id = self.request.query_params.get("course_id")
            if course_id:
                get_all_users = self.request.query_params.get("get_all_users")
                if get_all_users:
                    return AllLearningUsersSerializer #查看该课程所有用户
                return UserIsLearningSerializer  #判断用户是否关注
            else :
                return UserAllLearningCoursesSerializer #查看用户所有关注课程
        elif self.action == "create":
            return UserLearningCourseSerializer

        return UserLearningCourseSerializer


class CourseGroupViewSet(viewsets.ModelViewSet):#viewsets.ReadOnlyModelViewSet
    queryset = CourseGroup.objects.all().order_by('id')
    serializer_class = CourseGroupSerializer

    def perform_update(self, serializer):
        serializer.save()
    def get_queryset(self):

        if self.action == "list":
            course = self.request.query_params.get("course_id")
            if course:
                return CourseGroup.objects.filter(course_id=course).order_by('id')
            else:
                return CourseGroup.objects.filter(course_id=0).order_by('id')
        else:
            return self.queryset
    def get_serializer_class(self):
        if self.action == "update":
            return CourseGroupUpdateSerializer
        return CourseGroupSerializer




