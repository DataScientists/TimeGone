from django import forms
from django.utils.safestring import mark_safe

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


class SatisfactionSlider(forms.NumberInput):
    def render(self, name, value, attrs=None):
        super(SatisfactionSlider, self).render(name, value, attrs)
        tag_attrs = {k: v for k, v in attrs.items()}
        if name:
            tag_attrs['name'] = name
        if value:
            tag_attrs['value'] = value
        shadowed = ['type']
        attr_insertion = u' '.join([u'%s="%s"' % (k, v) for k, v in 
                                    tag_attrs.items() if k not in shadowed])
        tag_line = u'<input type="range" min="0" max="100" step="10" %s />' % attr_insertion
        return mark_safe(tag_line)


class QuickTrackForm(forms.ModelForm):
    class Meta:
        model = TrackedTime
        exclude = ('user', 'created_at', 'manual_date', 'track_date')

    hours = forms.FloatField(widget=forms.NumberInput(
        attrs={'min': 0}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                     widget=forms.HiddenInput)
    satisfaction = forms.IntegerField(widget=SatisfactionSlider)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'color')
