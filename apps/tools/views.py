from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.http import HttpResponse

from apps.tools.models import Likes


class Like(GenericAPIView):
    def post(self, request):
        likes_model = Likes.objects.get(id=1)
        likes = likes_model.count
        likes_model.count = likes + 1
        likes_model.save()
        return HttpResponse(likes + 1)

    def get(self, request):
        return HttpResponse(Likes.objects.get(id=1).count)
