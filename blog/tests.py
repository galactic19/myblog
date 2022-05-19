from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import *
# import requests


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.no_post = '작성된 게시물이 없습니다.'
        self.user_trump = User.objects.create(username='trump', password='password')
        self.user_obama = User.objects.create(username='obama', password='password')

        self.category_programing = Category.objects.create(name='프로그래밍', slug='프로그래밍')
        self.category_music = Category.objects.create(name='음악', slug='음악')
        
        self.post_001 = Post.objects.create(title='첫번째 포스트 입니다', content='Hello World', author=self.user_trump, category=self.category_programing)
        self.post_002 = Post.objects.create(title='두번째 포스트 입니다', content='My Test page', author=self.user_obama, category=self.category_music)
        self.post_003 = Post.objects.create(title='세번째 포스트 입니다', content='No category', author=self.user_obama)


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
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        home_btn = navber.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navber.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_btn = navber.find('a', text='About')
        self.assertEqual(about_btn.attrs['href'], '/about/')


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
    
        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
    
        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

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
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About', navbar.text)
        self.nav_test(soup)

        # 2-3 첫 번째 포스트의 제목이 웹프라우저 탭 타이틀에 들어있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2-4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)

        # 2-5 첫 번째 포스트의 작성자가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)
        
        # 2-6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)

        