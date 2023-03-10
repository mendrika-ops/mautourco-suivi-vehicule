import hashlib
import json

import requests
import simplejson as simplejson
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.forms import ModelForm

from suiviVehicule.models import User, Trajetcoordonnee, TrajetcoordonneeSamm, Recordcomment, Statusparameter
from suiviVehicule.services import services
from datetime import datetime

list_sexe = [
    ('M', 'Masculin'),
    ('F', 'Feminin')
]
list_statut = [
    ('', 'All'),
    ('Risky', 'Risky'),
    ('On Track', 'On Track'),
    ('Off Track', 'Off Track'),
    ('Late', 'Late'),
    ('Cancel', 'Cancel')
]
list_active = [
    ('1', 'Enable'),
    ('0', 'Desable')
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
    driver_oname = forms.CharField(required=False, label='Driver Name', widget=forms.TextInput(
                              attrs={'class': "form-control", 'id': "driver"}))
    driver_mobile_number = forms.CharField(required=False,label='Driver mobile', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    vehicleno = forms.CharField(required=False,label='Vehicule', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    FromPlace = forms.CharField(required=False, label='Pickup Place', widget=forms.TextInput(
        attrs={'class': "form-control"}))
    ToPlace = forms.CharField(required=False, label='Destination', widget=forms.TextInput(
        attrs={'class': "form-control"}))
    status = forms.CharField(required=False, label='Status',widget=forms.Select(choices=list_statut, attrs={'class': "form-control"}))
    
    class Meta:
        model = TrajetcoordonneeSamm
        fields = (
        "driver_oname", "driver_mobile_number", "vehicleno", "FromPlace", "ToPlace", "status")

class CommentFrom(ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control",'placeholder': "* Please specify the reason for trip cancellation below", 'style': 'height: 5em;'}))

    class Meta:
        model = Recordcomment
        fields = ("comment", "id_trip")

    def save(self):
        comment = self.cleaned_data['comment']
        id_trip = self.cleaned_data['id_trip']
        if self.checkexist():
            raise Exception("Error ! object already canceled")
        else:
            record = Recordcomment()
            record.comment = self.cleaned_data['comment']
            record.id_trip = self.cleaned_data['id_trip']
            record.datetime = datetime.now() 
            record.etat = 0
            record.save()
    def checkexist(self):
        return Recordcomment.objects.filter(id_trip=self.cleaned_data['id_trip'],etat=0).exists()
    
class ParameterForm(ModelForm):
    status = forms.CharField(required=True, label='Status', widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    min_percent  = forms.FloatField(required=True, label='Min value', widget=forms.NumberInput(
                              attrs={'class': "form-control", 'style':"width: 100px"}))
    max_percent = forms.FloatField(required=True, label='Max value', widget=forms.NumberInput(
                              attrs={'class': "form-control", 'style':"width: 100px"}))
    couleur = forms.CharField(required=False, label='Status', widget=forms.TextInput(
                              attrs={'type':"color", 'class': "form-control"}))
    desce = forms.CharField(required=True, label='Etat', widget=forms.Select(choices=list_active, 
                              attrs={'class': "form-control"}))
    
    class Meta:
        model = Statusparameter
        fields = '__all__'

    def update(self,parameter):
        parameter.status = self.cleaned_data['status']
        parameter.min_percent = self.cleaned_data['min_percent']
        parameter.max_percent = self.cleaned_data['max_percent']
        parameter.desce = self.cleaned_data['desce']
        parameter.couleur = self.cleaned_data['couleur']
        parameter.save()

    def isExist(self):
        return Statusparameter.objects.filter(status=self.cleaned_data['status']).exists()
