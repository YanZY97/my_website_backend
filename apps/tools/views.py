import django.http
import re
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from apps.tools.models import Likes, Visits, Announcement
from apps.user.models import User


class Like(APIView):
    """点赞"""
    def post(self, request):
        likes_model = Likes()
        likes_model.user = request.data.get('user')
        likes_model.save()
        likes_count = len(Likes.objects.all())
        return HttpResponse(likes_count)

    def get(self, request):
        return HttpResponse(len(Likes.objects.all()))


class Visit(APIView):
    """浏览网页"""
    def post(self, request):
        visits_model = Visits()
        visits_model.save()
        return HttpResponse()

    def get(self, request):
        visit_count = len(Visits.objects.all())
        return HttpResponse(visit_count)


class PostAnnouncement(APIView):
    """发布通知"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        announcement = Announcement()
        user = User.objects.get(id=request.user.id)
        announcement.user = user
        announcement.text = request.data.get('text')
        announcement.save()
        return HttpResponse('发布成功')


class GetAnnouncementCount(APIView):
    """获取通知数量"""
    def get(self, request):
        announcements = len(Announcement.objects.all())
        return JsonResponse({'count': announcements})


class GetAnnouncement(APIView):
    """获取通知"""
    def get(self, request):
        announcements = Announcement.objects.all()
        page = int(request.query_params['page'])
        start_index = 0 + (page - 1) * 5
        _end = 5 + (page - 1) * 5
        end_index = _end if _end < len(announcements) else len(announcements)
        announcements_list = []
        announcements = list(reversed(announcements))[start_index:end_index]
        for announcement in announcements:
            time = str(announcement.time)
            announcements_list.append({
                'id': announcement.id,
                'author': announcement.user.username,
                'text': announcement.text,
                'time': time[:-7]
            })
        return JsonResponse({"data": announcements_list})


class EchoChat(APIView):
    def get(self, request):
        command = str(request.query_params['command'])
        return HttpResponse(gen_response(command))


class UploadAction(APIView):
    def get(self, request):
        return HttpResponse(status=200)

    def post(self, request):
        return HttpResponse(status=200)


def gen_response(command: str):
    """
    创建回复内容
    :param command:
    :return:
    """
    if command.startswith('ping '):
        return "<div style='padding: 8px 10px 10px'>pong {}</div>".format(command[5:])
    elif re.match(r'^list (\d+) items$', command):
        response = ''
        num = int(command.split(' ')[1])
        for i in range(num):
            response += ("<li>item {}</li>".format(str(i + 1)))
        return "<div style='padding: 8px 10px 10px'><h4>list：<ul>{}</ul></h4></div>".format(response)
    elif command == 'image':
        return "<img style='width: 100%' src='/api/media/echo_chat.png'>"
    else:
        return "<div style='padding: 8px 10px 10px'>I don't understand {}</div>".format(command)
