from django.conf.urls.defaults import patterns, url, include
from http_utils.dispatcher import dispatch

urlpatterns = patterns('',
    url(r'^$', dispatch(get='news.views.home'), name='competition_news'),
    url(r'^(?P<year>[-\w]+)/(?P<month>[-\w]+)/(?P<day>[-\w]+)/(?P<article_slug>[-\w]+)/?$',
        dispatch(get='news.views.show_news_article'),
        name='show_news_article'),
    url(r'^add/?$', dispatch(get='news.views.article_add_edit',
                     post='news.views.article_add_edit'),
                     name='article_add'),
    url(r'^(?P<article_uid>[-\w]+)/delete/?$', dispatch(get='news.views.article_delete',
                     post='news.views.article_delete'),
                     name='article_delete'),
    url(r'^(?P<article_uid>[-\w]+)/edit/?$', dispatch(get='news.views.article_add_edit',
                     post='news.views.article_add_edit'),
                     name='article_edit')

) 
