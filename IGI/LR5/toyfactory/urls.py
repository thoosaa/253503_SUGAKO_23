"""
URL configuration for toyfactory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/customer/', customer_register, name='customer_register'),
    path('login/customer/', customer_login, name='customer_login'),
    path('login/staff/', staff_login, name='staff_login'),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('logout/', log_out, name='log_out'),
    path('edit/customer/', customer_edit, name='customer_edit'),
    path('edit/staff/', staff_edit, name='staff_edit'),
    path('news/', news_view, name='news'),
    path('faq/', faq_view, name='faq'),
    path('contact/',contact_view, name='contact'),
    path('confidentiality/', confidentiality, name='confidentiality'),
    path('catalogue/', cat, name='catalogue'),
    path('search/', search_toys, name='search_toys'),
    re_path(r'catalogue/buy/(?P<id>\d+)/', buy, name='buy'),
    path('promocode/', promocode, name='promocode'),
    path('jobs/', jobs, name='jobs'),
    re_path(r'delete/(?P<id>\d+)/', delete, name='delete'),
    path('clientinfo/', clientinfo, name='clientinfo'),
    path('salelist/', salesinfo, name='salesinfo'),
    path('feedback/form/', save_feedback, name='feedback form'),
    path('feedback/', feedback, name='feedback'),
    path('sortbypriceasc/', sortbypriceasc, name='sortbypriceasc'),
    path('sortbypricedesc/', sortbypricedesc, name='sortbypriceasc'),
    path('sortbycategory/', sortbycategory, name='sortbycategory'),
    path('citygrouped/', citygrouped, name = 'citygrouped'),
    path('pickuppoints/', pickuplist, name='pickuplist'),
    path('read/customer/', customer_read, name='customer_read'), 
    path('read/staff', staff_read, name='staff_read'),
    path('basestat/', base_stat, name='basestat'),
    path('analysis/', analysis, name='analysis')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
