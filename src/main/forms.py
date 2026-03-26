#! coding: utf-8
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from main.models import *
from django import forms

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active')

    type = forms.ChoiceField(label=_("Type"), choices=Profile.USER_TYPE_CHOICES)

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        super(UserForm, self).__init__(*args, **kw)
        # reordering - keyOrder is deprecated, using fields order
        field_order = ['username', 'email', 'type', 'is_active']

        if hasattr(self.instance, 'profile'):
            self.fields['type'].initial = self.instance.profile.type

        # allow superuser to edit center code profile field
        if self.request.user.is_superuser:
            selected_cc = None
            if hasattr(self.instance, 'profile'):
                selected_cc = self.instance.profile.cooperative_center

            self.fields['cc'] = forms.ModelChoiceField( queryset=CooperativeCenter.objects.order_by('code'),
                empty_label=None, initial=selected_cc, label=_("Cooperative Center") )
            field_order.append('cc')
        else:
            # tk39 - allow advanced user to select cooperative center of users in their network (manage by his center)

            ccs_networks_responsible = []
            # check networks that request user CC manages
            networks_managed = Network.objects.filter(responsible=self.request.user.profile.cooperative_center)

            # create list with all CCs that user can view users
            for net_managed in networks_managed:
                ccs_networks_responsible.extend( [member.pk for member in net_managed.members.all()] )

            # only show select when request user CC manages a network
            if len(ccs_networks_responsible) > 1:
                selected_cc = self.instance.profile.cooperative_center if self.instance.id else None
                self.fields['cc'] = forms.ModelChoiceField(
                        queryset=CooperativeCenter.objects.filter(pk__in=ccs_networks_responsible).order_by('code'),
                        empty_label=None, initial=selected_cc, label=_("Cooperative Center") )
                field_order.append('cc')

        # Set field order using order_fields method
        self.order_fields(field_order)

    def save(self, commit=True, *args, **kw):
        super(UserForm, self).save(commit=True, *args, **kw)

        if self.request.user.is_superuser and not hasattr(self.instance, 'profile'):
            profile = Profile(user=self.request.user)
            profile.save()

        self.instance.profile.type = self.cleaned_data.get('type')
        if 'cc' in self.cleaned_data:
            self.instance.profile.cooperative_center = self.cleaned_data.get('cc')

        self.instance.profile.save()

        return self.instance

class NetworkForm(forms.ModelForm):

    class Meta:
        model = Network
        fields = ('country', 'topic', 'acronym', 'responsible', 'type')

    def __init__(self, *args, **kw):
        super(NetworkForm, self).__init__(*args, **kw)
        # order cc codes
        self.fields['responsible'] = forms.ModelChoiceField(queryset=CooperativeCenter.objects.order_by('code'),
                                                            label=_("Responsible Cooperative Center") )

class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ( 'name', 'acronym')



class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ( 'name', 'acronym', 'description')
