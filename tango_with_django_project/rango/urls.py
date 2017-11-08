from django.conf.urls import url
from rango import views

from django.conf.urls import url
from rango import views

urlpatterns =[
    url(r'^$', views.index,  name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^add_page/(?P<category_name_slug>[\w\-]+)/$', views.add_page, name='add_page_category'),
    url(r'^add_page/$', views.add_page, name='add_page'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^register/$', views.register, name='register'),

    url(r'^confirm_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_email, name='confirm_email'),

    url(r'^user_login/$', views.user_login, name='user_login'),

    url(r'^user_logout/$', views.user_logout, name='user_logout'),

]
