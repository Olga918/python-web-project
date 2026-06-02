from django import forms
from .models import Product, Category, Tag

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price','category', 'tags']
        
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(),
            'price': forms.NumberInput(),
            
            'category': forms.Select(),
            'tags': forms.CheckboxSelectMultiple()
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if('category' in self.fields.keys()):
            self.fields['category'].empty_label = "Оберіть категорію"
            self.fields['category'].queryset = Category.objects.filter(deleted_at=None)
        
    