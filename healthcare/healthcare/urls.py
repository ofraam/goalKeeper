from django.conf.urls import include, url
from healthcare import views as hc_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'healthcare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', hc_views.show_login, name='home'),
   	url(r'^home/', hc_views.home, name='home'),
    #check our own login and logout handlers too
    url(r'^login/', hc_views.login_handler, name='login'),
    url(r'^logout/', hc_views.logout_handler, name='logout'),
    url(r'^logs/', hc_views.logs),
]
