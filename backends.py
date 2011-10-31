from su_utils.mongo import django_mongo_op, django_get_mongodb_connection, ensure_index
from pymongo.errors import OperationFailure
from pymongo import ASCENDING
from pymongo import DESCENDING
from django.http import Http404
import uuid, datetime

def ensure_indexes():
    pass

ensure_indexes()


class News(object):
    def __init__(self, **kwargs):
        pass

    def get(self, article_uid):
        @django_mongo_op
        def _get_article():
            collection = django_get_mongodb_connection().su.news
            return collection.find_one({'uid':article_uid})
        return _get_article()

    def get_by_id_or_404(self, article_uid):
        article = self.get(article_uid)
        if not article:
            raise Http404
        return article 

    def get_by_slug(self, competition_slug, article_slug):
        """
        Competition slug is also required as slugs are unique per comp.
        """ 
        @django_mongo_op
        def _get_entry():
            collection = django_get_mongodb_connection().su.news
            return collection.find_one({'competition_slug':competition_slug,'article_slug':article_slug})
        return _get_entry()
    
    def get_many(self, competition_slug, ignore_dates=False, page=1, page_size=10):
        """
        Gets a list of news entries.
        
        @param ignore_dates: if True, this will not filter on any dates. 
                             Otherwise, reg_start_date and start_date will 
                             default to today.
        @param page: page number to retrieve news entries
        @param page_size: number of competitions to return for each page
         
        """
        collection = django_get_mongodb_connection().su.news
        @django_mongo_op
        def get_news():
            today = datetime.datetime.now()
            criteria = {'competition_slug':competition_slug}
            if not ignore_dates:
                criteria['reg_start_date'] = {'$lte': today}
                criteria['start_date'] = {'$gt': today}
                
            return [c for c in collection.find(criteria)
                                         .sort([('post_date', DESCENDING), 
                                                ('created', ASCENDING)])
                                         .skip((page - 1) * page_size)
                                         .limit(page_size)]
        return get_news()

    def add(self, competition_slug, title, article_slug, author, content, excerpt, post_date):
        """
        Add a news article 
        """
        article = {'uid':uuid.uuid1().hex,
                    'competition_slug': competition_slug,
                    'title': title, 
                    'article_slug': article_slug, 
                    'author': author, 
                    'post_date': post_date, 
                    'content': content, 
                    'excerpt': excerpt,
                }
        @django_mongo_op
        def _add_article():
            collection = django_get_mongodb_connection().su.news
            collection.insert(article, safe=True)
        _add_article()

    def update(self, article_uid, updated_attributes):
        """
        Update a news entry.
        Pass a dict of news attributes to change.
        """
        @django_mongo_op
        def _update_article():
            collection = django_get_mongodb_connection().su.news
            collection.update({'uid':article_uid}, {'$set':updated_attributes},
                              upsert=False, safe=True, multi=False)
        _update_article()

    def delete(self, uid):
        """
        Delete an entry 
        """
        @django_mongo_op
        def _remove_entry():
            article = django_get_mongodb_connection().su.news
            article.remove({'uid':uid})
        _remove_entry()
         

news = News()
        
