from django import forms

class SendMailsForm(forms.Form):
    subject = forms.CharField(widget=forms.Textarea, max_length=100)
    message = forms.CharField(widget=forms.Textarea, max_length=500)
    attachments = forms.FileField(required=False)
    excel_file = forms.FileField()