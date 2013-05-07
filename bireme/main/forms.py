from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import *
from django import forms

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser', 'is_active')

    type = forms.ChoiceField(label=_("Type"), choices=Profile.USER_TYPE_CHOICES)
    
    # reaordering 
    def __init__(self, *args, **kw):
        super(UserForm, self).__init__(*args, **kw)
        self.fields.keyOrder = ['username', 'email', 'type', 'is_active', 'is_superuser']

    def save(self, commit=True, *args, **kw):
        super(UserForm, self).save(commit=True, *args, **kw)
        
        self.instance.profile.type = self.cleaned_data["type"]
        self.instance.profile.save()

        return self.instance

class NetworkForm(forms.ModelForm):

    class Meta:
        model = Network
        fields = ('country', 'topic', 'acronym', 'responsible', 'type')


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ( 'name', 'acronym')



class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ( 'name', 'acronym', 'description')

