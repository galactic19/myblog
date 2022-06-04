from tabnanny import verbose
from django.db import models

# Create your models here.
class Book(models.Model):
    bid = models.IntegerField(primary_key=True) # 책 Id
    title = models.CharField(max_length=50) # 책 제목
    creator = models.CharField(max_length=50) # 저자
    category = models.CharField(max_length=50)
    pages = models.IntegerField()
    price = models.IntegerField()
    published_date = models.DateField() # 출판일
    description = models.TextField()


    class Meta:
        verbose_name = '도서 정보'
        verbose_name_plural = '도서 정보'
        
        
    def get_absolute_url(self):
        pass