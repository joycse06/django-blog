from django.conf.urls import url, patterns, include
from forms import SignupFormExtra

urlpatterns = patterns('',
    (r'^accounts/signup/$',
        'userena.views.signup',
        {'signup_form': SignupFormExtra}),
)