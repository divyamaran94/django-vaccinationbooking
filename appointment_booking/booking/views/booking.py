from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_manager:
            return redirect('managers:manager_home_view')
        else:
            return redirect('endusers:enduser_home_view')
    return render(request, 'booking/home.html')

