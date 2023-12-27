from core.views import CommentViewSet, BlogPostViewSet
from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'post', BlogPostViewSet)
app_name = 'blog'
urlpatterns = [
    path('API', include(router.urls)),
    path('', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
    path('post/add/', views.post_add, name='post_add'),
    path('comment/<int:id>/add/', views.add_comment, name='add_comment'),
]