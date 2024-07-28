from django import forms
from .models import (
    CallRequest, Subscriber, Filing
)


class CallRequestForm(forms.ModelForm):
    class Meta:
        model = CallRequest
        fields = [
            'full_name', 'email', 'phone'
        ]


class FilingForm(forms.ModelForm):
    class Meta:
        model = Filing
        fields = [
            'full_name', 'email', 'phone', 'company'
        ]


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = [
            'email'
        ]
