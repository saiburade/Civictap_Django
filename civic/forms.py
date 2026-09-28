from django import forms
from django.contrib.auth.hashers import make_password
from .models import CivicUser, Issue, Feedback


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Create password"}),
        min_length=6,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}),
        min_length=6,
    )

    class Meta:
        model = CivicUser
        fields = ["full_name", "gender", "phone", "address"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-15 digit phone number"}),
            "address": forms.TextInput(attrs={"placeholder": "Your address"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CivicUser
        fields = ["full_name", "gender", "phone", "address"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["description", "address", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Describe the civic issue..."}),
            "address": forms.TextInput(attrs={"placeholder": "Area / address"}),
        }


class FeedbackForm(forms.ModelForm):
    rating = forms.TypedChoiceField(choices=[(i, f"{i} / 5") for i in range(1, 6)], coerce=int, widget=forms.RadioSelect)

    class Meta:
        model = Feedback
        fields = ["message", "rating"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your thoughts..."}),
            "rating": forms.RadioSelect(),
        }
