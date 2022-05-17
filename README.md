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

