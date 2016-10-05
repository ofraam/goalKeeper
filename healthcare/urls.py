from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin

admin.autodiscover()

app_name = 'healthcare'
urlpatterns = [
    url(r'^goalkeeper/', include('gk.urls', namespace="gk")),
    url(r'^', include('healthcare.urls', namespace="healthcare")),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^admin/', include(admin.site.urls)),
]
