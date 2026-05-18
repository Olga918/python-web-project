from django import forms
from django.forms import formset_factory, widgets
from django.core.exceptions import ValidationError

choices=[
    (1, "Item1"),
    (2, "Item2"),
    (3, "Item3"),
]

class EventForm(forms.Form):
    title = forms.CharField(
        label="Назва заходу",
        widget=widgets.TextInput(attrs={"class": "validate"}),
    )
    date = forms.DateField(
        label="Дата заходу",
        widget=widgets.DateInput(attrs={"class": "validate", "type": "date"}),
    )


class ParticipantForm(forms.Form):
    email = forms.EmailField(
        label="Email учасника",
        required=False,
        widget=widgets.EmailInput(attrs={"class": "validate"}),
    )


class BaseParticipantFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        emails = []
        for form in self.forms:
            email = form.cleaned_data.get("email")
            if email:
                if email in emails:
                    raise ValidationError("Email учасника не може повторюватися.")
                emails.append(email)

        if not emails:
            raise ValidationError("Додайте хоча б одного учасника.")


ParticipantFormSet = formset_factory(
    ParticipantForm,
    formset=BaseParticipantFormSet,
    extra=1,
    can_delete=False,
)


class UserForm(forms.Form):
    name_field = forms.CharField(label="Name", initial="Tom", widget=widgets.TextInput(
        attrs={"class":"validate"}))
    name_field2 = forms.CharField(label="Name2", widget=widgets.TextInput(
        attrs={"class":"validate"}))
    surname_field = forms.CharField(label="Surname", widget=widgets.TextInput(
        attrs={"class":"validate"}
    ))

class TestForm(forms.Form):
    # BooleanField -> input:checkbox
    # EmailField -> input:email
    # IntegerField/DecimalField/FloatField -> input:number
    
    field_order = ["password","name_field", "surname_field"]
    
    # Output: <input type="text">
    name_field = forms.CharField(label="Name", initial="Tom", help_text="Enter name", widget=widgets.TextInput(
        attrs={"name": 'name_field'}))
    name_field2 = forms.CharField(label="Name2", widget=widgets.TextInput(
        attrs={"name": 'name_field'}))
    surname_field = forms.CharField(label="Surname")
    
    password = forms.CharField(widget=widgets.PasswordInput, label='Password')
    
    about = forms.CharField(widget=widgets.Textarea(attrs={"class":"materialize-textarea"}))
    
    hidden = forms.CharField(widget=widgets.HiddenInput)
    
    # set_item = forms.ChoiceField(choices=choices)
    set_items = forms.MultipleChoiceField(choices=choices)