from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik, Upisi, Predmeti, Uloge

class DodajPredmetForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name','kod','program','ects','sem_red','sem_izv','izborni']

class DodajNovogStudenta(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = UserCreationForm.Meta.fields + ('status',)

    def save(self, commit=True):
        user = super(DodajNovogStudenta, self).save(commit=False)
        status = self.cleaned_data["status"]
        user.role = Uloge.objects.get(id = 3)
        user.status = status
        if commit:
            user.save()
        return user
    
class DodajNovogProfesora(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super(DodajNovogProfesora, self).save(commit=False)
        user.role = Uloge.objects.get(id = 2)
        user.status = 'None'
        if commit:
            user.save()
        return user

class DodijeliPredmetProfesour(Form):
    korisnik_id = forms.ModelChoiceField(queryset=Korisnik.objects.all().filter(role=2), required=True)
    predmet_id = forms.ModelChoiceField(queryset=Predmeti.objects.all(), required=True)
    status = forms.CharField(max_length=64, required=True)

class DodijeliKaoNositelja(Form):
    korisnikId = forms.ModelChoiceField(queryset=Korisnik.objects.all().filter(role=2), required=True)
    predmetId = forms.ModelChoiceField(queryset=Predmeti.objects.all(),required=True)

class ListStudentiKojiSuUpisaliPredmet(Form):
    predmetId = forms.ModelChoiceField(queryset=Predmeti.objects.all(), required=True)

class EditKorisnika(ModelForm):
    class Meta:
        model = Korisnik
        fields = ['username','password','role','status']