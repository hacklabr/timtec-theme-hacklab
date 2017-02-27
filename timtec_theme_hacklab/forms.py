# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm


# This class is for tests pourpose only.
# Do not use it in production inviroments!!!
#
class SindsepLoginForm(LoginForm):

    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=True)
    accept_terms = forms.BooleanField(label=_('Accept '), initial=False, required=False)

    def clean_password2(self):
        # import ipdb;ipdb.set_trace()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2:
            if password != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_email(self):
        # import ipdb;ipdb.set_trace()
        return self.data['email']

    def clean(self):
        if self._errors:
            return
        User = get_user_model()
        try:
            login = self.cleaned_data["login"]
            sindsep_user = User.objects.get(username=login)

            if not sindsep_user.is_active:
                if not sindsep_user.email or self.data["email"].split('@')[1]:
                    sindsep_user.email = self.data["email"]
                else:
                    if sindsep_user.email != self.data["email"]:
                        #TODO avaliar com entremeios o caso de o email inserido e o
                        # pre cadastrado ser diferente.
                        pass
                sindsep_user.is_active = True
                sindsep_user.set_password(self.cleaned_data["password"])
                sindsep_user.save()
                return super(SindsepLoginForm, self).clean()
            else:
                self.user = sindsep_user
                self.user.is_cpf_verified = True
                # gera erro para informar o usuário que ele já
                # cadastrou uma senha
                pass
        except User.DoesNotExist:
            pass

        return self.cleaned_data

    def login(self, request, redirect_url=None):
        import ipdb;ipdb.set_trace()
        if not self.user:
            return redirect(reverse_lazy('base_theme:sindsep_signup_error'))
        elif self.user.is_cpf_verified:
            return redirect(reverse_lazy('account_login'))
        response = super(SindsepLoginForm, self).login(request, redirect_url)
        return response
