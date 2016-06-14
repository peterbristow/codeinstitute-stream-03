from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    """
    Create a user registration form.
    """
    MONTH_CHOICES = [(i, i,) for i in xrange(1,12)]
    YEAR_CHOICES = [(i, i,) for i in xrange(2015, 2036)]

    credit_card_number = forms.CharField(label='Credit card number')
    cvv = forms.CharField(label='Security code (CVV)')
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES)

    # Widgets deal with rendering of HTML form input elements on
    # the web page and extraction of raw submitted data.
    stripe_id = forms.CharField(widget=forms.HiddenInput)  # added in the model so it can be saved.
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User  # tie the form to the User model
        fields = ['email', 'password1', 'password2', 'stripe_id']  # fields to display on form
        exclude = ['username']  # don't display this field

    def clean_password2(self):
        """
        Custom method to clean the password data and check if passwords match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)

        return password2

    def save(self, commit=True):
        """
        Override the default save method.
        Ensure the username field (which has a unique constraint) is not
        left blank and instead populated with the users email address.
        """
        instance = super(UserRegistrationForm, self).save(commit=False)

        # Automatically set to email address to create a unique identifier
        instance.username = instance.email

        if commit:
            instance.save()

        return instance


class UserLoginForm(forms.Form):
    """
    Create login form.
    """
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
