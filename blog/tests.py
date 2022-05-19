from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import *
# import requests


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.no_post = '작성된 게시물이 없습니다.'
        
    def test_post_list(self):

        #requests 를 사용해, 게시물 번호로 게시물이 있는지 조회를 한다. 서버를 켜고 실행해야 한다.
        # url = 'http://127.0.0.1:8000/blog/post/3'
        # res = requests.get(url)
        # print(res.json())
        
        # 1 포스트 목록 페이지를 가져 온다.
        post_list = self.client.get('/blog/')
        
        # 1-1 정상적으로 페이지가 로드된다.
        self.assertEqual(post_list.status_code, 200)

        # 1-2 페이지 타이틀은 '블로그 : 목록' 이다.
        soup = BeautifulSoup(post_list.content, 'html.parser')
        self.assertEqual(soup.title.text, '블로그 : 목록')

        # 1-3 네비게이션 바를 체크하여 변수에 대입.
        navbar = soup.nav
        
        # 1.4 Blog, About 라는 문구가 네비게이션 바에 있다.
        self.assertIn('Blog', navbar.text, '26라인 메뉴에 메뉴가 없습니다')
        self.assertIn('About', navbar.text, '27라인 메뉴에 메뉴가 없습니다')
        
        
        # 2.1 포스트 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        
        # 2.2 main area에 '작성된 게시물이 없습니다.' 라는 문구가 나타난다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.no_post, main_area.text)
        
        # 3.1 포스트가 2개 있다면
        post_001 = Post.objects.create(title='첫번째 포스트 입니다', content='Hello World')
        post_002 = Post.objects.create(title='두번째 포스트 입니다', content='My Test page')
        self.assertEqual(Post.objects.count(), 2)
        
        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        post_list = self.client.get('/blog/')
        soup = BeautifulSoup(post_list.content, 'html.parser')
        self.assertEqual(post_list.status_code, 200)
        
        # 3.3 main_area에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        
        self.assertNotIn(self.no_post, main_area.text)