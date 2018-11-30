from django import forms
from .models import AuthUserManager, AuthUser
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(forms.ModelForm):
    """User Signup Form"""
    class Meta:
        #Use AuthUser class from model.py
        model = AuthUser
        #Prepare the same fields as being made in model.py
        fields = ('first_name', 'last_name', 'phone', 'restaurant', 'password', )
        #パスワードform作るときのおまじない
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '*Password'}),
        }

    #Create Password Confirmation form
    confirm_password = forms.CharField(
        label='checking password',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '*Password'}),
    )

    #Create Input form
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'placeholder': '*First name'}
        self.fields['first_name'].required = True
        self.fields['last_name'].widget.attrs = {'placeholder': '*Last name'}
        self.fields['last_name'].required = True
        self.fields['phone'].widget.attrs = {'placeholder': '*Phone'}
        self.fields['phone'].required = True
        self.fields['restaurant'].widget.attrs = {'placeholder': '*Restaurant name'}
        self.fields['restaurant'].required = True

    def clean_phone(self):
        """validate phone"""
        phone = self.cleaned_data['phone']

        #if phone is less than 9 letters, show error message
        if len(phone) < 9:
            raise forms.ValidationError('Phone number must be more than 9 letters')
        #if phoen is not numeric, show error message
        if not phone.isnumeric():
            raise forms.ValidationError('Phone number must be numbers')
        return phone

    def clean(self):
        """validate password and confirm password"""
        super(SignUpForm, self).clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        #if password and confirm password dont match, show error message
        if password != confirm_password:
            raise forms.ValidationError("password and confirmed password don't match")

    def save(self, commit=True):
        """hash password and save user info"""

        user_info = super(SignUpForm, self).save(commit=False)
        user_info.set_password(self.cleaned_data["password"])
        if commit:
            user_info.save()
            AuthUser.objects.create(user=user_info)

        return user_info


class LoginForm(forms.Form):
    phone = forms.CharField(
        label='Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number',
                                      'autofocus': True})
    )
    """
    - render_value=True... when user go back to login page, password remains
    - strip=Flase...When strip=True, remove space in the first and last place
    """
    password = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}, render_value=True)
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        #create object to keep the user info
        self.user_request_to_login = None

    def clean_password(self):
        """validate password"""
        password = self.cleaned_data['password']
        return password

    def clean_phone(self):
        """validate phone number"""
        phone = self.cleaned_data['phone']
        return phone

    def clean(self):
        """validate phone and its password are corresponding"""
        phone = self.clean_phone()
        password = self.clean_password()

        try:
            requesting_user = AuthUser.objects.get(phone=phone)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Input correct phone number')
        if not requesting_user.check_password(password):
            raise forms.ValidationError('Input correct password')
        self.user_request_to_login = requesting_user


    def get_login_user(self):
        """return user id which has corresponding phone and database id"""
        return self.user_request_to_login