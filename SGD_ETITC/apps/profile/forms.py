from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass
 
    first_name = forms.CharField(label='Nombres', max_length=30)
    last_name = forms.CharField(label='Apelliods', max_length=150)
    email = forms.EmailField(label="Email", help_text='')


    class Meta:
        model = Profile
        exclude = ('user', )
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'phone', 'cellphone', 'avatar',)

    def save(self, *args, **kwargs):
        """
        Update the primary email address, lastname, firstname on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile