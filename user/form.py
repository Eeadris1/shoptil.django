from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    # Generally this  fuction handle the css styling for the inbuilt django form.... Define the initialization method (__init__) for the form class
    def __init__(self, *args, **kwargs):

        # Call the initialization method of the parent class (super) to ensure proper initialization
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Set placeholder attributes for specific form fields to provide hints to users about the expected input
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'

        # Iterate over all fields in the form and set the CSS class 'form-control' for each field's widget so generally this handle the css styling for the inbuilt django form
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # this check if the password and the confirm password match thrn raise an error
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
