from django.core import urlresolvers
from django.contrib.syndication.views import Feed
from django.http import Http404
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User  # NOQA
from django.conf import settings
from django.utils import feedgenerator

#
# Support for django 1.3
#
try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.utils.functional import lazy
    reverse_lazy = lazy(urlresolvers.reverse)

from tagging.models import Tag, TaggedItem

from fusionbox.blog.models import Blog


class BlogFeed(Feed):
    title = getattr(settings, 'BLOG_TITLE', "Blog")
    link = reverse_lazy('blog:blog_index')
    description = getattr(settings, 'BLOG_DESCRIPTION', None)
    feed_type = feedgenerator.Atom1Feed

    def items(self, obj):
        if isinstance(obj, User):
            objs = obj.blogs.all()
        elif isinstance(obj, Tag):
            objs = TaggedItem.objects.get_by_model(Blog, obj)
        else:
            objs = Blog.objects.all()

        objs = objs.published().order_by('-publish_at')

        limit = getattr(settings, 'BLOG_FEED_ITEMS', None)
        if limit is not None:
            objs = objs[:limit]
        return objs

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        try:
            return item.author.first_name + item.author.last_name
        except AttributeError:
            return item.author.get_full_name()

    def item_author_link(self, item):
        return urlresolvers.reverse('blog:author', kwargs={'author_id': item.author.id})

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.publish_at

    def item_categories(self, item):
        return [i.name for i in Tag.objects.get_for_object(item)]

    def get_object(self, request, *args, **kwargs):
        try:
            return User.objects.get(id=kwargs['author_id'])
        except User.DoesNotExist:
            raise Http404
        except KeyError:
            pass

        try:
            return Tag.objects.get(name=kwargs['tag'])
        except Tag.DoesNotExist:
            raise Http404
        except KeyError:
            pass
