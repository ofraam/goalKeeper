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
    url(r'^admin/', include(admin.site.urls)),
    #check our own login and logout handlers too
    url(r'^login/', 'healthcare.views.login_handler'),
    url(r'^logout/', 'healthcare.views.logout_handler'), 
    url(r'^logs/', 'healthcare.views.logs'), 


)
