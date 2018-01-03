from betterforms.forms import BetterModelForm

from .models import Profile


class ProfileAddForm(BetterModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fieldsets = (
            ('info', {
                'fields': (
                    'company',
                ),
                'legend': 'Profile details'
            }),
        )


class ProfileUpdateForm(BetterModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fieldsets = (
            ('info', {
                'fields': (
                    'company',
                ),
                'legend': 'Profile details'
            }),
        )
