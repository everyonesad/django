from rest_framework import serializers, viewsets
from .models import Comment, Post
# from .models import Comment

class CommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    created_date = serializers.DateTimeField()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'created_date', 'text', 'approved')

class BlogPostListSerializer(serializers.ModelSerializer):

    # def get_preview_text(self, post):
    #     return post.get_text_preview()

    class Meta:
        model = Post
        fields = ('title', 'author', 'created_date')

class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'published_date', 'comments')

class BlogPostListSerializer(serializers.ModelSerializer):

    # def get_preview_text(self, post):
    #     return post.get_text_preview()

    class Meta:
        model = Post
        fields = ('title', 'author', 'created_date')


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ()
