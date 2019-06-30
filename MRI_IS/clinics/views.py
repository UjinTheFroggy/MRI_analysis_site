from django.shortcuts import render, redirect
from domain.models import Clinic
from users.models import User
from .forms import ClinicCreationForm
from domain.clinics_manager import ClinicsManager
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.list import ListView


# Create your views here.


def clinics_create_edit(request):
    if request.method == 'GET':
        clinic = ClinicsManager.get_clinics_by_director(
            director=request.user.id)
        if clinic is None:
            clinic_creation_form = ClinicCreationForm()
            return render(request, 'clinics/create_edit.html',
                          {'clinic_creation_form': clinic_creation_form,
                           'action': 'Создать'})
        else:
            clinic_creation_form = ClinicCreationForm(instance=clinic)
            return render(request, 'clinics/create_edit.html',
                          {'clinic_creation_form': clinic_creation_form,
                           'action': 'Изменить'})
    elif request.method == 'POST':
        clinic = ClinicsManager.get_clinics_by_director(
            director=request.user.id)
        form = ClinicCreationForm(request.POST, instance=clinic)
        if form.is_valid():
            clinic = form.save(commit=False)
            ClinicsManager.create_edit_clinic(
                clinic=clinic, director=request.user)
            messages.success(
                request, 'Вы создали клинику!')
            return redirect('profile')


class DoctorListView(ListView):

    model = User
    paginate_by = 10
    template_name = "doctor-list.html"
    ordering = ['-created']

    def get_queryset(self):
        queryset = ClinicsManager.get_clinics_by_director(
            director=self.request.user.id)
        return queryset
