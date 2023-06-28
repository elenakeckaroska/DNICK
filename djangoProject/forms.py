from django.contrib.auth.forms import UserCreationForm
from django.forms import forms, EmailField
from django import forms
from unique_eshop.models import *

from django import forms

class CreditCardForm(forms.Form):
    card_number = forms.CharField(label='Card Number')
    card_expiry = forms.CharField(label='Card Expiry')
    card_cvv = forms.CharField(label='Card CVV')


class ModelNameForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(ModelNameForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = True

        if commit:
            user.save()

        return user


class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            # field.field.widget.attrs["style"] = "width: 5rem;"

    class Meta:
        model = Sale
        fields = ['accessory', ]


class AccessoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccessoryForm, self).__init__(*args, **kwargs)
        # for field in self.visible_fields():
        # field.field.widget.attrs["style"] = "height: 3rem;"
        # field.field.widget.attrs["class"] = "col-5 mx-3 mt-5"

    class Meta:
        model = Accessory
        exclude = ['datetime']


