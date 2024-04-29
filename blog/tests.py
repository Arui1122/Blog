from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

class PostModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='A good title',
            content='Nice body content',
            author=self.user
        )

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.content}', 'Nice body content')
        self.assertEqual(f'{self.post.author}', 'testuser')


class BlogUrlsTest(TestCase):

    def test_blog_home_url_resolves(self):
        url = reverse('blog-home')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_blog_post_detail_url_resolves(self):
        url = reverse('post-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)


class BlogViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='A good title',
            content='Nice body content',
            author=self.user
        )

    def test_blog_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_user_posts_view(self):
        response = self.client.get(reverse('user-posts', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'blog/user_posts.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_update_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')


class LoginRequiredViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_required_for_post_create_view(self):
        response = self.client.get(reverse('post-create'))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith('/login/'))

    def test_login_required_for_post_update_view(self):
        url = reverse('post-update', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith('/login/'))

    def test_login_required_for_post_delete_view(self):
        url = reverse('post-delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith('/login/'))
