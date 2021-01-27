from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.users import forms as wagtail_users_forms


class UserEditForm(wagtail_users_forms.UserEditForm):
    resource = forms.URLField(required=False, label=_("Resource"))


class UserCreationForm(wagtail_users_forms.UserCreationForm):
    resource = forms.URLField(required=False, label=_("Resource"))
