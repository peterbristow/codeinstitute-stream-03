"""we_are_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

PJB Note:
Importing "views" from more than one app,
will get a collision unless using aliases with "as".
Use "name" to avoid hard coding urls on code or inside templates.
E.g. reverse('index').
"""

from django.conf.urls import url, include
from django.contrib import admin
from paypal.standard.ipn import urls as paypal_urls
from paypal_store import views as paypal_views
from accounts import views as accounts_views  # aliases: see above note
from home import views as home_views
from products import views as product_views
from magazines import views as magazine_views
from reusable_blog_v1 import urls as reusable_blog_v1_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_views.get_index, name='index'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^cancel_subscription/$', accounts_views.cancel_subscription, name='cancel_subscription'),
    url(r'^a-very-hard-to-guess-url/', include(paypal_urls)),
    url(r'^paypal-return/$', paypal_views.paypal_return, name='paypal-return'),
    url(r'^paypal-cancel/$', paypal_views.paypal_cancel, name='paypal-cancel'),
    url(r'^products/$', product_views.all_products, name='products'),
    url(r'^magazines/$', magazine_views.all_magazines, name='magazines'),
    url(r'^blog/', include(reusable_blog_v1_urls)),
]
