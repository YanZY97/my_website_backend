import base64
import numpy as np
import cv2
import os
from django.http import JsonResponse
from rest_framework.views import APIView

from my_website_backend import settings
from apps.message.models import Messages, MessagePictures
from apps.user.models import User


class PostMessage(APIView):
    """发表留言"""
    def post(self, request):
        images = request.data.get('images')
        message_model = Messages()
        user = User.objects.get(username=request.data.get('user'))
        message_model.user = user.id
        message_model.content = request.data.get('data')
        message_model.save()
        message_id = message_model.id
        for image in images:
            img_name = image['name']
            image_b64 = image['imageb64'].split(',')[1]
            image_data = base64.b64decode(image_b64)
            image_array = np.fromstring(image_data, np.uint8)
            img = cv2.imdecode(image_array, cv2.COLOR_RGB2BGR)
            img_dir = os.path.join(settings.BASE_DIR, 'media', 'message_images', str(message_id))
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            img_path = os.path.join(img_dir, img_name)

            cv2.imwrite(img_path, img)
            img_url = '/api/' + os.path.join('media', 'message_images', str(message_id), img_name)
            message_pictures = MessagePictures()
            message_pictures.message = message_model
            message_pictures.url = img_url
            message_pictures.save()
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
            try:
                user = User.objects.get(id=message.user)
                author = user.username
                avatar = user.avatar
                signature = user.signature
            except:
                author = ''
                avatar = ''
                signature = ''
            message_pics = MessagePictures.objects.filter(message=message)
            pic_list = []
            for message_pic in message_pics:
                pic_list.append(message_pic.url)
            message_list.append({
                'id': message.id,
                'author': author,
                'avatar': avatar,
                'signature': signature,
                'content': message.content,
                'pictures': pic_list,
                'time': time[:-7]
            })
        return JsonResponse({"data": message_list})


