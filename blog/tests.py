from unicodedata import category
from urllib import response
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
import os
from .models import *
# import requests


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.no_post = '작성된 게시물이 없습니다.'
        self.user_trump = User.objects.create_user(username='trump', password='password')
        self.user_obama = User.objects.create_user(username='obama', password='password')
        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programing = Category.objects.create(name='프로그래밍', slug='프로그래밍')
        self.category_music = Category.objects.create(name='음악', slug='음악')
        
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(title='첫번째 포스트 입니다', content='Hello World', author=self.user_trump, category=self.category_programing)
        self.post_001.tags.add(self.tag_hello)
        self.post_002 = Post.objects.create(title='두번째 포스트 입니다', content='My Test page', author=self.user_obama, category=self.category_music)
        self.post_003 = Post.objects.create(title='세번째 포스트 입니다', content='No category', author=self.user_obama)
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)
        
        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='첫 번째 댓글입니다.'
        )
        
    


    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)

        self.assertIn(f'{self.category_programing.name} ({self.category_programing.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)
        
        
    def nav_test(self, soup):
        navber = soup.nav
        self.assertIn('Blog', navber.text)
        self.assertIn('About', navber.text)
        
        logo_btn = navber.find('a', text='Beom\'s')
        self.assertEqual(logo_btn.attrs['href'], '/blog/')
        
        home_btn = navber.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/blog/')

        blog_btn = navber.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_btn = navber.find('a', text='About')
        self.assertEqual(about_btn.attrs['href'], '/about/')


    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.nav_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.text)
        
        main_area = soup.find('div',id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)

        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)


    def test_post_list(self):
        # 포스트(글)가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        respone = self.client.get('/blog/')
        self.assertEqual(respone.status_code, 200)
        soup = BeautifulSoup(respone.content, 'html.parser')

        self.nav_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn(self.no_post, main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
    
        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
    
        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)        
        

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)


        # 포스트(글)가 없는경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        respone = self.client.get('/blog/')
        soup = BeautifulSoup(respone.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.no_post, main_area.text)
    
    

    def test_post_detail(self):
        # 1-1 포스트가 하나 있다.
        # self.post_001 = Post.objects.create(title='첫 번째 포스트 입니다.',content='첫번째 내용 테스트 입니다.', author=self.user_trump)
        
        # 1-2 포스트의 url은 /blog/1/ 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')
        
        # 2-1 첫 번째 포스트의 상세 페이지 테스트
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2-2 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다 (state_code : 200)
        self.nav_test(soup)
        self.category_card_test(soup)

        # 2-3 첫 번째 포스트의 제목이 웹프라우저 탭 타이틀에 들어있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2-4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programing.name, post_area.text)

        # 2-5 첫 번째 포스트의 작성자가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)
        
        # 2-6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
        
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)
        
        # 코멘트
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
        


    def test_category_page(self):
        response = self.client.get(self.category_programing.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.nav_test(soup)
        self.category_card_test(soup)

        category_bar = soup.find('h1', id='category_area')
        self.assertIn(self.category_programing.name, category_bar.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programing.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)


    def test_create_post(self):
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # 스텝이 아닌 트럼프가 로그인을 한다
        self.client.login(username='trump', password='password')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # 스텝이 로그인 한다.
        self.client.login(username='obama', password='password')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Blog Create New Post', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)
        
        
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        
        
        self.client.post('/blog/create_post/',
            {
                'title':'Post Form 만들기',
                'content' : 'Post Form 페이지 만들어보기',
                'tags_str' : 'new tag; 한글 태그, python',
            }
        )

        self.assertEqual(Post.objects.count(), 4)
        # last_post = Post.objects.last() # models.py 에 Meta 에 ordering 를 -created_at 로 지정해서 first 를 사용함.
        last_post = Post.objects.first()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, "obama")
        
        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)
        
    
    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'
        
        # 로그인 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인 했지만 작성자 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        # self.client.login(username=self.user_trump.username, password='password')
        self.client.login(username='trump', password='password')
        
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        
        # 작성자가 접근하는 경우
        self.client.login(username=self.post_003.author.username, password='password')
        
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Blog Edit Post', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn(' Edit Post', main_area.text)
        
        
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])
        

        response = self.client.post(update_post_url, 
            {
                'title': '세 번째 포스트를 수정 했습니다..',
                'content': '안녕 세계? 우리는 하나',
                'category': self.category_music.pk,
                'tags_str':'파이썬 공부; 한글 태그, some tag',
            },
            follow = True
        )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정 했습니다..', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)