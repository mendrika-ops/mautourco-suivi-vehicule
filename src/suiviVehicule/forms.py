import hashlib
import json

import requests
import simplejson as simplejson
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.forms import ModelForm

from suiviVehicule.models import User, Trajetcoordonnee

list_sexe = [
    ('M', 'Masculin'),
    ('F', 'Feminin')
]


class SigninForm(ModelForm):
    mail = forms.EmailField(required=True, label='Email')
    pswd = forms.CharField(label='Password', widget=forms.PasswordInput)
    address = forms.CharField(required=False)
    contact = forms.CharField(required=False)
    sexe = forms.CharField(widget=forms.Select(choices=list_sexe))

    class Meta:
        model = User
        fields = ("username", "sexe", "address", "contact", "mail", "pswd")

    def save(self, commit=True):
        user = super(SigninForm, self).save(commit=False)
        user.mail = self.cleaned_data['mail']
        enc = hashlib.sha256(self.cleaned_data['pswd'].encode()).hexdigest()
        user.pswd = enc
        user.etat = 1
        if commit:
            user.save()
        return user

    def isExist(self):
        return User.objects.filter(mail=self.cleaned_data['mail']).exists()


class LoginForm(ModelForm):
    mail = forms.EmailField(required=True, label='email')
    pswd = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("mail", "pswd")

    def checkUser(self):
        print("mail ", self.cleaned_data['mail'])

        enc = hashlib.sha256(self.cleaned_data['pswd'].encode()).hexdigest()
        print("password ", enc)
        return User.objects.filter(mail=self.cleaned_data['mail'], pswd=enc).exists()


class dashboardForm(ModelForm):
    class Meta:
        model = Trajetcoordonnee
        fields = ("vehicleno", "driver_oname", "driver_mobile_number", "FromPlace", "ToPlace", "id_trip", "trip_no",
                  "trip_start_date", "pick_up_time", "PickUp_H_Pos")

    def get_data(self):
        data = Trajetcoordonnee.objects.all().order_by('trip_start_date', '-pick_up_time').values()
        return data


class Form(ModelForm):
    mail = forms.EmailField(required=True, label='Email')
    pswd = forms.CharField(label='Password', widget=forms.PasswordInput)
    address = forms.CharField(required=False)
    contact = forms.CharField(required=False)
    sexe = forms.CharField(widget=forms.Select(choices=list_sexe))

    class Meta:
        model = User
        fields = ("username", "sexe", "address", "contact", "mail", "pswd")

    def save(self, commit=True):
        user = super(SigninForm, self).save(commit=False)
        user.mail = self.cleaned_data['mail']
        enc = hashlib.sha256(self.cleaned_data['pswd'].encode()).hexdigest()
        user.pswd = enc
        user.etat = 1
        if commit:
            user.save()
        return user
