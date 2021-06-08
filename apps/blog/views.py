from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from apps.blog.models import Blogs, Comments
from apps.user.models import User


class PostBlog(APIView):
    """发布文章"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        blog_model = Blogs()
        user = User.objects.get(id=request.user.id)
        blog_model.user = user
        blog_model.title = request.data.get('title')
        blog_model.cls = request.data.get('cls')
        blog_model.tags = request.data.get('tags')
        blog_model.content = request.data.get('data')
        blog_model.abstract = request.data.get('abstract')
        blog_model.likes = 0
        blog_model.dislikes = 0
        blog_model.visits = 0
        blog_model.comments_num = 0
        blog_model.save()
        return JsonResponse({'data': 'succeed'})


class GetBlogCount(APIView):
    """获取文章数量"""
    def get(self, request):
        blogs = len(Blogs.objects.all())
        return JsonResponse({'count': blogs})


class GetBlog(APIView):
    """获取文章列表"""
    def get(self, request):
        blogs = Blogs.objects.all()
        page = int(request.query_params['page'])
        start_index = 0 + (page - 1) * 10
        _end = 10 + (page - 1) * 10
        end_index = _end if _end < len(blogs) else len(blogs)
        blog_list = []
        blogs = list(reversed(blogs))[start_index:end_index]
        for blog in blogs:
            time = str(blog.time)
            blog_list.append({
                'id': blog.id,
                'author': blog.user.username,
                'avatar': blog.user.avatar,
                'title': blog.title,
                'cls': blog.cls,
                'tags': blog.tags.split(","),
                'abstract': blog.abstract,
                'likes': blog.likes,
                'dislikes': blog.dislikes,
                'visits': blog.visits,
                'comments': blog.comments_num,
                'time': time[:-7]
            })
        return JsonResponse({"data": blog_list})


class GetArticle(APIView):
    """获取文章内容"""
    def get(self, request):
        article_id = request.query_params['id']
        article = Blogs.objects.get(id=article_id)
        visits = article.visits
        article.visits = visits + 1
        article.save()
        time = str(article.time)
        data = {
            'id': article.id,
            'author': article.user.username,
            'avatar': article.user.avatar,
            'title': article.title,
            'cls': article.cls,
            'tags': article.tags.split(","),
            'content': article.content,
            'likes': article.likes,
            'dislikes': article.dislikes,
            'visits': article.visits,
            'comments': article.comments_num,
            'time': time[:-7]
        }
        return JsonResponse({'data': data})


class AddComment(APIView):
    permission_classes = [IsAuthenticated]
    """添加评论"""
    def post(self, request):
        article_id = request.data.get('articleid')
        data = request.data.get('data')
        article = Blogs.objects.get(id=article_id)
        user = User.objects.get(id=request.user.id)
        comments_num = article.comments_num
        article.comments_num = comments_num + 1
        article.save()
        comment = Comments()
        comment.user = user
        comment.likes = 0
        comment.dislikes = 0
        comment.article = article
        comment.text = data
        comment.save()
        return HttpResponse('succeed')


class GetComments(APIView):
    """获取评论"""

    def get(self, request):
        article_id = request.query_params['id']
        comments = Comments.objects.filter(article_id=article_id)
        comment_list = []
        for comment in comments:
            time = str(comment.time)
            comment_list.append({
                'id': comment.id,
                'author': comment.user.username,
                'avatar': comment.user.avatar,
                'data': comment.text,
                'likes': comment.likes,
                'dislikes': comment.dislikes,
                'time': time[:-7]
            })
        return JsonResponse({"data": comment_list})


class LikeArticle(APIView):
    """文章点赞"""
    def get(self, request):
        article_id = request.query_params['id']
        article = Blogs.objects.get(id=article_id)
        likes = int(article.likes)
        article.likes = likes + 1
        article.save()
        return HttpResponse(likes + 1)


class DislikeArticle(APIView):
    """文章点踩"""

    def get(self, request):
        article_id = request.query_params['id']
        article = Blogs.objects.get(id=article_id)
        dislikes = int(article.dislikes)
        article.dislikes = dislikes + 1
        article.save()
        return HttpResponse(dislikes + 1)


class LikeComments(APIView):
    """评论点赞"""
    def get(self, request):
        comment_id = request.query_params['id']
        comment = Comments.objects.get(id=comment_id)
        likes = int(comment.likes)
        comment.likes = likes + 1
        comment.save()
        return HttpResponse(likes + 1)


class DislikeComments(APIView):
    """评论点踩"""
    def get(self, request):
        comment_id = request.query_params['id']
        comment = Comments.objects.get(id=comment_id)
        dislikes = int(comment.dislikes)
        comment.dislikes = dislikes + 1
        comment.save()
        return HttpResponse(dislikes + 1)
