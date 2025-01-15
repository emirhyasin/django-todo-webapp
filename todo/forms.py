from django import forms
from .models import Todo, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TodoForm(forms.ModelForm):
    body = forms.CharField(required=True,
    widget = forms.widgets.Textarea(
        attrs={
            "placeholder": "What do you want to add?",
            "class": "form-control",
        }
        ),
    label="",
    )
    
    class Meta:
        model = Todo
        fields = ['date_day', 'date_month', 'title', 'category', 'priority', 'body',]
        exclude = ("user",)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Select a category", widget=forms.Select(attrs={'class':'form-control'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Your Email'}))
    
    class Meta:
        model = User
        fields = ('username','email','password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. Maximum 100 characters. Only letters, digits, and @/./+/-/_ symbols are allowed.</small></span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>The password should not contain your personal information.</li><li>At least 8 characters.</li><li>Do not use common passwords.</li><li>Your password cannot consist entirely of numbers.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password for verification.</small></span>'
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.username == username:
            return username

        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu kullanıcı adı zaten kullanılıyor.")
        
        return username

class ChangePasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        # Şifrelerin eşleşip eşleşmediğini kontrol et
        if new_password != confirm_new_password:
            raise ValidationError("New password and confirm new password do not match.")
        
        # Kullanıcıyı doğrula
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("User not found.")
        
        # Şu anki şifreyi kontrol et
        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")
        
        return cleaned_data