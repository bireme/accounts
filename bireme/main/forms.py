from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import *
from django import forms

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active')

    type = forms.ChoiceField(label=_("Type"), choices=Profile.USER_TYPE_CHOICES)
        
    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        super(UserForm, self).__init__(*args, **kw)
        # reordering 
        self.fields.keyOrder = ['username', 'email', 'type', 'is_active']

        # allow superuser to edit center code profile field
        if self.request.user.is_superuser:
            selected_cc = self.instance.profile.cooperative_center if self.instance.id else None

            self.fields['cc'] = forms.ModelChoiceField( queryset=CooperativeCenter.objects.all(),
                empty_label=None, initial=selected_cc, label=_("Cooperative Center") )


    def save(self, commit=True, *args, **kw):
        super(UserForm, self).save(commit=True, *args, **kw)
        
        self.instance.profile.type = self.cleaned_data["type"]
        if 'cc' in self.cleaned_data:
            self.instance.profile.cooperative_center = self.cleaned_data["cc"]
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

