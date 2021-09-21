from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = '__all__'


#회원가입폼
class CreateUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")
  def save(self, commit=True):
    user = super(CreateUserForm, self).save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
      user.save()
    return user


#댓글작성폼
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['text']
    labels = {
      'text': '댓글',
    }