from django import forms
from django.contrib.auth.forms import UserCreationForm
from store.models import User, Order


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
        
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
            field.help_text = None
            field.label = ''
            
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        

class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), label='')
    
    
    
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['address','phone','payment_method']