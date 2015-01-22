from django import forms

from constants import abbr2color, color2abbr
from models import Project, TrackedTime, Timezone


class TimezoneForm(forms.ModelForm):
    class Meta:
        model = Timezone
        fields = ('timezone',)


class PasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(self.__class__, self).clean()
        p = cleaned_data.get('new_password')
        c = cleaned_data.get('confirm')
        if (p and c and p != c):
            self.add_error('confirm', 'Does not match')


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(self.__class__, self).clean()
        p = cleaned_data.get('password')
        c = cleaned_data.get('confirm')
        if (p and c and p != c):
            self.add_error('confirm', 'Does not match')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TrackTimeForm(forms.ModelForm):
    class Meta:
        model = TrackedTime
        exclude = ('user', 'project', 'created_at', 'manual_date')

    hours = forms.FloatField(widget=forms.NumberInput(
        attrs={'min': 0}))
    track_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}))

    def __init__(self, *args, **kwargs):
        super(TrackTimeForm, self).__init__(*args, **kwargs)


class QuickTrackForm(forms.ModelForm):
    class Meta:
        model = TrackedTime
        exclude = ('user', 'created_at', 'manual_date', 'track_date')

    hours = forms.FloatField(widget=forms.NumberInput(
        attrs={'min': 0}))
