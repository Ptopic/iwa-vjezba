from django.shortcuts import redirect, HttpResponse, render
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Uloge, Predmeti, Upisi, Korisnik
from django.contrib.auth.decorators import login_required
from .forms import DodajPredmetForm, DodajNovogStudenta, DodajNovogProfesora, DodijeliPredmetProfesour, DodijeliKaoNositelja, EditKorisnika, ListStudentiKojiSuUpisaliPredmet


## Admin views 

@login_required(login_url='/login/')
def main(request):
    currentUser = request.user
    role = str(request.user.role)
    print(role == 'stu')
    if not currentUser.is_authenticated:
        return redirect('login')
    elif currentUser.is_authenticated and role == 'stu':
        return redirect("student")
    elif currentUser.is_authenticated and role == 'prof':
        return redirect("profesor")
    else:
        lista_predmeta = Predmeti.objects.all()
        return render(request, 'index.html', {'lista_predmeta' : lista_predmeta})

@login_required(login_url='/login/')
def logoutView(request):
    logout(request)
    return redirect('main')

@login_required(login_url='/login/')
def dodajPredmet(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    dodajPredmetForm = DodajPredmetForm()

    if request.method == 'POST':
        dodajPredmetForm = DodajPredmetForm(request.POST)
        if dodajPredmetForm.is_valid():
            dodajPredmetForm.save()
    
    return render(request, 'dodajPredmet.html', {'form' : dodajPredmetForm})

# --- Svi studenti koji imaju odredeni status (redovni, izvanredni)
@login_required(login_url='/login/')
def viewStudenti(request, status):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    studenti = Korisnik.objects.all().filter(status=status)
    return render(request, 'listaStudenata.html', {'studenti' : studenti})

# --- ispisat sve studente koji su upisali/polozili odredeni predmet
@login_required(login_url='/login/')
def viewPredmet(request, predmet_id):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    predmet = Predmeti.objects.all().filter(id=predmet_id)
    allUpisi = Upisi.objects.all().filter(predmet_id=predmet_id)
    studentsForPredmet = []
    for upis in allUpisi:
        if str(upis.student_id.role) == 'stu':
            studentsForPredmet.append(upis.student_id)

    polozeniPredmeti = Upisi.objects.all().filter(predmet_id=predmet_id,status="Položen")

    studentiKojiSuPoloziliPredmet = []

    for upis in polozeniPredmeti:
        if str(upis.student_id.role) == 'stu':
            studentiKojiSuPoloziliPredmet.append(upis.student_id)
        
    print(studentsForPredmet)
    return render(request, 'predmet-stu-list.html', {'predmet':predmet, 'student_list': studentsForPredmet, 'polozili_predmet': studentiKojiSuPoloziliPredmet})

@login_required(login_url='/login/')
def listaStudenata(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    studenti = Korisnik.objects.all().filter(role=3)
    return render(request, 'listaStudenata.html', {'studenti' : studenti})

@login_required(login_url='/login/')
def dodajStudenta(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    dodajStudentaForm = DodajNovogStudenta()

    if request.method == 'POST':
        dodajStudentaForm = DodajNovogStudenta(request.POST)
        if dodajStudentaForm.is_valid():
            dodajStudentaForm.save()
    
    return render(request, 'dodajStudenta.html', {'form' : dodajStudentaForm})

@login_required(login_url='/login/')
def studentAdminView(request, student_id):
    role = str(request.user.role)
    user = Korisnik.objects.get(id=student_id)
    if role != 'admin':
        return redirect('main')
    
    subjects = Predmeti.objects.all()

    if request.POST.get('add', False):
        if not Upisi.objects.filter(student_id=student_id,predmet_id=request.POST["add"]).exists():
            upis = Upisi(student_id=user,predmet_id=Predmeti.objects.get(pk=request.POST["add"]),status="Upisan")
            upis.save()


    elif request.POST.get('remove', False):
        if Upisi.objects.filter(student_id=student_id,predmet_id=request.POST["remove"]).exists():
            upis = Upisi.objects.get(predmet_id=request.POST["remove"],student_id=user)
            upis.delete()

    upisi_korisnika = Upisi.objects.all().filter(student_id=student_id)
    upisani_predmeti = []
    for u in upisi_korisnika:
        if user.status == 'red':
            upisani_predmeti.append(u.predmet_id)
        elif user.status == 'izv':
            upisani_predmeti.append(u.predmet_id)

    return render(request, 'studentAdmin.html', {'subjects' : subjects, 'user': user,'upisi':upisani_predmeti,
                                        'range':range(1,11)})

@login_required(login_url='/login/')
def listaProfesora(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')

    profesori = Korisnik.objects.all().filter(role=2)
    return render(request, 'listaProfesora.html', {'profesori' : profesori})

@login_required(login_url='/login/')
def dodajProfesora(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')

    dodajProfesoraForm = DodajNovogProfesora()

    if request.method == 'POST':
        dodajProfesoraForm = DodajNovogProfesora(request.POST)
        if dodajProfesoraForm.is_valid():
            dodajProfesoraForm.save()

    return render(request, 'dodajProfesora.html', {'form': dodajProfesoraForm})

@login_required(login_url='/login/')
def dodijeliPredmet(request):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')
    
    form = DodijeliPredmetProfesour()
    updateNositeljForm = DodijeliKaoNositelja()

    if request.method == 'POST':
        form = DodijeliPredmetProfesour(request.POST)
        updateNositeljForm = DodijeliKaoNositelja(request.POST)
        if form.is_valid():
            upis = Upisi(student_id=form.cleaned_data["korisnik_id"],predmet_id=form.cleaned_data["predmet_id"],status=form.cleaned_data["status"])
            upis.save()
        if updateNositeljForm.is_valid():
            predmetId = updateNositeljForm.cleaned_data["predmetId"]
            korisnikNositelj = updateNositeljForm.cleaned_data["korisnikId"]
            predmet = Predmeti.objects.all().filter(id=predmetId.id).update(nositelj=korisnikNositelj)

    return render(request, 'dodijeliPredmet.html', {'dodijeliPredmetForm' : form, 'dodijeliKaoNositeljaForm' : updateNositeljForm})

@login_required(login_url='/login/')
def editPredmet(request, predmet_id):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')

    predmet = Predmeti.objects.get(pk=predmet_id)
    form = DodajPredmetForm(initial={'name': predmet.name,'kod':predmet.kod,'program':predmet.program,'ects':predmet.ects,
    'sem_red':predmet.sem_red,'sem_izv':predmet.sem_izv,'izborni':predmet.izborni.upper()})

    if request.method == "POST":
        form = DodajPredmetForm(request.POST)
        if form.is_valid():
            predmet.name = form.cleaned_data['name']
            predmet.kod = form.cleaned_data['kod']
            predmet.program = form.cleaned_data['program']
            predmet.ects = form.cleaned_data['ects']
            predmet.sem_red = form.cleaned_data['sem_red']
            predmet.sem_izv = form.cleaned_data['sem_izv']
            predmet.izborni = form.cleaned_data['izborni']
            predmet.save()

    return render(request,'edit-predmet.html',{'form':form})

@login_required(login_url='/login/')
def editKorisnik(request, user_id):
    role = str(request.user.role)
    if role != 'admin':
        return redirect('main')

    korisnik = Korisnik.objects.get(id=user_id)
    form = EditKorisnika(instance=korisnik)

    if request.method == "POST":
        form = EditKorisnika(request.POST, instance=korisnik)
        if form.is_valid():
            korisnik.username = form.cleaned_data['username']
            korisnik.status = form.cleaned_data['status']
            korisnik.role = form.cleaned_data['role']
            korisnik.set_password(form.cleaned_data['password'])
            korisnik.save()
    return render(request,'edit-korisnika.html',{'form':form})

## Student views

# ---
@login_required(login_url='/login/')
def student(request):
    role = str(request.user.role)
    user = request.user
    if role != 'stu':
        return redirect('main')
    
    subjects = Predmeti.objects.all()

    # Ako nisi polozia sve predmete s prve godine, ne mozes upisat predmete s druge godine 
    # i ako nisi polozia predmete s prve i druge godine, ne mozes upisat predmete s trece godine
    moguci_predmeti = []

    if user.status == 'red':
        polozeni_predmet = Upisi.objects.all().filter(student_id=user.id, status="Polozen")

        prvi_sem = subjects.filter(sem_red=1)
        drugi_sem = subjects.filter(sem_red=2)
        treci_sem = subjects.filter(sem_red=3)
        cetvrti_sem = subjects.filter(sem_red=4)
        peti_sem = subjects.filter(sem_red=5)
        sesti_sem = subjects.filter(sem_red=6)

        moguci_predmeti.extend(prvi_sem)
        moguci_predmeti.extend(drugi_sem)

        upis_druge_godine = True
        upis_trece_godiene = True

        for predmet in prvi_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_druge_godine = False
                break
        
        for predmet in drugi_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_druge_godine = False
                break
        
        moguci_predmeti.extend(treci_sem)
        moguci_predmeti.extend(cetvrti_sem)

        for predmet in treci_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_trece_godiene = False
                break
        
        for predmet in cetvrti_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_trece_godiene = False
                break

        moguci_predmeti.extend(peti_sem)
        moguci_predmeti.extend(sesti_sem)

    elif user.status == 'izv':
        polozeni_predmet = Upisi.objects.all().filter(student_id=user.id, status="Polozen")

        prvi_sem = subjects.filter(sem_izv=1)
        drugi_sem = subjects.filter(sem_izv=2)
        treci_sem = subjects.filter(sem_izv=3)
        cetvrti_sem = subjects.filter(sem_izv=4)
        peti_sem = subjects.filter(sem_izv=5)
        sesti_sem = subjects.filter(sem_izv=6)

        moguci_predmeti.extend(prvi_sem)
        moguci_predmeti.extend(drugi_sem)

        upis_druge_godine = True
        upis_trece_godine = True

        for predmet in prvi_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_druge_godine = False
                break
        
        for predmet in drugi_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_druge_godine = False
                break
        
        if upis_druge_godine == True:
            moguci_predmeti.extend(treci_sem)
            moguci_predmeti.extend(cetvrti_sem)

        for predmet in treci_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_trece_godine = False
                break
        
        for predmet in cetvrti_sem:
            if not polozeni_predmet.filter(predmet_id=predmet.id).exists():
                upis_trece_godine = False
                break
        
        if upis_trece_godine == True:
            moguci_predmeti.extend(peti_sem)
            moguci_predmeti.extend(sesti_sem)

    if request.POST.get('add', False):
        if not Upisi.objects.filter(student_id=user.id,predmet_id=request.POST["add"]).exists():
            upis = Upisi(student_id=user,predmet_id=Predmeti.objects.get(pk=request.POST["add"]),status="Upisan")
            upis.save()

    elif request.POST.get('remove', False):
        if Upisi.objects.filter(student_id=user.id,predmet_id=request.POST["remove"]).exists():
            upis = Upisi.objects.get(predmet_id=request.POST["remove"],student_id=user.id)
            upis.delete()

    upisi_korisnika = Upisi.objects.all().filter(student_id=user.id)
    upisani_predmeti = []
    for u in upisi_korisnika:
        if user.status == 'red':
            upisani_predmeti.append(u.predmet_id)
        elif user.status == 'izv':
            upisani_predmeti.append(u.predmet_id)

    return render(request, 'student.html', {'subjects' : moguci_predmeti, 'user': user,'upisi':upisani_predmeti,
                                        'range':range(1,11)})

## Profesor views
@login_required(login_url='/login/')
def profesor(request):
    role = str(request.user.role)
    if role != 'prof':
        return redirect('main')

    svi_upisi = Upisi.objects.all().filter(student_id=request.user.id)
    prijavljeniPredmeti = []
    print(svi_upisi)
    for u in svi_upisi:
        prijavljeniPredmeti.append(Predmeti.objects.get(pk=u.predmet_id.id))
    print(prijavljeniPredmeti)
    return render(request, 'profesor.html', {'prijavljeniPredmeti' : prijavljeniPredmeti})

@login_required(login_url='/login/')
def profesor_predmet_list(request, predmet_id, slug):
    role = str(request.user.role)
    if role != 'prof':
        return redirect('main')
    
    if not Upisi.objects.all().filter(student_id=request.user.id,predmet_id=predmet_id).exists():
        return redirect('main')
    
    if request.POST.get('remove', False):
        if Upisi.objects.filter(student_id=request.POST["remove"],predmet_id=predmet_id).exists():
            upis = Upisi.objects.get(predmet_id=predmet_id,student_id=request.POST["status-change"])
            upis.delete()
    
    if request.POST.get('status-change', False):
        if request.POST.getlist("status","none") != "none":
            upis = Upisi.objects.get(predmet_id=predmet_id,student_id=request.POST["status-change"])
            if request.POST.getlist("status","none")[0] == "polozen":
                upis.status = "Položen"
            elif request.POST.getlist("status","none")[0] == "izgubio_potpis":
                upis.status = "Izgubio potpis"
            elif request.POST.getlist("status","none")[0] == "potpis":
                upis.status = "Dobio potpis ali nije položen"
            upis.save()

    students = []
    if slug == 'svi':
        svi_upisi = Upisi.objects.all().filter(predmet_id=predmet_id)
        for u in svi_upisi:
            if str(u.student_id.role) == 'stu':
                students.append(u)
    elif slug == 'izgubili-potpis':
        svi_upisi = Upisi.objects.all().filter(predmet_id=predmet_id,status="Izgubio potpis")
        for u in svi_upisi:
            if str(u.student_id.role) == 'stu':
                students.append(u)
    elif slug == 'dobili-potpis':
        svi_upisi = Upisi.objects.all().filter(predmet_id=predmet_id,status="Dobio potpis ali nije položen")
        for u in svi_upisi:
            if str(u.student_id.role) == 'stu':
                students.append(u)
    elif slug == 'polozili':
        svi_upisi = Upisi.objects.all().filter(predmet_id=predmet_id,status="Položen")
        for u in svi_upisi:
            if str(u.student_id.role) == 'stu':
                students.append(u) 
    return render(request,'profesor-predmet-list.html',{'students':students,'predmet_id':predmet_id})