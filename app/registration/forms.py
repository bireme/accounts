from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class ChangeProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', )