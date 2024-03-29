from django.contrib import admin
from django.conf.urls import patterns, include, url
from dblog.settings.common import *



# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('dblog.apps.accounts.urls')),
    (r'^accounts/', include('userena.urls')),
    url(r'^blog/', include('dblog.apps.blogengine.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    url(r'', include('dblog.apps.static_pages.urls')),
)
