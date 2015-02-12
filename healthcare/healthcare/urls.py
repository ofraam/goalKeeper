from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'healthcare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', 'healthcare.views.show_login', name='home'),
   	url(r'^home/', 'healthcare.views.home', name='home'),
    url(r'^goalkeeper/', include('gk.urls')),    
    #check our own login and logout handlers too
    url(r'^login/', 'healthcare.views.login_handler'),
    url(r'^logout/', 'healthcare.views.logout_handler'), 
    url(r'^logs/', 'healthcare.views.logs'), 
    url(r'^admin/password_reset/$','django.contrib.auth.views.password_reset', name='admin_password_reset'), 
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete', name='password_reset_complete'), 
    url(r'^admin/', include(admin.site.urls)),


)
