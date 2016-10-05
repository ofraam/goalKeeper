from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'healthcare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', 'healthcare.views.show_login', name='home'),
   	url(r'^home/', 'healthcare.views.home', name='home'),  
    #check our own login and logout handlers too
    url(r'^login/', 'healthcare.views.login_handler', name='login'),
    url(r'^logout/', 'healthcare.views.logout_handler', name='logout'), 
    url(r'^logs/', 'healthcare.views.logs'), 
]
