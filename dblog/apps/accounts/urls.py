from django.conf.urls import url, patterns, include
from forms import SignupFormExtra
from userena import views as userena_views

urlpatterns = patterns('',
    (r'^accounts/signup/$',
        'userena.views.signup',
        {  'template_name':'accounts/signup.html',
           'signup_form': SignupFormExtra}),
    (r'^accounts/signin/$',
        'userena.views.signin',
        {'template_name':'accounts/signin.html'}
    ),
    (r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
       'userena.views.profile_detail',
       {
            'template_name' : 'accounts/profile.html'
        }
    ),
)