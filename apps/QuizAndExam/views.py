from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from QuizAndExam.models import Quiz, QuizAnswerSheet, QuizAnswerRecord, Exam, ExamAnswerRecord, ExamAnswerSheet
from QuizAndExam.serializers import QuizListSerializer, QuizDetailSerializer, \
    QuizAnswerSheetListSerializer, QuizAnswerSheetCreateSerializer, QuizAnswerRecordCreateSerializer, ExamListSerializer, \
    ExamDetailSerializer, ExamAnswerRecordCreateSerializer, ExamAnswerSheetListSerializer, \
    ExamAnswerSheetCreateSerializer
from rest_framework.exceptions import ValidationError

class CommonPagination(PageNumberPagination):
    """考试列表自定义分页"""
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 10

class QuizViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """作业列表页或者详情页"""
    # 这里必须要定义一个默认的排序,否则会报错
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizListSerializer
    pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id', )
    def get_serializer_class(self):
        if self.action == "retrieve":     #详情
            return QuizDetailSerializer   #列表
        elif self.action == "list":
            return QuizListSerializer
        return QuizListSerializer
    def get_queryset(self):
        lesson_id = self.request.query_params.get("lesson_id")
        if lesson_id:
            self.queryset = Quiz.objects.filter(lesson=lesson_id).order_by('id')
        else:
            self.queryset = Quiz.objects.all().order_by('id')
        return self.queryset
class ExamViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """考试列表页或者详情页"""
    queryset = Exam.objects.all().order_by('id')
    serializer_class = ExamListSerializer
    pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id', )
    def get_serializer_class(self):
        if self.action == "retrieve":
            return ExamDetailSerializer
        elif self.action == "list":
            return ExamListSerializer
        return ExamListSerializer
    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if course_id:
            self.queryset = Exam.objects.filter(course=course_id).order_by('id')
        else:
            self.queryset = Exam.objects.all().order_by('id')
        return self.queryset

class QuizAnswerRecordCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuizAnswerRecord.objects.all().order_by('id')
    serializer_class = QuizAnswerRecordCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):#默认为提交答卷的用户
        serializer.save(student=self.request.user)

class ExamAnswerRecordCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ExamAnswerRecord.objects.all().order_by('id')
    serializer_class = ExamAnswerRecordCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):#默认为提交答卷的用户
        serializer.save(student=self.request.user)

class QuizAnswerSheetViewSet(mixins.ListModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    """作业答卷列表页"""
    # 这里必须要定义一个默认的排序,否则会报错
    serializer_class = QuizAnswerSheetListSerializer
    pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', )
    def get_serializer_class(self):
        if self.action == "create":
            return QuizAnswerSheetCreateSerializer
        elif self.action == "list":
            return QuizAnswerSheetListSerializer
        return QuizAnswerSheetListSerializer

    def perform_create(self, serializer):#默认为提交答卷的用户
        queryset=QuizAnswerSheet.objects.filter(student=self.request.user,quiz=serializer.validated_data['quiz']).order_by('id')
        if queryset.exists():
            raise ValidationError('你已经提交过答卷')
        # 注意，调试时不能直接监视 窗口查看整个serializer对象，因为会导致serializer.data也会被访问从而导致下面save失败
        serializer.save(student=self.request.user)
    # 重写queryset,学生只能请求自己填写的答卷
    def get_queryset(self):
        quiz_id = self.request.query_params.get("quiz_id")
        if quiz_id:
            self.queryset = QuizAnswerSheet.objects.filter(student=self.request.user,quiz=quiz_id).order_by('id')
        else:
            self.queryset = QuizAnswerSheet.objects.filter(student=self.request.user).order_by('id')
        return self.queryset

class ExamAnswerSheetViewSet(mixins.ListModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    """考试答卷列表页"""
    pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', )
    def get_serializer_class(self):
        if self.action == "create":
            return ExamAnswerSheetCreateSerializer
        elif self.action == "list":
            return ExamAnswerSheetListSerializer
        return ExamAnswerSheetListSerializer

    def perform_create(self, serializer):  # 默认为提交答卷的用户
        queryset = ExamAnswerSheet.objects.filter(student=self.request.user,
                                                  exam=serializer.validated_data['exam']).order_by('id')
        if queryset.exists():
            raise ValidationError('你已经提交过答卷')
        # 注意，调试时不能直接监视 窗口查看整个serializer对象，因为会导致serializer.data也会被访问从而导致下面save失败
        serializer.save(student=self.request.user)

    def get_queryset(self):
        exam_id = self.request.query_params.get("exam_id")
        if exam_id:
            self.queryset = ExamAnswerSheet.objects.filter(student=self.request.user,exam=exam_id).order_by('id')
        else:
            self.queryset = ExamAnswerSheet.objects.filter(student=self.request.user).order_by('id')
        return self.queryset