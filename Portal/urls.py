from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^scripting101/admin/', include(admin.site.urls)),
    (r'^scripting101/', include('byld.urls')),
) + static('/static/', document_root=settings.STATIC_ROOT)
