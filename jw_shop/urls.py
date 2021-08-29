from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #path('admin/', admin.site.urls),
    
    path('', include('store.urls')),

]
