from django import forms

NETWORK_CHOICES = [
    ('mtn', 'MTN'),
    ('airtel', 'Airtel'),
    ('glo', 'GLO'),
    ('etisalat', '9mobile'),
]

class AirtimeForm(forms.Form):
    phone = forms.CharField(label="Phone Number", max_length=11)
    amount = forms.DecimalField(label="Amount", max_digits=6, decimal_places=2)
    network = forms.ChoiceField(choices=NETWORK_CHOICES)
