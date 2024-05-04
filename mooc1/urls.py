"""mooc1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, re_path,include

import xadmin
from QuizAndExam.views import QuizAnswerSheetViewSet, QuizViewSet, \
    QuizAnswerRecordCreateViewSet, ExamViewSet, ExamAnswerSheetViewSet, ExamAnswerRecordCreateViewSet
from comments.views import TopicsViewSet, LevelOneReplysViewSet
from courses.views import *

from rest_framework.routers import DefaultRouter
from mooc1.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token

from users.views import UserViewSet, SmsCodeViewSet, OrganizationViewSet, PasswordUpdateViewSet, UserInfoShowViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, base_name='user')
router.register(r'codes', SmsCodeViewSet, base_name="codes")
router.register(r'password', PasswordUpdateViewSet, base_name="password")
router.register(r'user-info-show', UserInfoShowViewSet, base_name="user-info-shows")


router.register(r'learning-courses', UserLearningCourseViewset, base_name="learning-course")
router.register(r'category',CategoryViewset,base_name='category')
router.register(r'courses', CourseViewSet, base_name='course')
router.register(r'groups', CourseGroupViewSet, base_name='group')

router.register(r'organizations', OrganizationViewSet, base_name='organization')
router.register(r'chapters', ChapterViewSet, base_name='chapter')
router.register(r'lessons', LessonViewSet, base_name='lesson')
router.register(r'coursewares', CoursewareViewSet, base_name='courseware')
router.register(r'banners', BannerViewset, base_name="banners")

router.register(r'topics', TopicsViewSet, base_name="topic")
router.register(r'level_one_replys', LevelOneReplysViewSet, base_name="level_one_reply")

router.register(r'quiz', QuizViewSet, base_name='quiz')
router.register(r'exams', ExamViewSet, base_name='exam')
router.register(r'quiz_answer_sheets', QuizAnswerSheetViewSet, base_name='quiz_answer_sheet')
router.register(r'exam_answer_sheets', ExamAnswerSheetViewSet, base_name='exam_answer_sheet')
router.register(r'quiz_answer_records', QuizAnswerRecordCreateViewSet, base_name="quiz_answer_record")
router.register(r'exam_answer_records', ExamAnswerRecordCreateViewSet, base_name="exam_answer_record")

from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView

urlpatterns = [
    # path('test/xadmin',xadmin.site.urls ),
    # path('test/api',include(router.urls) ),
    # path('test/aimooc/', TemplateView.as_view(template_name='index.html'), name="mooc1"),
    # path('test/login/', obtain_jwt_token),

    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls(title="aimooc API文档")),
    path('api/',include(router.urls)),
    path('aimooc/', TemplateView.as_view(template_name='index.html'), name="mooc1"),
    # path('',include(router.urls)),
#配置下面路由链接才有登录效果
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),#配置资源路由
    #(?P<path>.*)$' 作用：捕获请求路径media/之后的路径，赋值给变量page,page将传递给serve函数的path参数
    path('api/login/', obtain_jwt_token),
]
