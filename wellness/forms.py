import urllib.parse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, WellnessResource, CounselingSession, AnonymousSupport, Profile

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Profile._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2', 'role']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile._meta.get_field('role').choices)



class WellnessResourceForm(forms.ModelForm):
    class Meta:
        model = WellnessResource
        fields = ['title', 'description', 'link']

    def clean_link(self):
        link = self.cleaned_data['link']
        # Check that the link has a valid scheme and netloc
        parsed = urllib.parse.urlparse(link)
        if not parsed.scheme or not parsed.netloc:
            raise forms.ValidationError("Invalid URL format. Must start with http:// or https://")

        # Optional: normalize YouTube short links
        if "youtu.be/" in link:
            video_id = link.split("youtu.be/")[-1]
            link = f"https://www.youtube.com/watch?v={video_id}"

        return link


class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession
        fields = ['student', 'counselor', 'scheduled_time', 'notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'max-width: 250px;'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users with student role
        student_ids = Profile.objects.filter(role='student').values_list('user_id', flat=True)
        self.fields['student'].queryset = User.objects.filter(id__in=student_ids)

        # Only show users with counselor role
        counselor_ids = Profile.objects.filter(role='counselor').values_list('user_id', flat=True)
        self.fields['counselor'].queryset = User.objects.filter(id__in=counselor_ids)


class AnonymousSupportForm(forms.ModelForm):
    class Meta:
        model = AnonymousSupport
        fields = ['message', 'response']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'response': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

