from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


app_name = 'spider_cam'

urlpatterns = [
    path('', staff_member_required(views.SpiderCamView.as_view(), login_url='/login'), name='spider_cam'),
    path('funny-spider/', staff_member_required(views.FunnySpiderView.as_view(), login_url='/login'), name='funny_spider'),
    path('video_feed/', staff_member_required(views.video_feed, login_url='/login'), name='video_feed'),
]