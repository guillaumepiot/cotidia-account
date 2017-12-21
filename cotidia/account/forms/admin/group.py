from django import forms
from django.contrib.auth.models import Group, Permission

from betterforms.forms import BetterModelForm


class GroupAddForm(BetterModelForm):

    permissions = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.all(),
        required=False)

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        fieldsets = (
            ('info', {'fields': ('name', 'permissions'), 'legend': 'Role details'}),
        )


class GroupUpdateForm(GroupAddForm):
    class Meta:
        model = Group
