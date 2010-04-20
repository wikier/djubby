from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^(.*)', 'djubby.dispatcher'),

)

