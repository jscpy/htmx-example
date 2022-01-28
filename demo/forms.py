from django import forms
from demo.models import Todo, Profile


class TodoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input'
        }
    ))
    class Meta:
        model = Todo
        fields = ('title', )


class ProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}))
    
    class Meta:
        model = Profile
        fields = ('address', 'phonenumber', 'email')