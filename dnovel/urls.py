from adminplus.sites import AdminSitePlus
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from dnovel import settings


admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^xmy/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'', include('novel.urls')),
    # url(r'^dnovel/', include('dnovel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

