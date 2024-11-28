from django import forms
from .models import BlogUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = BlogUser
        fields = ['image', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.add_input(Submit(_('Update'), _('Update'), css_class='btn btn-primary'))
