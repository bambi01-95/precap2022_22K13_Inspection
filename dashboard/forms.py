# アンケートフォームなどの形式作成
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','quantity','thresh','width','height']
