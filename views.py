from decorators import needs_user, wants_user
from http_utils.decorators import html
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from su_utils.mongo import django_get_mongodb_connection, django_mongo_op
from news.backends import news
from news.forms import EntryAddForm, EntryEditForm
import datetime

@wants_user
@html('news/home.html')
def home(request, competition_slug):
        return {'competition_slug':competition_slug, 
                'news':news.get_many(competition_slug, ignore_dates=True), 
                'recent_posts':news.get_many(competition_slug, ignore_dates=True, page_size=10)}  

@wants_user
@html('news/article.html')
def show_news_article(request, competition_slug, year, month, day, article_slug):
        return {'competition_slug':competition_slug, 
                'article': news.get_by_slug(competition_slug, article_slug),  
                'recent_posts':news.get_many(competition_slug, ignore_dates=True, page_size=10)}  

@html('news/unauth/entry.html')
def _unauth_news_article(request, article_uid):
    return {}

@needs_user
@html('news/article_add_edit.html')
def article_add_edit (request, competition_slug, article_uid=None):
    
    if article_uid is not None and request.method != 'POST':
        form = EntryAddForm()
        article = news.get_by_id_or_404(article_uid)
        form.fields['title'].initial = article.get('title', None)
        form.fields['author'].initial = article.get('author', None)
        form.fields['content'].initial = article.get('content', None)
    elif article_uid is None and request.method != 'POST':
        form = EntryAddForm() 
    else:
        form = EntryAddForm(request.POST)
  
    if form.is_valid():
        try:
            if article_uid is not None:
                updated_attrs = {
                    'competition_slug':competition_slug,
                    'title':form.cleaned_data['title'],
                    # needs slugify
                    'article_slug':'slug',
                    'author':form.cleaned_data['author'],
                    'content':form.cleaned_data['content'],
                    'excerpt':form.cleaned_data['content'], 
                    'post_date':datetime.datetime.utcnow()
                    }
                news.update(article_uid, updated_attrs)
                messages.info(request, "Your article has been updated")
                return redirect(reverse('competition_news', args=[request.competition['slug']]))
                
            else:
                news.add ( 
                    competition_slug=competition_slug,
                    title=form.cleaned_data['title'],
                    # needs slugify
                    article_slug='slug',
                    author=form.cleaned_data['author'],
                    content=form.cleaned_data['content'],
                    excerpt=form.cleaned_data['content'], 
                    post_date=datetime.datetime.utcnow()
                    ) 
                
                messages.info(request, "Your article has been added")
                return redirect(reverse('competition_news', args=[request.competition['slug']]))
        except Exception as e:
            messages.error(request, "There has been an error; contact your system administrator")
    return {'form':form, 'competition_slug':competition_slug, 'article_uid':article_uid,
            'recent_posts':news.get_many(competition_slug, ignore_dates=True, page_size=10)}  

@needs_user
@html('news/delete.html')
def article_delete (request, competition_slug, article_uid):
    if request.user:
        news.delete(article_uid)
        messages.info(request, "Article has been deleted")
        return redirect(reverse('competition_news', args=[request.competition['slug']]))
    else:
        return _unauth_news_home(request, competition_slug)
 

