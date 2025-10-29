from django import forms


class CrosswordSessionForm(forms.Form):

    reset_session = forms.BooleanField(required=False, label="Reset session")
    reset_wordlist = forms.BooleanField(required=False, label="Reset wordlist")
    check_crossword = forms.BooleanField(
        required=False, label="Check crossword")


class userUploadFile(forms.Form):
    file = forms.FileField()

