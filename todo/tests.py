from django.test import TestCase, Client
from django.contrib.auth.models import User
from todo.models import Article, Todo
from django.urls import reverse


c = Client()


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
        c.login(username='testuser', password='secret')
        response = self.client.get(reverse('currenttodos'))
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        c.login(username='testuser', password='secret')
        response = self.client.get(reverse('currenttodos'))
        self.assertEqual(response.status_code, 302)


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

    def test_update_todo_memo(self):
        todo = Todo.objects.get(id=1)
        todo.memo = "New Memo"
        todo.save()
        self.assertEqual(todo.memo, 'New Memo')


class ArticleTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        c.post('/login/', self.credentials, follow=True)

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

    def test_bookmarked_article_becomes_todo(self):
        response = c.get('/bookmark/324212/')
        todo = Todo.objects.all()

        self.assertTrue(response.status_code, 200)
        self.assertTrue(todo)
