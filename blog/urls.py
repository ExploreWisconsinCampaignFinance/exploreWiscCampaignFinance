from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^post_index$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^asm_leadership$', views.asm_leadership, name="asm_leadership"),
    #url(r'', views.asm_leadership, name="asm_leadership"),
    url(r'^legend_data$', views.legend_data, name="legend_data"),
    url(r'^contrib_sources_by_party$', views.contrib_sources_by_party, name="contrib_sources_by_party"),
    url(r'^test$', views.test_retrieval, name="test_retrieval"),
    url(r'^data_contrib_sources_by_party$', views.contrib_sources_data, name="contrib_sources_data"),
    url(r'^contributor_data', views.contributor_data, name="contributor_data")
]
