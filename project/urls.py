"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.main, name='main'),
    ## Logout user view
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    ## Login user view
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    ## Admin view
    path('admin/', admin.site.urls),
    ## Admin - Dodaj novi predmet
    path('dodajPredmet/', views.dodajPredmet, name='dodajPredmet'),
    ## Admin - Lista svih studenata
    path('listaStudenata/', views.listaStudenata, name='listaStudenata'),
    ## Admin - Lista studenata po statusu
    path('listaStudenata/<slug:status>/', views.viewStudenti, name='viewStudenti'),
    ## Admin - Pregled pojedinacnog studenta iz liste studenata
    path('student/<int:student_id>', views.studentAdminView, name='studentAdminView'),
    ## Admin - Dodaj novog studenta
    path('dodajStudenta/', views.dodajStudenta, name='dodajStudenta'),
    ## Admin - Lista svih profesora
    path('listaProfesora/', views.listaProfesora, name='listaProfesora'),
    ## Admin - Dodaj novog profesora
    path('dodajProfesora/', views.dodajProfesora, name='dodajProfesora'),
    ## Admin - Dodajeli predmet odredenom profesour
    path('dodijeliPredmet/', views.dodijeliPredmet, name='dodijeliPredmet'),
    ## Admin - Uredi predmet
    path('predmet/<int:predmet_id>/',views.editPredmet,name='editPredmet'),
    ## Admin - Uredi korisnika
    path('user/<int:user_id>/',views.editKorisnik,name='editKorisnik'),
    ## Admin - Pregled liste studenata po predmetima
    path('predmet-stu-list/<int:predmet_id>', views.viewPredmet, name='viewPredmet'),
    ## Student - Lista svih predmeta i upisna lista
    path('student/', views.student, name='student'),
    ## Profesor - Lista predmeta za koje je profesor zaduzen
    path('profesor/', views.profesor, name='profesor'),
    ## Profesor - Pregled odredenog upisanog predmeta za koji je profesor zaduzen
    path('profesor-predmet-list/<int:predmet_id>/<slug:slug>/', views.profesor_predmet_list, name='profesor_predmet_list'),
]
