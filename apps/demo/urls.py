from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^resource/(.*)', 'djubby.dispatcher'),

)

