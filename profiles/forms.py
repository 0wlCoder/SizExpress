from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Profile
from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]


class Editprofileform(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ["address", "parish", "mobilenumber"]  # "trnnumber",


class EditBankInfo(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ["bankname", "branchname", "nameonbankaccount", "accountnumber"]
