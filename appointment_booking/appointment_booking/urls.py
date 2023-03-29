from django.urls import include, path
from django.contrib import admin

from booking.views import booking, endusers, managers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', booking.SignUpView.as_view(), name='signup'),
    path('accounts/signup/enduser/', endusers.EnduserSignUpView.as_view(), name='enduser_signup'),
    path('accounts/signup/manager/', managers.ManagerSignUpView.as_view(), name='manager_signup'),
]
