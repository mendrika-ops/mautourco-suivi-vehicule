import hashlib
import json

import requests
import simplejson as simplejson
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.forms import ModelForm

from suiviVehicule.models import User, Trajetcoordonnee, TrajetcoordonneeSamm
from suiviVehicule.services import services

list_sexe = [
    ('M', 'Masculin'),
    ('F', 'Feminin')
]
list_statut = [
    ('', 'Tous'),
    ('On time', 'On time'),
    ('Late', 'Late'),
    ('Risky', 'Risky'),
    ('Terminated', 'Terminated'),
    ('Cancel', 'Cancel')
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
    mail = forms.EmailField(required=False, label='Email',widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    pswd = forms.CharField(required=False, label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ("mail", "pswd")

    def checkUser(self):
        print("mail ", self.cleaned_data['mail'])

        enc = hashlib.sha256(self.cleaned_data['pswd'].encode()).hexdigest()
        print("password ", enc)
        return User.objects.filter(mail=self.cleaned_data['mail'], pswd=enc).exists()


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


class SearchForm(ModelForm):
    driver_oname = forms.CharField(required=False, label='Driver', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    driver_mobile_number = forms.CharField(required=False,label='Driver mobile', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    vehicleno = forms.CharField(required=False,label='Vehicule', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    id_trip = forms.CharField(required=False, label='Trip', widget=forms.TextInput(
        attrs={'class': "form-control"}))
    FromPlace = forms.CharField(required=False, label='FromPlace', widget=forms.TextInput(
        attrs={'class': "form-control"}))
    ToPlace = forms.CharField(required=False, label='ToPlace', widget=forms.TextInput(
        attrs={'class': "form-control"}))
    status = forms.CharField(required=False, label='ToPlace',widget=forms.Select(choices=list_statut, attrs={'class': "form-control"}))
    trip_no = forms.CharField(required=False, label='Trip N°', widget=forms.TextInput(
        attrs={'class': "form-control"}))

    class Meta:
        model = TrajetcoordonneeSamm
        fields = (
        "driver_oname", "driver_mobile_number", "vehicleno", "id_trip", "FromPlace", "ToPlace", "status", "trip_no")
