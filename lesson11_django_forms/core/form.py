from django import forms
from django.forms import widgets

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description", "release_date", "country", "poster"]
        labels = {
            "title": "Назва фільму",
            "description": "Опис фільму",
            "release_date": "Дата виходу",
            "country": "Країна",
            "poster": "Постер",
        }
        widgets = {
            "title": widgets.TextInput(attrs={"class": "validate"}),
            "description": widgets.Textarea(attrs={"class": "materialize-textarea"}),
            "release_date": widgets.DateInput(attrs={"class": "validate", "type": "date"}),
            "country": widgets.TextInput(attrs={"class": "validate"}),
        }


class UserForm(forms.Form):
    
    error_css_class = "error-text"
    
    name = forms.CharField(max_length=100, required=True, label="First Name", 
                           widget=widgets.TextInput(attrs={
                               "placeholder": "First Name",
                               "class": "validate"
                           }))
    surname = forms.CharField(max_length=100, required=True, label="Second Name",
                              widget=widgets.TextInput(attrs={
                                  "class":"validate"
                              }))
    age = forms.IntegerField(min_value=18, required=True, label="Age",
                              widget=widgets.NumberInput(attrs={
                                  "class":"validate"
                              }))
    picture = forms.ImageField(required=False)
    
    # clean_<field_name>
    
    # Валідація для конкретного поля, пілся clean_ підставляйте назву свого поля
    def clean_name(self):
        data = self.cleaned_data["name"]
        
        if "joe" in str(data).lower():
            self.add_error("name", "Contains 'joe'")
            return data
        return data
    
    # Валідація всієї форми
    def clean(self):
        result = super().clean()
        surname = result.get("surname")
        if surname and "due" in str(surname).lower():
            self.add_error("surname", "Contains 'due'")
        return result