from django import forms
from django.urls import reverse_lazy
from collections import Counter
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
    data = Counter(list(Profile.objects.values_list('company', flat=True)))
    CHOICES = [(key,key) for key, value in data.items() if value > 1]
    # 
    company = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input',
                'hx-post': reverse_lazy('demo:workers'),
                'hx-trigger': 'change',
                'hx-target': '#search'
            }
        )
    )
    class Meta:
        model = Profile
        fields = ('company', )