from django.urls import include, path

from .views import booking, endusers, managers

urlpatterns = [
    path('', booking.home, name='home'),

    path('endusers/', include(([
        path('', endusers.enduser_home_view, name='enduser_home_view'),

        path('appointment/add/', endusers.AppointmentCreateView.as_view(), name='appointment_add'),
        path('appointment/<int:pk>/', endusers.AppointmentUpdateView.as_view(), name='appointment_change'),
        path('appointment/view/', endusers.AppointmentListView.as_view(), name='appointment_change_list'),

       
    ], 'booking'), namespace='endusers')),

    path('managers/', include(([
       

        path('', managers.manager_home_view, name='manager_home_view'),


        path('vaccinetype/add/', managers.VaccinetypeCreateView.as_view(), name='vaccinetype_add'),
        path('vaccinecenter/add/', managers.VaccinecenterCreateView.as_view(), name='vaccinecenter_add'),
        path('availabledate/add/', managers.AvailabledateCreateView.as_view(), name='availabledate_add'),



        path('vaccinetype/view/', managers.VaccinetypeListView.as_view(), name='vaccinetype_change_list'),
        path('vaccinecenter/view/', managers.VaccinecenterListView.as_view(), name='vaccinecenter_change_list'),
        path('appointment/view/', managers.AppointmentListView.as_view(), name='appointment_change_list'),
        path('availabledate/view/', managers.AvailabledateListView.as_view(), name='availabledate_change_list'),


        path('vaccinetype/<int:pk>/', managers.VaccinetypeUpdateView.as_view(), name='vaccinetype_change'),
        path('vaccinecenter/<int:pk>/', managers.VaccinecenterUpdateView.as_view(), name='vaccinecenter_change'),
        path('availabledate/<int:pk>/', managers.AvailabledateUpdateView.as_view(), name='availabledate_change'),

        path('appointment/<int:pk>/', managers.AppointmentUpdateView.as_view(), name='appointment_change'),

        path('vaccinetype/<int:pk>/delete/', managers.VaccinetypeDeleteView.as_view(), name='vaccinetype_delete'),
        path('vaccinecenter/<int:pk>/delete/', managers.VaccinecenterDeleteView.as_view(), name='vaccinecenter_delete'),
        path('availabledate/<int:pk>/delete/', managers.AvailabledateDeleteView.as_view(), name='availabledate_delete'),


        
    ], 'booking'), namespace='managers')),
]
