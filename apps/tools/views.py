from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from apps.tools.models import Likes, Visits, Announcement


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
    def get(self, request):
        visits_model = Visits()
        visits_model.save()
        visit_count = len(Visits.objects.all())
        return HttpResponse(visit_count)


class PostAnnouncement(APIView):
    """发布通知"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        announcement = Announcement()
        announcement.author = request.user.username
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
                'author': announcement.author,
                'text': announcement.text,
                'time': time[:-7]
            })
        return JsonResponse({"data": announcements_list})

