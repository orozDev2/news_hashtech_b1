from django import forms

from main.models import News


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = News
        fields = (
            'title',
            'category',
            'image',
            'tags',
            'content',
            'author',
        )
        
        label = {
            'title': 'Заголовог'
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'title_inp',
                'placeholder': 'Что произошло? Сформулируйте главное',
                'autocomplete': 'off',
            }),
            'category': forms.Select(attrs={
                'id': 'category_inp',
            }),
            'image': forms.FileInput(attrs={
                'id': 'image_inp',
                'accept': 'image/*',
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'id': 'tags_inp',
                'aria-describedby': 'tags_help',
            }),
            'content': forms.Textarea(attrs={
                'id': 'content_inp',
                'rows': 10,
                'placeholder': 'Расскажите о событии подробнее…',
            }),
            'author': forms.TextInput(attrs={
                'id': 'author_inp',
                'placeholder': 'Имя автора',
                'autocomplete': 'name',
            }),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': ''}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': ''}))
