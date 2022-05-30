from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #  fields , exclude 둘중 하나는 꼭 사용 해야함.
        # fields = ('content',)
        exclude = ('post', 'author', 'created_at', 'modified_at')
        
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id':'id_content'})
        }
        labels = {
            'content': '댓글'
        }


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ('category', 'title','hook_title', 'content', 'post_image', 'post_file')
        
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'hook_title' : forms.TextInput(attrs={'class': 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'id':'id_content'}),
            'post_image' : forms.FileInput(attrs={'class': 'form-control'}),
            'post_file' : forms.FileInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
        }
        
        labels = {
             'title':'제목',
             'hook_title' : '부제, 요약',
             'content': '내용',
             'post_image':'메인 이미지',
             'post_file' : '첨부 파일',
             'category': '카테고리 선택'
        }
        