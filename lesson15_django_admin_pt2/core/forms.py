from django import forms
from .models import Product, Category, Tag, MyUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = MyUser
        fields = "__all__"

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label = "Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label = "Підтвердіть пароль"
    )
    birth_date = forms.DateField(required=False, label="Дата народження")
    
    def clean_password(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 != pass2:
            self.add_error("password1", "Паролі не співпадають")
            return None
        return pass1
    def save(self, commit = True):
        user = super().save(False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    class Meta:
        model = MyUser
        fields = '__all__'

class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

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
        
    