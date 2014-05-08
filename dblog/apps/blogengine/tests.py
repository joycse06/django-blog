from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from dblog.apps.blogengine.models import Post, Category
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Create your tests here.


class PostTest(TestCase):
    def test_create_category(self):
        # Create Post Category
        category = Category()

        # fill the category attributes
        category.name = 'Python'
        category.description = 'Python is a rad dynamic programming language'
        category.save()

        # Now test category creation
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category, category)

        #check Attributes 
        self.assertEquals(only_category.name, 'Python')
        self.assertEquals(only_category.description, 'Python is a rad dynamic programming language')

    def test_create_post(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'pass')
        author.save()

        # Create the category
        category = Category()
        category.name = 'Python'
        category.description = 'Python is a rad dynamic programming language'
        category.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = "My First Post"
        post.text = 'This is my first blog post. Hope you like this thing'
        post.slug = 'my-first-post'
        post.site = site
        post.pub_date = timezone.now()
        post.author = author
        post.category = category
        post.save()

        # check we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check Attributes
        self.assertEquals(only_post.title, 'My First Post')
        self.assertEquals(only_post.text, 'This is my first blog post. Hope you like this thing')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        # Skip month year, hour and minute
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)
        self.assertEquals(only_post.author.username, 'testuser')
        self.assertEquals(only_post.author.email, 'user@example.com')
        self.assertEquals(only_post.category.name, 'Python')
        self.assertEquals(only_post.category.description, 'Python is a rad dynamic programming language')


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def setup(self):
        self.client = Client()

    def test_login(self):
        # Create Client

        #get the login page
        response = self.client.get('/admin/')

        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log in' in response.content)

        # Log the user in
        self.client.login(username='joy', password='pass')

        #check the response code
        response = self.client.get('/admin/')
        # print response
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in the response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Create client

        #Log In
        self.client.login(username='joy', password='pass')

        #check the response
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # check log out in response
        self.assertTrue('Log out' in response.content)

        #Log out

        self.client.logout()

        # check response code

        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response

        self.assertTrue('Log in' in response.content)

    def test_create_post(self):
        #log in
        self.client.login(username='joy', password="pass")

        # Create the category
        category = Category()
        category.name = 'Python'
        category.description = 'Python is a rad language'
        category.save()

        #Check response code

        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', {
            'title': 'My First Post',
            'text': 'This is my first Post',
            'pub_date_0': '2014-04-06',
            'pub_date_1': '22:00:04',
            'slug': 'my-first-post',
            'site': 1,
            'author': 1
        },
                                    follow=True)

        self.assertEquals(response.status_code, 200)
        # check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new post now in database

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'pass')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the category
        category = Category()
        category.name = 'Python'
        category.description = 'Python is a rad language'
        category.save()
        # Create the post

        post = Post()
        post.title = 'My First Post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.site = site
        post.pub_date = timezone.now()
        post.author = author
        post.category = category
        post.save()

        # Log in
        self.client.login(username='joy', password='pass')

        # Edit the Post
        response = self.client.post('/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'This is my second blog post',
            'pub_date_0': '2014-05-06',
            'pub_date_1': '22:00:04',
            'slug': 'my-second-post',
            'site': 1,
            'author': 1,
            'category': 1
        }, follow=True)

        self.assertEquals(response.status_code, 200)

        # check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check post amended

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My second post')
        self.assertEquals(only_post.text, 'This is my second blog post')

    def test_delete_post(self):
        #create author
        author = User.objects.create_user('testuser', 'user@example.com', 'pass')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the category
        category = Category()
        category.name = 'Python'
        category.description = 'Python is a rad language'
        category.save()

        #create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.site = site
        post.pub_date = timezone.now()
        post.author = author
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Log in
        self.client.login(username='joy', password='pass')

        # Delete the post
        response = self.client.post('/admin/blogengine/post/1/delete/', {
            'post': 'yes'}, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

    def test_create_category(self):
        #Log in
        self.client.login(username='joy', password='pass')

        response = self.client.get('/admin/blogengine/category/add/')
        self.assertEquals(response.status_code, 200)

        # Create the category
        response = self.client.post('/admin/blogengine/category/add/', {
            'name': 'Pyton',
            'description': 'Python is a rad language'
        }, follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check the new category now in database

        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category

        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='joy', password="pass")

        # Edit the category
        response = self.client.post('/admin/blogengine/category/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'perl')
        self.assertEquals(only_category.description, 'The Perl programming language')


    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='joy', password="pass")

        # Delete the category
        response = self.client.post('/admin/blogengine/category/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)


class PostViewTest(BaseAcceptanceTest):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'pass')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()
        #Create the Post
        post = Post()
        post.title = 'My First post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.site = site
        post.author = author
        post.pub_date = timezone.now()
        post.save()

        # Check the new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        # check the post title is in the response
        self.assertTrue(post.title in response.content)

        # check whether the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_post_page(self):
        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'pass')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        #Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000)'
        post.slug = 'my-first-post'
        post.site = site
        post.pub_date = timezone.now()
        post.author = author
        post.save()

        #Check the new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the post url
        post_url = only_post.get_absolute_url()

        #Fetch the post
        response = self.client.get(post_url)
        self.assertEquals(response.status_code, 200)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post')

    def test_category_page(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the category URL
        category_url = post.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)


class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)

        only_page = all_pages[0]
        self.assertEquals(only_page, page)

        # Check data correct
        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'About me')
        self.assertEquals(only_page.content, 'All about me')

        # Get URL
        page_url = only_page.get_absolute_url()

        # Get the page
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)

        # Check title and content in response
        self.assertTrue('About me' in response.content)
        self.assertTrue('All about me' in response.content)













