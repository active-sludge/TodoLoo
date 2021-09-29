from django.test import TestCase, Client
from django.contrib.auth.models import User
from todo.models import Article, Todo
from django.urls import reverse
from todo import pubmed_service
from rest_framework.test import APIRequestFactory

c = Client()


# Create your tests here.
class ViewTestsCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_home_page_accessed_successfully(self):
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_lands_on_home_after_login(self):
        login = self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('currenttodos'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('currenttodos'))
        self.assertEqual(response.status_code, 200)


class LogInTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


class TodoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')

        Todo.objects.create(
            title="Buy milk",
            memo="Low fat if possible",
            user=user
        )

    def test_todo_has_title(self):
        todo = Todo.objects.get(id=1)
        self.assertTrue(todo.title)

    def test_todo_has_memo(self):
        todo = Todo.objects.get(id=1)
        self.assertTrue(todo.memo)

    def test_todo_has_user(self):
        todo = Todo.objects.get(id=1)
        self.assertTrue(todo.user)

    def test_update_todo_meme(self):
        todo = Todo.objects.get(id=1)
        todo.memo = "New Memo"
        todo.save()

        self.assertEqual(todo.memo, 'New Memo')


class ArticleTestCase(TestCase):

    @classmethod
    def setUp(cls):
        User.objects.create_user(username='testuser', password='12345')

        Article.objects.create(
            article_id="324212",
            article_title="Example article Title",
            article_abstract="Example article abstract that is a little bit longer",
            author_list="Ben, Sen, O",
            keyword_list="Aids, covid",
            pub_date="01.02.2004 00:00:00"
        )

    def test_when_api_called_articles_are_saved(self):
        response = c.get('refresh/')
        articles_saved = Article.objects.exists()
        self.assertTrue(response.status_code, 200)
        self.assertTrue(articles_saved)

