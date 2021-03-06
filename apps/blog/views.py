from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from apps.blog.models import Blogs, Comments


class PostBlog(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        blog_model = Blogs()
        blog_model.author = request.user.username
        blog_model.title = request.data.get('title')
        blog_model.cls = request.data.get('cls')
        blog_model.tags = request.data.get('tags')
        blog_model.content = request.data.get('data')
        blog_model.likes = 0
        blog_model.dislikes = 0
        blog_model.save()
        return JsonResponse({'data': 'ceed'})


class GetBlog(APIView):

    def get(self, request):
        blogs = Blogs.objects.all()
        blog_list = []
        for blog in blogs:
            time = str(blog.time)
            blog_list.append({
                'id': blog.id,
                'author': blog.author,
                'title': blog.title,
                'cls': blog.cls,
                'tags': blog.tags.split(","),
                'content': blog.content,
                'likes': blog.likes,
                'dislikes': blog.dislikes,
                'visits': blog.visits,
                'comments': blog.comments_num,
                'time': time.strip("." + time.split(".")[-1])
            })
        return JsonResponse({"data": blog_list})
