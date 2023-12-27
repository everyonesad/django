from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.models import Comment, Post
from blog.serializers import CommentSerializer, BlogPostListSerializer, BlogPostDetailSerializer, \
    BlogPostCreateUpdateSerializer


class ActionSerializedViewSet(viewsets.ModelViewSet):
    """
    provides custom serializer for specific viewsets action
    declate serializer in dict:
    action_serializers = {
        'list': ReportListSerializer,
        'retrieve': ReportPostPutSerializer,
        'create': ReportPostPutSerializer,
        'update': ReportPostPutSerializer,
        'partial_update': ReportPostPutSerializer,
    }
    """

    action_serializers = []

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return self.serializer_class

class BlogPostViewSet(ActionSerializedViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()

    action_serializers = {
        'list': BlogPostListSerializer,
        'retrieve': BlogPostDetailSerializer,
        'create': BlogPostCreateUpdateSerializer,
        'update': BlogPostCreateUpdateSerializer,
    }

    @action(detail=False)
    def published_posts(self, request):
        published_posts = Post.published.all()

        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()