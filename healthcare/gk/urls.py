from django.conf.urls import url, include

from gk import views

urlpatterns = [
	url(r'^$', views.landing_page, name='home'),
    url(r'^goal/(?P<goal_id>[\w ]+)/$', views.goal, name='goal'),
    url(r'^goal/(?P<goal_id>[\w ]+)/edit_status/$', views.edit_status, name='goal_edit'),
    url(r'^action/(?P<patient_id>[\w ]+)/$', views.action, name='action'),
    url(r'^contacts/(?P<patient_id>[\w ]+)/$', views.contacts, name='contacts'),
    url(r'^profile/(?P<patient_id>[\w ]+)/$', views.profile, name='profile'),
    url(r'^(?P<user_id>\w+)/$', views.home, name='home'),
    url(r'^api/goal_over_time/(?P<goal_id>[\w ]+)', views.goal_over_time, name='goal_over_time'),
]

#urlpatterns += staticfiles_urlpatterns()