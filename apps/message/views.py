from django.http import JsonResponse
from rest_framework.views import APIView

from apps.message.models import Messages


class PostMessage(APIView):
    """发表留言"""
    def post(self, request):
        message_model = Messages()
        message_model.author = request.data.get('user')
        message_model.content = request.data.get('data')
        message_model.save()
        return JsonResponse({'data': 'succeed'})


class GetMessageCount(APIView):
    """获取留言数量"""
    def get(self, request):
        messages = len(Messages.objects.all())
        return JsonResponse({'count': messages})


class GetMessage(APIView):
    """获取留言列表"""
    def get(self, request):
        messages = Messages.objects.all()
        page = int(request.query_params['page'])
        start_index = 0 + (page - 1) * 10
        _end = 10 + (page - 1) * 10
        end_index = _end if _end < len(messages) else len(messages)
        message_list = []
        messages = list(reversed(messages))[start_index:end_index]
        for message in messages:
            time = str(message.time)
            message_list.append({
                'id': message.id,
                'author': message.author,
                'content': message.content,
                'time': time[:-7]
            })
        return JsonResponse({"data": message_list})
