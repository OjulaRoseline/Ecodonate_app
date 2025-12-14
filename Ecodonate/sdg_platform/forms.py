# sdg_platform/forms.py
from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    # We use a ModelForm but explicitly define fields for custom widgets/placeholders
    amount = forms.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        label='Donation Amount (KES)',
        min_value=1.00,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 500.00'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        label='M-Pesa Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 2547XXXXXXXX'})
    )

    class Meta:
        model = Donation
        # Only include the fields we want the user to input
        fields = ['amount', 'phone_number']