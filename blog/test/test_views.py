import json
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Post
from ..serializers import BlogPostListSerializer, BlogPostDetailSerializer

User = get_user_model()
client = Client()

class GetAllPostsTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='author #1')
        Post.objects.create(title='First blog post',
                            text='text',
                            author=author)
        Post.objects.create(title='Second blog post',
                            text='text',
                            author=author)
        Post.objects.create(title='Third blog post',
                            text='text',
                            author=author)
    def test_get_all_posts(self, posts=None):
        response = client.get(reverse('blog:post-list'))
        post = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePostTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='test')
        self.post = Post.objects.create(title='First blog post', author=author)

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
        post = Post.objects.get(pk=self.post.pk)
        serializer = BlogPostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = client.get(reverse('blog:post-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewPostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.valid_payload = {
            'title':  'First blog post',
            'text': 'Blog Post Description',
            'author': 1,
        }
        self.invalid_payload = {
            'title': 'First blog post',
            'author': 2,
        }
    def test_create_valid_single_post(self):
        response = client.post(reverse('blog:post-list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_post(self):
        response = client.post(reverse('blog:post-list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='First blog post',
                                        text='Post Description',
                                        author=self.author)
        self.valid_payload = {
            'title': 'First blog post',
            'text': 'Blog Post Description',
            'author': 1,
        }
        self.invalid_payload = {
            'title': 'First blog post',
            'text': None,
            'author': 1,
        }

    def test_valid_update_post(self):
        response = client.post(reverse('blog:post-detail',
                                       kwargs={'pk': self.post.pk}),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        response = client.post(reverse('blog:post-detail',
                                       kwargs={'pk': self.post.pk}),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='First blog post',
                                        text='Post Description',
                                        author=self.author)

    def test_valid_delete_post(self):
        response = client.delete(reverse('blog:post-detail',
                                       kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        response = client.delete(reverse('blog:post-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIClient:
    pass


# class PublishSinglePostTest(TestCase):
#     def setUp(self):
#         self.api = APIClient()
#         self.author = User.objects.create(username='test', password='test')
#         self.post = Post.objects.create(title='First blog post',
#                                         text='Post Description',
#                                         author=self.author,
#                                         is_published=False)
#
#     def test_unauth_publish_post(self):
#         response = client.post(reverse('blog:post-publish', args=[self.post.pk]))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_authenticated_publish_post(self):
#         self.api.force_authenticate(user=self.author)
#         response = self.api.post(reverse('blog:post-publish', args=[self.post.pk]))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         post = Post.objects.get(title='First blog post')
#         self.assertEqual(post.is_published, True)
#
