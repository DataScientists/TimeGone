from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        p = cleaned_data.get('password')
        c = cleaned_data.get('confirm')
        if (p and c and p != c):
            self.add_error('confirm', 'Does not match')

            


