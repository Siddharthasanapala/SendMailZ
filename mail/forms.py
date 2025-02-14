from django import forms

class SendMailsForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=500)
    excel_file = forms.FileField()