from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from ..decorators import enduser_required
from ..forms import EnduserSignUpForm, AppointmentForm
from ..models import Enduser,  User, Vaccinetype, Vaccinecenter, Appointment, Availabledate

class EnduserSignUpView(CreateView):
    model = User
    form_class = EnduserSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'enduser'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        login(self.request, user)
        return redirect('endusers:enduser_home_view')


def enduser_home_view(request):
    return render(request, 'booking/endusers/enduser_home_view.html')


@method_decorator([login_required, enduser_required], name='dispatch')
class VaccinetypeListView(ListView):
    model = Vaccinetype
    ordering = ('name', )
    context_object_name = 'vaccinetypes'
    template_name = 'booking/endusers/vaccinetype_list.html'

    def get_queryset(self):
        enduser = self.request.user.enduser
        queryset = Vaccinetype.objects.all()
        return queryset


@method_decorator([login_required, enduser_required], name='dispatch')
class VaccinecenterListView(ListView):
    model = Vaccinecenter
    ordering = ('name', )
    context_object_name = 'vaccinecenters'
    template_name = 'booking/endusers/vaccinecenter_list.html'

    def get_queryset(self):
        return self.request.user.vaccinecenters.all()

@method_decorator([login_required, enduser_required], name='dispatch')
class AvailabledateListView(ListView):
    model = Availabledate
    ordering = ('name', )
    context_object_name = 'availabledates'
    template_name = 'booking/endusers/availabledate_list.html'

    def get_queryset(self):
        return self.request.user.availabledates.all()

@method_decorator([login_required, enduser_required], name='dispatch')
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    # fields = ('name', 'dose_type', 'vaccinetype', 'vaccinecenter')
    template_name = 'booking/endusers/appointment_add_form.html'


    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.owner = self.request.user
        appointment.save()
        messages.success(self.request, 'The appointment was created with success!')
        return redirect('endusers:appointment_change', appointment.pk)


@method_decorator([login_required, enduser_required], name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    ordering = ('name', )
    context_object_name = 'appointments'
    template_name = 'booking/endusers/appointment_change_list.html'

    def get_queryset(self):
        return self.request.user.appointments.all()


@method_decorator([login_required, enduser_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ('name', 'dose_type', 'vaccinetype', 'vaccinecenter','date_of_vaccine1', 'availabledate')

    context_object_name = 'appointment'
    template_name = 'booking/endusers/appointment_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing appointments that belongs
        to the logged in user.
        '''
        return self.request.user.appointments.all()

    def get_success_url(self):
        return reverse('endusers:appointment_change', kwargs={'pk': self.object.pk})
