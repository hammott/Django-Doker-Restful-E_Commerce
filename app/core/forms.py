from django import forms

class ContactForm(form.Form):
    fullname = forms.CharField()
    email = forms.EmailField()
    