
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  viewsets,permissions,filters, mixins
from comments.models import Topics, LevelOneReply
from comments.serializers import TopicsSerializer, LevelOneReplyCreateSerializer, LevelOneReplySerializer

class TopicsViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Topics.objects.all().order_by('public_date_time')
    serializer_class = TopicsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]  #  filters.OrderingFilter
    filterset_fields = ["course"]
    search_fields=['title','content']
    ordering_fields = ['public_date_time',]

class LevelOneReplysViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = LevelOneReply.objects.all().order_by('public_date_time')
    serializer_class = LevelOneReplySerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]  #  filters.OrderingFilter
    filterset_fields = ["topic"]
    search_fields=['content']
    ordering_fields = ['public_date_time',]

    def get_serializer_class(self):
        if self.action == "create":
            return LevelOneReplyCreateSerializer
        return LevelOneReplySerializer


