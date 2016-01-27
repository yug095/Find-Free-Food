from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index, name='event_index'),
    url(r'^events/$', views.index, name='event_index'),

    url(r'^events/(?P<pk>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^events/(?P<pk>[0-9]+)/register/$', views.register, name='event_register'),
	url(r'^events/create$', views.create, name='event_create'),
    url(r'^events/(?P<event_id>[0-9]+)/cancel-register/$', views.cancel_register, name='event_cancel_register'),

    url(r'^user/info/$', views.myinfo, name='myinfo'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
	url(r'^signout/$', views.signout, name='signout'),

    url(r'^events/create/$',views.create,name='event_create')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
