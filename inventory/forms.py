from django import forms
from .models import Product,BorrowedProduct
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','desc','total_quantity']

class BorrowedProductForm(forms.ModelForm):
    class Meta:
        model=BorrowedProduct
        fields=['id','product','worker','quantity','due_date']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']