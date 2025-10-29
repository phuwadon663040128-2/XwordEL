
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
import sys


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = "off"
        self.fields['password1'].widget.attrs['autocomplete'] = "off"
        self.fields['password2'].widget.attrs['autocomplete'] = "off"

class UserPlayedWordsDeleteForm(forms.Form):
    #Thai and English
    thaiWordDelete = forms.BooleanField(required=False,widget=forms.widgets.CheckboxInput( attrs={'value': 'thaiWordDelete', 'id': 'thaiWordDelete'}))
    engWordDelete = forms.BooleanField(required=False,widget=forms.widgets.CheckboxInput( attrs={'value': 'engWordDelete', 'id': 'engWordDelete'}))

class UserPlayedWordsDownloadForm(forms.Form):
    #Thai and English
    thaiWordDownload = forms.BooleanField(required=False,widget=forms.widgets.CheckboxInput( attrs={'value': 'thaiWordDownload', 'id': 'thaiWordDownload'}))
    engWordDownload = forms.BooleanField(required=False,widget=forms.widgets.CheckboxInput( attrs={'value': 'engWordDownload', 'id': 'engWordDownload'}))


# not used
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    remember_me = forms.BooleanField(required=False)

