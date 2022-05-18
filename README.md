# myblog
간단한 블로그를 구현해 보면서, 중요한 부분들을 기록하며 진행 한다.

***

## 이미지 파일등 파일들을 처리해줄때.
###### settings.py 파일에 처리

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

###### urls.py 파일에 설정(root 파일에 처리)

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

***


## 이미지 파일이 없을 때 외부 사이트 랜덤이미지 사용하기.

[https://picsum.photos/](https://picsum.photos/)


***

## user 정보를 가져오는 django 기본 모듈
`models.py` 에서 처리한다.

    from django.contrib.auth.models import User

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


***

## 테스트 주도 코딩 (tests.py 파일을 활용해 test 하는 방법)
테스트 코드 작성하기 위해 필요한 것.  `tests.py`

    from django.test import TestCase, Client
    from bs4 import BeautifulSoup
    from .models import *

```
    class TestView(TestCase):
        def setUp(self):
            self.client = Client()
        
        def test_post_list(self):
            # 코드 리뷰를 하듯 주석으로 먼저 로직을 작성하여
            # 써내려 가며, 앞으로 작성 해야할 방향대로 테스트 코드를 작성해 본다.

```

***

## 테스트 주도 코딩을 위한 간단한 코드 및 코드리뷰
코드를 테스트 하며 한다는것은 복잡하지만 생각해보면 그렇게 어려운 일은 아니다.

함수의 네이밍에 규칙이 있는것 같다.
함수의 이름을 바꾸고 테스트 해보니 작동되지 않는다.
네이밍의 규칙이 test_모델명_list 인가 ....

아래는 간단하게 작성해본 테스트 코드(참고용으로 올림.)
```
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import *


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.no_post = '작성된 게시물이 없습니다.'
        
    def test_post_list(self):
        # 1 포스트 목록 페이지를 가져 온다.
        post_list = self.client.get('/blog/')
        
        # 1-1 정상적으로 페이지가 로드된다.
        self.assertEqual(post_list.status_code, 200)

        # 1-2 페이지 타이틀은 '블로그 : 목록' 이다.
        soup = BeautifulSoup(post_list.content, 'html.parser')
        self.assertEqual(soup.title.text, '블로그 : 목록')

        # 1-3 네비게이션 바가 있다.
        navbar = soup.nav
        
        # 1.4 Blog, About 라는 문구가 네비게이션 바에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About', navbar.text)
        
        
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

```



***

## 업로드된 파일을 첨부. (다운로드 기능)
파일을 첨부하고 파일 다운로드 가능하게 처리하는 부분이다.
파일을 처리해 주기위해 조금의 수고스러움은 필요 했다.

파이썬에서 os 모듈을 import 파일 명만 골라내고 파일의 확장자도 골라낸다.

`models.py` 파일에서 처리 한다.
Views.py 파일도 있지만 데이터와 관련되어 바로 처리할 것이 있으면 models.py 에서 처리한다.
os 모듈을 사용해서 아래와 같이 models.py 에 함수를 만들어 처리한다.

```
    def get_file_name(self):
        return os.path.basename(self.post_file.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

```

template html 파일에서 이렇게 사용할 수 있다.
```
    <a href="psot.post_file.url">{{ post.get_file_name }}</a>
```

get_file_name에서 os 모듈을 사용해 경로를 제거한 파일명만 return 한다.
get_file_ext 함수에서는 get_file_name 의 값을 가져와 확장자만 떼어낸다.

get_file_name 에서 사용된 basename 는 os에서 제공하는 메서드다 .
여기 링크를 참고하자.
[https://devanix.tistory.com/298](https://devanix.tistory.com/298)

