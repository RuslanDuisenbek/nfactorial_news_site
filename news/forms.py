from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, News


#
# @deconstructible
# class EnglishValidator:
#     allowed_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789- _'
#     code = 'english'
#
#     def __init__(self, message=None):
#         self.message = message if message else "Must be only English letters,scape,line and under line"
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.allowed_symbols)):
#             raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Category has not chosen',
                                 label='Category', required=False)

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Length exceeds 50 characters!")
        return title


class UploadForm(forms.Form):
    file = forms.FileField(label='File')
