import collections
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.bootstrap import FormActions, PrependedText
from .models import Author, MobilePrice, Post, ContactInfo, Comment
from tinymce import TinyMCE


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column(
                    PrependedText(
                        'email', '@', placeholder="example: john@gmail.com")
                ),
            ),
            Row(
                Column('phone_no'),
                Column('company'),
            ),
            Row(
                Column('messages'),
            ),
            FormActions(
                Submit('send_message', 'Send Messages',
                       css_class='btn-success')
            )
        )


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name'),
            ),
            Row(
                Column('username'),
                Column('email'),
            ),
            Row(
                Column('password1'),
                Column('password2'),
            ),
            FormActions(
                Submit('submit_registerform', 'Register User',
                       css_class='btn-success')
            )
        )


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ("profile_picture",)


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    overview = forms.CharField(widget=TinyMCEWidget(
        attrs={'required': False, 'cols': 30, 'rows': 10}
    )
    )

    content = forms.CharField(widget=TinyMCEWidget(
        attrs={'required': False, 'cols': 30, 'rows': 10}
    )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail',
                  'categories', 'featured')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content', )


class MobilePrice_form(forms.ModelForm):
    model = MobilePrice

    content = forms.CharField(widget=TinyMCEWidget(
        attrs={'required': False, 'cols': 30, 'rows': 10}
    ))
