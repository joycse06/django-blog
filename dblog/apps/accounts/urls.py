from django.conf.urls import url, patterns, include


urlpatterns = patterns('',
    (r'^accounts/signup/$',
        'userena.views.signup',
        {'signup_form': SignupExtraProfileForm}),
)