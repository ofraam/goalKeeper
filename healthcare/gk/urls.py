from django.conf.urls import url

from gk import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^goal/(?P<goal_name>[\w ]+)/$', views.goal, name='goal'),
    url(r'^action/$', views.action, name='action'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^profile/$', views.profile, name='profile'),
]

#urlpatterns += staticfiles_urlpatterns()