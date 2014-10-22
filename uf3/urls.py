from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'biz.views.index', name='home'),
    url(r'^map.geojson$', 'biz.views.geojson', name='map'),
    url(r'^stats$', "biz.views.stats", name="stats"),
    url(r'^stats.json$', "biz.views.complex", name="stats_json"),
    url(r'^add$', "biz.views.add", name="add_venue"),
    url(r'^edit/(?P<business_id>\d+)$', "biz.views.edit", name="edit_venue"),
    url(r'^update/(?P<business_id>\d+)$', "biz.views.update", name="edit_venue"),
	
    url(r'^data.csv$','biz.views.get_csv',name="csv"),
    url(r'^login$','biz.views.login',name="login_page"),
    url(r'^logout$','biz.views.logout',name="logout_page"),

    url(r'^accounts/profile','biz.views.profile',name="profile_redirect"),
    url(r'^users/(?P<username>\w+)$','biz.views.user',name="profile"),


	url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
