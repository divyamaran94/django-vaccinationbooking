from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from ..decorators import manager_required
from ..forms import ManagerSignUpForm
from ..models import User, Vaccinetype, Vaccinecenter, Appointment, Availabledate


class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('managers:manager_home_view')
      

@method_decorator([login_required, manager_required], name='dispatch')
class VaccinetypeListView(ListView):
    model = Vaccinetype
    ordering = ('name', )
    context_object_name = 'vaccinetypes'
    template_name = 'booking/managers/vaccinetype_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.vaccinetypes.all()
        return queryset

@method_decorator([login_required, manager_required], name='dispatch')
class VaccinecenterListView(ListView):
    model = Vaccinecenter
    ordering = ('name', )
    context_object_name = 'vaccinecenters'
    template_name = 'booking/managers/vaccinecenter_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.vaccinecenters.all()
        return queryset

@method_decorator([login_required, manager_required], name='dispatch')
class AvailabledateListView(ListView):
    model = Availabledate
    ordering = ('name', )
    context_object_name = 'availabledates'
    template_name = 'booking/managers/availabledate_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.availabledates.all()
        return queryset


@method_decorator([login_required, manager_required], name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    ordering = ('name', 'dose_type', 'vaccinetype', 'vaccinecenter','date_of_vaccine1', 'availabledate')
    context_object_name = 'appointments'
    template_name = 'booking/managers/appointment_change_list.html'

    def get_queryset(self):
        return Appointment.objects.all()
        
   
def manager_home_view(request):
    return render(request, 'booking/managers/manager_home_view.html')


@method_decorator([login_required, manager_required], name='dispatch')
class VaccinetypeCreateView(CreateView):
    model = Vaccinetype
    fields = ('name',)
    template_name = 'booking/managers/vaccinetype_add_form.html'

    def form_valid(self, form):
        vaccinetype = form.save(commit=False)
        vaccinetype.owner = self.request.user
        vaccinetype.save()
        messages.success(self.request, 'The vaccinetype was created with success!')
        return redirect('managers:vaccinetype_change', vaccinetype.pk)


@method_decorator([login_required, manager_required], name='dispatch')
class VaccinecenterCreateView(CreateView):
    model = Vaccinecenter
    fields = ('name', )
    template_name = 'booking/managers/vaccinecenter_add_form.html'

    def form_valid(self, form):
        vaccinecenter = form.save(commit=False)
        vaccinecenter.owner = self.request.user
        vaccinecenter.save()
        messages.success(self.request, 'The vaccinecenter was created with success!')
        return redirect('managers:vaccinecenter_change', vaccinecenter.pk)

@method_decorator([login_required, manager_required], name='dispatch')
class AvailabledateCreateView(CreateView):
    model = Availabledate
    fields = ('name', 'date')
    template_name = 'booking/managers/availabledate_add_form.html'

    def form_valid(self, form):
        aailabledates = form.save(commit=False)
        aailabledates.owner = self.request.user
        aailabledates.save()
        messages.success(self.request, 'The availabledates was created with success!')
        return redirect('managers:availabledate_change', aailabledates.pk)


@method_decorator([login_required, manager_required], name='dispatch')
class VaccinetypeUpdateView(UpdateView):
    model = Vaccinetype
    fields = ('name',)
    context_object_name = 'vaccinetype'
    template_name = 'booking/managers/vaccinetype_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing vaccinetypes that belongs
        to the logged in user.
        '''
        return self.request.user.vaccinetypes.all()

    def get_success_url(self):
        return reverse('managers:vaccinetype_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, manager_required], name='dispatch')
class VaccinecenterUpdateView(UpdateView):
    model = Vaccinecenter
    fields = ('name', )
    context_object_name = 'vaccinecenter'
    template_name = 'booking/managers/vaccinecenter_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing vaccinecenters that belongs
        to the logged in user.
        '''
        return self.request.user.vaccinecenters.all()

    def get_success_url(self):
        return reverse('managers:vaccinecenter_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, manager_required], name='dispatch')
class AvailabledateUpdateView(UpdateView):
    model = Availabledate
    fields = ('name', 'date')
    context_object_name = 'availabledate'
    template_name = 'booking/managers/availabledate_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing availabledates that belongs
        to the logged in user.
        '''
        return self.request.user.availabledates.all()

    def get_success_url(self):
        return reverse('managers:availabledate_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, manager_required], name='dispatch')
class VaccinetypeDeleteView(DeleteView):
    model = Vaccinecenter
    context_object_name = 'vaccinetype'
    template_name = 'booking/managers/vaccinetype_delete_confirm.html'
    success_url = reverse_lazy('managers:vaccinetype_change_list')

    def delete(self, request, *args, **kwargs):
        vaccinetype = self.get_object()
        messages.success(request, 'The vaccine type %s was deleted with success!' % vaccinetype.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.vaccinetypes.all()


@method_decorator([login_required, manager_required], name='dispatch')
class AvailabledateDeleteView(DeleteView):
    model = Availabledate
    context_object_name = 'availabledate'
    template_name = 'booking/managers/availabledate_delete_confirm.html'
    success_url = reverse_lazy('managers:availabledate_change_list')

    def delete(self, request, *args, **kwargs):
        availabledate = self.get_object()
        messages.success(request, 'The availabledate type %s was deleted with success!' % availabledate.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.availabledates.all()

@method_decorator([login_required, manager_required], name='dispatch')
class VaccinecenterDeleteView(DeleteView):
    model = Vaccinecenter
    context_object_name = 'vaccinecenter'
    template_name = 'booking/managers/vaccinecenter_delete_confirm.html'
    success_url = reverse_lazy('managers:vaccinecenter_change_list')

    def delete(self, request, *args, **kwargs):
        vaccinecenter = self.get_object()
        messages.success(request, 'The vaccinecenter %s was deleted with success!' % vaccinecenter.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.vaccinecenters.all()

@method_decorator([login_required, manager_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    model = Appointment
    ields = ('name', 'dose_type', 'vaccinetype', 'vaccinecenter','date_of_vaccine1')
    context_object_name = 'appointment'
    template_name = 'booking/managers/appointment_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing appointments that belongs
        to the logged in user.
        '''
        return self.request.user.appointments.all()

    def get_success_url(self):
        return reverse('managers:appointment_change', kwargs={'pk': self.object.pk})
